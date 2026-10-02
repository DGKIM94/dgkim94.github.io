"""Fetch a complete public Scholar profile, or keep the last good snapshot untouched."""
import argparse
import json
import os
import re
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urljoin, urlparse
from urllib.error import URLError
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


def number(text):
    value = re.sub(r"[^0-9]", "", text or "")
    return int(value) if value else None


def parse_page(html, scholar_id, expected_name):
    soup = BeautifulSoup(html, "html.parser")
    name = soup.select_one("#gsc_prf_in")
    if not name or name.get_text(" ", strip=True).casefold() != expected_name.casefold():
        raise ValueError("Scholar did not return the expected profile (blocked or changed markup).")
    articles = []
    for row in soup.select(".gsc_a_tr"):
        title = row.select_one(".gsc_a_at")
        detail = row.select(".gs_gray")
        if not title or len(detail) < 2:
            raise ValueError("Incomplete Scholar publication row.")
        url = urljoin("https://scholar.google.com", title.get("href", ""))
        article_id = parse_qs(urlparse(url).query).get("citation_for_view", [""])[0]
        if not article_id.startswith(scholar_id + ":"):
            raise ValueError("Unexpected Scholar publication identity.")
        for suffix in detail[1].select(".gs_oph"):
            suffix.decompose()
        year = row.select_one(".gsc_a_y")
        cited = row.select_one(".gsc_a_ac")
        articles.append({
            "id": article_id,
            "title": title.get_text(" ", strip=True),
            "authors": detail[0].get_text(" ", strip=True),
            "venue": detail[1].get_text(" ", strip=True),
            "year": number(year.get_text()) if year else None,
            "citations": number(cited.get_text()) if cited else None,
            "scholar_url": url,
        })
    more = soup.select_one("#gsc_bpf_more")
    if more is None:
        raise ValueError("Cannot verify that Scholar pagination is complete.")
    metrics = {}
    rows = soup.select("#gsc_rsb_st tbody tr")
    for key, row in zip(("citations", "h_index", "i10_index"), rows):
        values = row.select(".gsc_rsb_std")
        if values:
            metrics[key] = number(values[0].get_text())
    return articles, not more.has_attr("disabled"), metrics


def validate_snapshot(snapshot, previous, allow_removals=False):
    articles = snapshot["articles"]
    ids = [a["id"] for a in articles]
    if not articles or len(ids) != len(set(ids)):
        raise ValueError("Empty or duplicate Scholar result; previous data retained.")
    if any(not a["title"] or not a["authors"] for a in articles):
        raise ValueError("Missing publication metadata; previous data retained.")
    missing = {a["id"] for a in previous.get("articles", [])} - set(ids)
    if missing and not allow_removals:
        raise ValueError(f"{len(missing)} previously indexed items are missing. Review before allowing removals.")


def atomic_save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix=".scholar-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def sync(args):
    profile = json.loads((ROOT / "data/profile.json").read_text())
    destination = ROOT / "data/scholar.json"
    previous = json.loads(destination.read_text()) if destination.exists() else {}
    articles, metrics = [], {}
    for start in range(0, 2000, 100):
        if args.html:
            html = args.html.read_bytes()
        else:
            query = urlencode({"user": profile["scholar_id"], "hl": "en", "cstart": start, "pagesize": 100})
            request = Request("https://scholar.google.com/citations?" + query,
                              headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.8"})
            with urlopen(request, timeout=30) as response:
                html = response.read()
        page, has_more, page_metrics = parse_page(html, profile["scholar_id"], profile["name"])
        if not page:
            raise ValueError("Empty page before confirmed end of pagination.")
        articles.extend(page)
        if start == 0:
            metrics = page_metrics
        if not has_more:
            break
        if args.html:
            raise ValueError("Saved HTML is incomplete. Expand the full publication list and save again.")
        time.sleep(2)
    else:
        raise ValueError("Pagination limit reached; refusing an incomplete update.")
    snapshot = {"source": "Google Scholar", "profile_id": profile["scholar_id"],
                "profile_url": profile["scholar_url"],
                "last_successful_sync": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "metrics": metrics, "articles": sorted(articles, key=lambda a: a["id"])}
    validate_snapshot(snapshot, previous, args.allow_removals)
    atomic_save(destination, snapshot)
    print(f"Updated {len(articles)} Scholar publications. Complete snapshot saved.")


def validate_cache():
    """Only a readable snapshot belonging to this author can be used as fallback."""
    profile = json.loads((ROOT / "data/profile.json").read_text())
    cached = json.loads((ROOT / "data/scholar.json").read_text())
    if cached.get("source") != "Google Scholar" or cached.get("profile_id") != profile["scholar_id"]:
        raise ValueError("Saved snapshot does not belong to the configured Scholar profile.")
    datetime.fromisoformat(cached["last_successful_sync"])
    validate_snapshot(cached, {})
    for paper in cached["articles"]:
        if not paper["id"].startswith(profile["scholar_id"] + ":") or not isinstance(paper["venue"], str):
            raise ValueError("Invalid publication in the saved snapshot.")
    if not isinstance(cached["metrics"], dict):
        raise ValueError("Invalid cached metrics.")
    return cached


def record_status(status):
    cached = validate_cache()
    atomic_save(ROOT / "data/scholar-sync-status.json", {
        "status": status,
        "last_attempt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "last_successful_sync": cached["last_successful_sync"],
    })
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
            output.write(f"status={status}\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", type=Path, help="Import a saved complete Scholar profile page.")
    parser.add_argument("--allow-removals", action="store_true", help="Accept intentional profile deletions after review.")
    parser.add_argument("--github-actions", action="store_true", help="Continue with a validated cache on a source-access failure.")
    args = parser.parse_args(argv)
    try:
        sync(args)
    except (URLError, TimeoutError, ValueError) as error:
        if not args.github_actions:
            raise
        # Invalid or missing cache raises here: a genuinely unusable build must still fail.
        record_status("cached")
        message = str(error).replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print(f"::warning title=Scholar refresh unavailable::{message}. Using the last successful snapshot; deployment can continue.")
        return
    record_status("updated")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Scholar sync failed; last successful snapshot preserved: {error}", file=sys.stderr)
        sys.exit(1)
