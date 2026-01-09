// 1. 논문 데이터 관리
// type: 'journal', 'conf_intl', 'poster_intl', 'conf_dom', 'poster_dom'
const papers = [
    {
        type: "journal",
        year: 2025,
        title: "Tactile Enhancement of Mid-Air Ultrasonic Stimulation by Wrist Vibration: Perceived Intensity and Pattern Recognition",
        authors: "Dong-Geun Kim, Seungmoon Choi",
        venue: "IEEE Transactions on Haptics",
        link: "https://ieeexplore.ieee.org/document/11045208",
        pdf: "files/J_Enhancement.pdf"
    },
    {
        type: "journal",
        year: 2024,
        title: "Sound-to-Touch Crossmodal Pitch Matching for Short Sounds",
        authors: "Dong-Geun Kim, Jungeun Lee, Gyeore Yun, Hong Z. Tan, and Seungmoon Choi",
        venue: "IEEE Transactions on Haptics",
        link: "https://ieeexplore.ieee.org/document/10337769",
        pdf: "files/Crossmodal.pdf"
    },
    {
        type: "conf_intl",
        year: 2024,
        title: "A Feasibility Study of Tactile Enhancement of Mid-Air Ultrasonic Stimulation by Wrist Vibration",
        authors: "Dong-Geun Kim and Seungmoon Choi",
        venue: "Proceedings of EuroHaptics",
        link: "https://dl.acm.org/doi/10.1007/978-3-031-70061-3_1",
        pdf: "files/1071-doc.pdf"
    },
    {
        type: "conf_intl",
        year: 2023,
        title: "Generating Real-Time, Selective, and Multimodal Haptic Effects from Sound for Gaming Experience Enhancement",
        authors: "Gyeore Yun, Minjae Mun, Jungeun Lee, Dong-Geun Kim, Hong Z Tan, and Seungmoon Choi",
        venue: "Proceedings of the ACM CHI Conference on Human Factors in Computing Systems (CHI)",
        link: "https://dl.acm.org/doi/full/10.1145/3544548.3580787",
        pdf: "files/3544548.3580787.pdf"
    },
    {
        type: "conf_intl",
        year: 2022,
        title: "Vibration-Augmented Buttons: Information Transmission Capacity and Application to Interaction Design",
        authors: "Chaeyong Park, Jeongwoo Kim, Dong-Geun Kim, Seungjae Oh, and Seungmoon Choi",
        venue: "Proceedings of the ACM CHI Conference on Human Factors in Computing Systems (CHI)",
        link: "https://dl.acm.org/doi/abs/10.1145/3491102.3501849",
        pdf: "files/3491102.3501849.pdf"
    },
    {
        type: "poster_intl",
        year: 2025,
        title: "Tactile Localization in Forearm-Mounted Multi-Tactor Displays: The Effect of Tactor Number and Position",
        authors: "Dong-Geun Kim, Suheon Nam, Geunho Lee, Chaeyong Park and Seungmoon Choi",
        venue: "IEEE World Haptics Conference",
        link: "",
        pdf: "files/wipwhc.pdf"
    },
    {
        type: "poster_intl",
        year: 2023,
        title: "Real-Time, Selective, and Multimodal Haptic Feedback from Gameplay Sound",
        authors: "Gyeore Yun, Jungeun Lee, Dong-Geun Kim, Minjae Mun, Hong Z. Tan, and Seungmoon Choi",
        venue: "IEEE World Haptics Conference",
        link: "",
        pdf: ""
    },
    {
        type: "poster_intl",
        year: 2022,
        title: "MMGrip: A Handheld Multimodal Haptic Device Combining Vibration, Impact, and Shear for Realistic Expression of Contact",
        authors: "Dong-Geun Kim, Jungeun Lee, and Seungmoon Choi",
        venue: "Proceedings of SIGGRAPH Asia Posters",
        link: "https://dl.acm.org/doi/abs/10.1145/3550082.3564177",
        pdf: "files/3550082.3564177.pdf"
    },
    {
        type: "conf_dom",
        year: 2024,
        title: "A Feasibility Study of Tactile Enhancement of Mid-Air Ultrasonic Stimulation by Wrist Vibration",
        authors: "Dong-Geun Kim and Seungmoon Choi",
        venue: "Proceedings of Korea Haptics Conference",
        link: "",
        pdf: "files/koreaHap.pdf"
    },
    {
        type: "poster_dom",
        year: 2024,
        title: "Investigating the Luxuriousness of Haptic Warning on the Steering Wheel",
        authors: "Jeongwoo Kim, Jungeun Lee, Dong-Geun Kim, Ki-Min Kwon, Beomyoung Chung, Junseong Park, Taeuk Kang, Sangji Moon, Wonseok Leee, Sung H. Han, and Seungmoon Choi",
        venue: "Spring Conference, The Acoustical Society of Korea",
        link: "",
        pdf: ""
    },
    {
        type: "conf_dom",
        year: 2024,
        title: "MMGrip: A Multimodal Haptic Device Combining Vibration, Impact, and Shear for Realistic Haptic Feedback ",
        authors: "Dong-Geun Kim, Jungeun Lee and Seungmoon Choi",
        venue: "Korean Institute of Information Scientists and Engineers (KIISE)",
        link: "https://www.dbpia.co.kr/Journal/articleDetail?nodeId=NODE11224329",
        pdf: "files/MMGRIP_DOMESTIC.pdf"
    },
    {
        type: "conf_dom",
        year: 2023,
        title: "음향-촉감 교차 모달 스펙트럼 매칭",
        authors: "Dong-Geun Kim, Jungeun Lee, Gyeore Yun, Hong Z. Tan, and Seungmoon Choi",
        venue: "Korean Institute of Next Generation Computing",
        link: "",
        pdf: ""
    }
];

