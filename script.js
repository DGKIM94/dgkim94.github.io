'use strict';
(() => {
  const rows = [...document.querySelectorAll('.publication-row')];
  const search = document.querySelector('#paper-search');
  const year = document.querySelector('#paper-year');
  const chips = [...document.querySelectorAll('.filter-chip')];
  let type = 'all';
  document.querySelector('.publication-toolbar').hidden = false;
  const text = new Map(rows.map(row => [row, row.textContent.toLocaleLowerCase()]));
  function filter() {
    const query = search.value.trim().toLocaleLowerCase();
    let count = 0;
    rows.forEach(row => {
      const category = row.dataset.type;
      const matchType = type === 'all' || category === type || (type === 'conference' && category.startsWith('conf_')) || (type === 'poster' && category.startsWith('poster_'));
      const match = matchType && (year.value === 'all' || row.dataset.year === year.value) && text.get(row).includes(query);
      row.hidden = !match;
      if (match) count++;
    });
    document.querySelector('#result-count').textContent = `${count} publication${count === 1 ? '' : 's'}`;
    document.querySelector('.empty-state').hidden = count > 0;
  }
  chips.forEach(button => button.addEventListener('click', () => {
    type = button.dataset.type;
    chips.forEach(chip => {
      chip.classList.toggle('active', chip === button);
      chip.setAttribute('aria-pressed', String(chip === button));
    });
    filter();
  }));
  search.addEventListener('input', filter);
  year.addEventListener('change', filter);
  document.querySelectorAll('.authors').forEach(element => {
    const parts = element.textContent.split(/(Dong-Geun Kim|DG Kim|김동근)/g);
    element.replaceChildren(...parts.map((part, i) => {
      if (i % 2 === 0) return document.createTextNode(part);
      const strong = document.createElement('strong'); strong.textContent = part; return strong;
    }));
  });
  const time = document.querySelector('.sync-caption time');
  if (time && Date.now() - new Date(time.dateTime).getTime() > 21 * 86400000) document.querySelector('.stale-note').hidden = false;
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) document.querySelectorAll('nav a').forEach(link => {
        const active = link.hash === `#${entry.target.id}`;
        link.classList.toggle('active', active);
        if (active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
      });
    }), {rootMargin: '-15% 0px -65% 0px'});
    document.querySelectorAll('section[id]').forEach(section => observer.observe(section));
  }
})();
