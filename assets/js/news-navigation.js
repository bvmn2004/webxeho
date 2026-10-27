const menuButton = document.getElementById('hamburger');
const mobileNavigation = document.getElementById('mobile-menu-placeholder');
if (menuButton && mobileNavigation) {
  const closeMenu = () => {
    mobileNavigation.classList.add('hidden');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Mở menu');
  };
  menuButton.addEventListener('click', () => {
    const expanded = !mobileNavigation.classList.toggle('hidden');
    menuButton.setAttribute('aria-expanded', String(expanded));
    menuButton.setAttribute('aria-label', expanded ? 'Đóng menu' : 'Mở menu');
  });
  mobileNavigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      menuButton.focus();
    }
  });
}