// 2. 수상(Awards) 데이터 관리
const awards = [
    {
        year: 2024,
        title: "Best ToH Short Paper Award (Finalist)",
        venue: "IEEE Haptics Symposium"
    },
    {
        year: 2022,
        title: "Best Paper Award",
        venue: "KSC (KIISE)"
    }
];


// 3. 실행 및 렌더링
document.addEventListener('DOMContentLoaded', () => {
    // 탭 기능
    const tabs = document.querySelectorAll('.tab-btn');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));
            tab.classList.add('active');
            const targetId = tab.getAttribute('data-target');
            document.querySelector(targetId).classList.add('active');
        });
    });

    // 화면 렌더링 함수들 실행
    renderPublications();
    renderAwards();      // CV 탭의 Awards
    renderRecentNews();  // About 탭의 Recent News
});


// [함수 1] 논문 목록 렌더링
function renderPublications() {
    console.log("Rendering Publications...");

    const categories = [
        { type: 'journal', id: 'journal-list', prefix: 'J' },
        { type: 'conf_intl', id: 'conf-intl-list', prefix: 'C' },
        { type: 'poster_intl', id: 'poster-intl-list', prefix: 'PDA' },
        { type: 'conf_dom', id: 'conf-dom-list', prefix: 'DC' },
        { type: 'poster_dom', id: 'poster-dom-list', prefix: 'DP' }
    ];

    categories.forEach(cat => {
        const listElement = document.getElementById(cat.id);
        if (!listElement) return;

        const filteredPapers = papers
            .filter(p => p.type === cat.type)
            .sort((a, b) => b.year - a.year);

        listElement.innerHTML = filteredPapers.map((paper, index) => {
            const number = `${cat.prefix}${index + 1}`;
            const highlightedAuthors = paper.authors.replace("Dong-Geun Kim", "<strong>Dong-Geun Kim</strong>");

            let linksHtml = '';
            if (paper.link) {
                linksHtml += `<a href="${paper.link}" target="_blank" class="resource-link">[Link]</a>`;
            }
            if (paper.pdf) {
                linksHtml += `<a href="${paper.pdf}" target="_blank" class="resource-link pdf">[PDF]</a>`;
            }

            return `
                <li>
                    [${number}] ${highlightedAuthors},
                    "${paper.title}",
                    <em>${paper.venue}</em>, ${paper.year}.
                    <br>
                    ${linksHtml}
                </li>
            `;
        }).join('');
    });
}

// [함수 2] 수상(Awards) 목록 렌더링
function renderAwards() {
    const listElement = document.getElementById('award-list');
    if (!listElement) return;

    const sortedAwards = awards.sort((a, b) => b.year - a.year);

    listElement.innerHTML = sortedAwards.map(award => {
        return `
            <li>
                <strong>${award.title}</strong>, ${award.venue}, ${award.year}
            </li>
        `;
    }).join('');
}

// [함수 3] Recent News 자동 생성 (논문 타입별 문구 수정됨)
function renderRecentNews() {
    const listElement = document.getElementById('recent-news-list');
    if (!listElement) return;

    // 1. 논문 뉴스 변환 (타입별 문구 분기)
    const paperNews = papers.map(p => {
        let typeText = "Paper"; // 기본값

        if (p.type === 'journal') {
            typeText = "Journal paper";
        } else if (p.type.includes('conf')) { // conf_intl, conf_dom
            typeText = "Conference paper";
        } else if (p.type.includes('poster')) { // poster_intl, poster_dom
            typeText = "Poster";
        }

        return {
            year: p.year,
            content: `${typeText} accepted to <strong>${p.venue}</strong>.`
        };
    });

    // 2. 수상 뉴스 변환
    const awardNews = awards.map(a => ({
        year: a.year,
        content: `<strong>${a.title}</strong> at ${a.venue}.`
    }));

    // 3. 합치고 정렬 및 상위 5개 추출
    const allNews = [...paperNews, ...awardNews]
        .sort((a, b) => b.year - a.year);

    const recentItems = allNews.slice(0, 5); // 최신 5개만 보여줌

    // 4. HTML 생성
    listElement.innerHTML = recentItems.map(item => {
        return `
            <li>
                <span class="date">${item.year}</span> ${item.content}
            </li>
        `;
    }).join('');
}
