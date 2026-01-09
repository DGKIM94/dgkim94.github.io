document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab-btn');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // 모든 탭 비활성화
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));

            // 클릭된 탭 활성화
            tab.classList.add('active');

            // 연결된 컨텐츠 보여주기
            const targetId = tab.getAttribute('data-target');
            document.querySelector(targetId).classList.add('active');
        });
    });
});
