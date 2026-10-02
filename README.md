# Dong-Geun Kim — research homepage

기존 GitHub Pages 주소 `https://dgkim94.github.io`에 적용하는 개편본입니다.

## 먼저 보기

`index.html`을 더블클릭하면 웹사이트를 볼 수 있습니다. 검색·필터도 서버 없이 작동합니다.
`files/DongGeunKim_CV.pdf`는 동일한 논문 데이터로 생성한 PDF CV입니다.

## GitHub에 적용하기 — 처음 한 번만

1. 기존 저장소의 **Code → Download ZIP**으로 현재 버전을 백업합니다.
2. 이 압축파일의 `dgkim94.github.io` 폴더 안 내용을 기존 저장소에 덮어씁니다. 폴더 자체를 한 단계 더 넣지 마세요.
3. **`.github/workflows/update-and-deploy.yml`도 반드시 포함**합니다. GitHub 웹 업로드에서 숨김 폴더가 누락되면, 저장소의 **Add file → Create new file**에 이 경로를 입력하고 파일 내용을 붙여넣습니다.
4. 저장소 **Settings → Actions → General → Workflow permissions → Read and write permissions**를 선택하고 저장합니다. 보호된 `main` 브랜치가 봇 커밋을 막는 경우에는 자동 갱신 커밋을 허용하는 저장소 설정이 필요합니다.
5. **Settings → Pages → Build and deployment → Source → GitHub Actions**를 선택합니다. 기존 주소는 유지됩니다.
6. **Actions → Update Scholar and deploy CV → Run workflow**를 누릅니다. 기본 브랜치는 이 저장소의 `main`입니다.
7. 완료 후 기존 홈페이지 주소를 새로고침합니다. 첫 실행이 Pages 설정 전에 시작되어 실패했다면 설정 후 다시 실행하면 됩니다.

자동으로 올리는 외부 서비스 가입, API 키, 결제는 필요 없습니다. 이 전달본 자체는 아직 원격 저장소에 반영되지 않았습니다.

## 자동 갱신 동작

- 매주 **월요일 오전 7:23 (한국시간)**, `main` 변경 시, 또는 수동 실행 시 Scholar를 확인합니다. 예약 실행은 GitHub 사정에 따라 지연될 수 있습니다.
- Scholar ID: `XD8q7lsAAAAJ` — 기존 홈페이지에 링크된 본인 프로필입니다.
- 제목, 저자 약식 표기, 학술지/학회, 연도, 인용 수를 Scholar에서 가져옵니다.
- 기존 자료로 확인된 저자의 전체 이름, PDF 링크, 논문 분류는 보조 데이터로 유지합니다. 새 논문은 Scholar 저자 표기로 먼저 반영됩니다.
- Scholar에 없는 국내 발표·포스터는 별도의 목록으로 보존합니다.
- 웹페이지와 PDF CV를 함께 생성한 뒤 **같은 작업에서 직접 Pages를 배포**합니다. 봇의 커밋만으로 Pages 재배포가 시작될 것이라고 가정하지 않습니다.
- PDF CV의 학력, 경력, 수상 등은 Scholar에서 알 수 없으므로 `data/profile.json`에서 관리합니다.

## Scholar 접근이 실패하는 경우

Google Scholar의 공개 HTML을 읽는 방식입니다. **공식 API 연동이 아니므로 Google의 자동 접근 차단이나 페이지 구조 변경에 의해 실패할 수 있습니다. GitHub 실행 환경에서의 접근 성공은 아직 검증되지 않았습니다.**

실패 시 기존 데이터를 지우지 않으며, 마지막 성공한 논문 목록으로 홈페이지와 CV를 유지합니다. 성공 날짜는 사이트에 표시됩니다. 21일 이상 경과하면 방문자에게 최신 논문이 Scholar에 있을 수 있다는 안내를 표시합니다. Actions 실행은 실패 표시와 요약을 남기므로 이메일 등 원하는 알림을 GitHub에서 설정할 수 있습니다.

