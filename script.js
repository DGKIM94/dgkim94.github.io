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
        link: "",
        pdf: ""
    },
    {
        type: "conf_intl",
        year: 2023,
        title: "Generating Real-Time, Selective, and Multimodal Haptic Effects from Sound for Gaming Experience Enhancement",
        authors: "Gyeore Yun, Minjae Mun, Jungeun Lee, Dong-Geun Kim, Hong Z Tan, and Seungmoon Choi",
        venue: "Proceedings of the ACM CHI Conference on Human Factors in Computing Systems (CHI)",
        link: "",
        pdf: ""
    },
    {
        type: "conf_intl",
        year: 2022,
        title: "Vibration-Augmented Buttons: Information Transmission Capacity and Application to Interaction Design",
        authors: "Chaeyong Park, Jeongwoo Kim, Dong-Geun Kim, Seungjae Oh, and Seungmoon Choi",
        venue: "Proceedings of the ACM CHI Conference on Human Factors in Computing Systems (CHI)",
        link: "",
        pdf: ""
    },
    {
        type: "poster_intl",
        year: 2025,
        title: "Tactile Localization in Forearm-Mounted Multi-Tactor Displays: The Effect of Tactor Number and Position",
        authors: "Dong-Geun Kim, Suheon Nam, Geunho Lee, Chaeyong Park and Seungmoon Choi",
        venue: "IEEE World Haptics Conference",
        link: "",
        pdf: ""
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
        link: "",
        pdf: ""
    },
    {
        type: "conf_dom",
        year: 2024,
        title: "A Feasibility Study of Tactile Enhancement of Mid-Air Ultrasonic Stimulation by Wrist Vibration",
        authors: "Dong-Geun Kim and Seungmoon Choi",
        venue: "Proceedings of Korea Haptics Conference",
        link: "",
        pdf: ""
    },
    {
        type: "poster_dom",
        year: 2024,
        title: "Investigating the Luxuriousness of Haptic Warning on the Steering Wheel",
        authors: "Jeongwoo Kim, Jungeun Lee, Dong-Geun Kim, Ki-Min Kwon, Beomyoung Chung, Junseong Park, Taeuk Kang, Sangji Moon, Wonseok Leee, Sung H. Han, and Seungmoon Choi",
        venue: "Spring Conference, The Acoustical Society of Korea",
        link: "",
        pdf: ""
    }
];

// 2. 탭 기능 및 논문 렌더링 실행
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

    // 논문 렌더링 실행
    renderPublications();
});

// 3. 논문 렌더링 함수
function renderPublications() {
    console.log("Rendering Publications..."); // 디버깅용 로그

    const categories = [
        { type: 'journal', id: 'journal-list', prefix: 'J' },
        { type: 'conf_intl', id: 'conf-intl-list', prefix: 'C' },
        { type: 'poster_intl', id: 'poster-intl-list', prefix: 'PDA' },
        { type: 'conf_dom', id: 'conf-dom-list', prefix: 'DC' },
        { type: 'poster_dom', id: 'poster-dom-list', prefix: 'DP' }
    ];

    categories.forEach(cat => {
        const listElement = document.getElementById(cat.id);
        if (!listElement) {
            console.warn(`Element with id ${cat.id} not found.`);
            return;
        }

        const filteredPapers = papers
            .filter(p => p.type === cat.type)
            .sort((a, b) => b.year - a.year);

        listElement.innerHTML = filteredPapers.map((paper, index) => {
            // 최신순이므로 번호는 전체 개수에서 index를 빼거나, 그냥 1부터 매길 수 있음
            // 여기서는 최신순으로 J1, J2... (index + 1) 사용
            const number = `${cat.prefix}${index + 1}`;

            // 이름 볼드 처리
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
