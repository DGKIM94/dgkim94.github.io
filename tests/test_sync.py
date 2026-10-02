import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from sync_scholar import parse_page, validate_snapshot, atomic_save
from build import publications

PAGE = '''<div id="gsc_prf_in">Dong-Geun Kim</div>
<table><tr class="gsc_a_tr"><td><a class="gsc_a_at" href="/citations?citation_for_view=XD8q7lsAAAAJ:one">A &amp; B</a>
<div class="gs_gray">DG Kim, S Choi</div><div class="gs_gray">Journal 1 (2)<span class="gs_oph">, 2026</span></div></td>
<td class="gsc_a_ac">1,234</td><td class="gsc_a_y">2026</td></tr></table>
<button id="gsc_bpf_more" disabled>Show more</button>'''

class SyncTests(unittest.TestCase):
    def test_real_fields_and_completion(self):
        papers, more, _ = parse_page(PAGE, 'XD8q7lsAAAAJ', 'Dong-Geun Kim')
        self.assertFalse(more)
        self.assertEqual(papers[0]['title'], 'A & B')
        self.assertEqual(papers[0]['venue'], 'Journal 1 (2)')
        self.assertEqual(papers[0]['citations'], 1234)
        self.assertEqual(papers[0]['year'], 2026)
    def test_block_or_wrong_author_is_rejected(self):
        for source in ['<html>unusual traffic</html>', PAGE.replace('Dong-Geun Kim', 'Someone Else')]:
            with self.assertRaises(ValueError):
                parse_page(source, 'XD8q7lsAAAAJ', 'Dong-Geun Kim')
    def test_missing_pagination_cannot_silently_truncate(self):
        with self.assertRaises(ValueError):
            parse_page(PAGE.split('<button')[0], 'XD8q7lsAAAAJ', 'Dong-Geun Kim')
        self.assertTrue(parse_page(PAGE.replace(' disabled', ''), 'XD8q7lsAAAAJ', 'Dong-Geun Kim')[1])
    def test_dropped_records_preserve_previous_snapshot(self):
        a={'id':'a','title':'One','authors':'DG Kim'}
        b={'id':'b','title':'Two','authors':'DG Kim'}
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'snapshot.json'
            atomic_save(path, {'articles':[a,b]})
            before=path.read_bytes()
            with self.assertRaises(ValueError):
                validate_snapshot({'articles':[a]}, json.loads(before))
            self.assertEqual(path.read_bytes(), before)
        validate_snapshot({'articles':[a]}, {'articles':[a,b]}, allow_removals=True)
    def test_empty_and_duplicate_records_fail(self):
        a={'id':'a','title':'One','authors':'DG Kim'}
        for articles in [[], [a,a]]:
            with self.assertRaises(ValueError):
                validate_snapshot({'articles':articles}, {})
    def test_scholar_year_wins_and_manual_items_remain(self):
        article={'id':'a','title':'Scholar title','authors':'DG Kim','venue':'Journal','year':2023}
        overrides={'a':{'year':2024,'title':'Old title','full_authors':'Dong-Geun Kim','type':'journal'}}
        extra=[{'id':'manual','title':'Poster','authors':'DG Kim','venue':'Domestic meeting','year':2024,'type':'poster_dom','source':'Existing website'}]
        items=publications({'articles':[article]}, overrides, extra)
        canonical=next(p for p in items if p['id']=='a')
        self.assertEqual(canonical['year'],2023)
        self.assertEqual(canonical['title'],'Scholar title')
        self.assertEqual(len(items),2)

if __name__ == '__main__':
    unittest.main()