정상 응답이 비어 있거나, 페이지 목록이 불완전하거나, 이전 논문이 사라지면 자동 덮어쓰기를 거부합니다. 본인이 Scholar에서 논문을 의도적으로 삭제·통합한 경우에만 Run workflow의 `allow_removals`를 체크하세요.

오랫동안 차단된다면 공개 프로필에서 논문 목록을 모두 펼친 후 HTML로 저장하여 아래처럼 수동 갱신할 수 있습니다. CAPTCHA를 우회하지 않습니다.

```bash
python scripts/sync_scholar.py --html saved-profile.html
python scripts/build.py
```

GitHub는 활동이 없는 공개 저장소의 예약 작업을 60일 후 비활성화할 수 있습니다. 자동 갱신이 정상 실행되면 갱신 커밋이 남지만, 연속 실패 등으로 장기간 활동이 없으면 Actions에서 활성화 여부를 확인하세요.

## 데이터 수정 위치

| 파일 | 용도 |
| --- | --- |
| `data/profile.json` | 소개, 학력, 프로젝트, 경력, 수상, 연락처 |
| `data/scholar.json` | 마지막 정상 Scholar 응답; 자동 생성 |
| `data/publication-overrides.json` | Scholar 논문 ID별 전체 저자명, PDF, 분류, 대표 논문 여부 |
| `data/additional-publications.json` | Scholar에 없는 추가 발표 |
| `templates/index.html` | 홈페이지 구조 |
| `style.css` | 색상, 레이아웃, 모바일 디자인 |
| `script.js` | 검색, 필터, 저자 강조 |
| `scripts/build.py` | HTML·PDF 생성 |

`index.html`, `data/publications.json`, `files/DongGeunKim_CV.pdf`는 생성 결과이므로 지속할 수정은 원본 데이터/템플릿에 적용합니다. 새 Scholar 논문의 학회 유형은 학술지/학회명으로 기본 분류되며, 정확한 국내·국제·포스터 구분은 overrides에서 지정할 수 있습니다. 기존 추가 발표가 나중에 Scholar에 등록되면 해당 추가 항목에 `scholar_id`를 넣어 중복을 방지할 수 있습니다.

## 이번 반영 기준

2026-10-02 확인: Scholar 8편, 기존 사이트에서만 확인된 발표 5건. 인용 수 85, h-index 4. 인용 지표는 Scholar 집계이며 추가 발표 수와 혼합하지 않습니다.

- 새로 확인된 2026년 논문: *Effects of Spatiotemporal Parameters on Forearm Vibrotactile Stimulus Identification*.
- *Sound-to-touch crossmodal pitch matching for short sounds*: 기존 사이트의 2024년 대신 Scholar의 2023년 사용.
- 국내 MMGrip 발표: 기존 사이트의 2024년/영문 제목 대신 Scholar의 2022년/한글 제목 사용.
- 기존 PDF CV에는 샘플 인물 이력서가 들어 있어 홈페이지의 실제 정보로 교체했습니다. 기존 Word 파일은 업데이트 대상이 아닙니다.

## 로컬에서 다시 만들기

Python 3.10 이상을 설치한 후 이 폴더에서 실행합니다.

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/sync_scholar.py
python scripts/build.py
python -m http.server 8000 --directory _site
```

`http://localhost:8000`에서 확인합니다. 이미 저장된 데이터로 디자인만 수정할 때는 sync 명령을 생략합니다.

배포 대상 `_site`에는 명시적으로 필요한 파일만 복사됩니다. 저장소 ZIP, Word 임시 파일, Python 소스는 공개 배포에 포함되지 않습니다. 폰트 라이선스는 `assets/fonts`에 있습니다.

참고: [GitHub Pages 배포 설정](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages), [예약 실행](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule).
