const input = document.querySelector('#article-search');
if (input) {
  const normalize = value => value.toLocaleLowerCase('vi').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd');
  const cards = [...document.querySelectorAll('[data-search]')];
  const buttons = [...document.querySelectorAll('[data-category-filter]')];
  const regionPanel = document.querySelector('#region-filters');
  const regionOptions = document.querySelector('#region-options');
  const empty = document.querySelector('#search-empty');
  const reset = document.querySelector('#clear-filters');
  const regions = [...new Set(cards.map(card => card.dataset.region).filter(Boolean))];
  // Only offer places that have a dedicated page in the current content list.
  regions.forEach(name => {
    const button = document.createElement('button');
    button.type = 'button'; button.dataset.regionFilter = name;
    button.textContent = name; button.setAttribute('aria-pressed', 'false');
    regionOptions.append(button);
  });
  const regionButtons = [...regionOptions.querySelectorAll('button')];
  const params = new URLSearchParams(window.location.search);
  const requestedTopic = params.get('chu-de') || '';
  const legacyCategories = {'Bảng giá':'bang-gia','Khu vực':'khu-vuc'};
  let category = buttons.some(button => button.dataset.categoryFilter === params.get('loai')) ? params.get('loai') : '';
  let region = regions.includes(params.get('khu-vuc')) ? params.get('khu-vuc') : '';
  if (region) category = 'khu-vuc';
  // Existing topic links from article pages remain usable.
  if (regions.includes(requestedTopic)) { category = 'khu-vuc'; region = requestedTopic; }
  else if (legacyCategories[requestedTopic]) category = legacyCategories[requestedTopic];
  input.value = params.get('q') || (requestedTopic && !regions.includes(requestedTopic) && !legacyCategories[requestedTopic] ? requestedTopic : '');
  const applyFilter = () => {
    const query = normalize(input.value.trim()); let count = 0;
    cards.forEach(card => {
      card.hidden = !(normalize(card.dataset.search).includes(query) && (!category || card.dataset.category === category) && (!region || card.dataset.region === region));
      if (!card.hidden) count++;
    });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.categoryFilter === category)));
    regionButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.regionFilter === region)));
    regionPanel.hidden = category !== 'khu-vuc';
    empty.hidden = count > 0;
    reset.hidden = !category && !region && !input.value;
    document.querySelector('#search-status').textContent = count ? `${count} nội dung${region ? ' tại ' + region : ''}` : 'Không tìm thấy nội dung';
    ['dich-vu', 'khu-vuc', 'bai-viet'].forEach(id => {
      const section = document.getElementById(id);
      if (section) {
        section.hidden = ![...section.querySelectorAll('.card')].some(card => !card.hidden);
        const categoryLink = document.querySelector('.news-search a[href="#' + id + '"]');
        if (categoryLink) categoryLink.hidden = section.hidden;
      }
    });
  };
  const rememberFilters = () => {
    const url = new URL(window.location.href);
    url.searchParams.delete('chu-de');
    if (category) url.searchParams.set('loai', category); else url.searchParams.delete('loai');
    if (region) url.searchParams.set('khu-vuc', region); else url.searchParams.delete('khu-vuc');
    if (input.value.trim()) url.searchParams.set('q', input.value.trim()); else url.searchParams.delete('q');
    window.history.replaceState(null, '', url);
  };
  input.addEventListener('input', () => { applyFilter(); rememberFilters(); });
  buttons.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.categoryFilter; region = ''; applyFilter(); rememberFilters();
  }));
  regionButtons.forEach(button => button.addEventListener('click', () => {
    region = button.dataset.regionFilter; applyFilter(); rememberFilters();
  }));
  reset.addEventListener('click', () => {
    category = ''; region = ''; input.value = ''; applyFilter(); rememberFilters(); input.focus();
  });
  applyFilter();
}
document.querySelectorAll('a[href="tel:0985666044"], a[href="https://zalo.me/0985666044"]').forEach(link => {
 link.addEventListener('click', () => {
  if (typeof gtag === 'function') {
   gtag('event', 'conversion', {send_to:'AW-18148925849/knAqCJfnh6wcEJnDis5D'});
   gtag('event', 'conversion', {send_to:'AW-17783643653/SVzMCJn6lrscEIW8859C',value:1.0,currency:'VND'});
  }
 });
});
