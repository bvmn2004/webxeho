"""Render the 29 editorial pages and news hub from content/pages.json using their existing shells.

Python standard library only. Does not touch index.html, booking code or styling.
Run without arguments to render; use --check to detect stale generated pages.
"""
from pathlib import Path
import argparse, html, json, re, sys, xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://laixehodanang.me/'
REGIONS = {
    'lai-xe-ho-hai-chau-da-nang.html': 'Hải Châu',
    'lai-xe-ho-son-tra-da-nang.html': 'Sơn Trà',
    'lai-xe-ho-cam-le-da-nang.html': 'Cẩm Lệ – Hòa Xuân',
    'lai-xe-ho-thanh-khe-da-nang.html': 'Thanh Khê',
    'lai-xe-ho-ngu-hanh-son-da-nang.html': 'Ngũ Hành Sơn',
    'lai-xe-ho-lien-chieu-da-nang.html': 'Liên Chiểu',
}
SERVICES = {
    'lai-xe-ho-o-to-da-nang.html', 'lai-xe-ho-xe-may-da-nang.html',
    'lai-xe-ho-sau-tiec-da-nang.html', 'dat-tai-xe-lai-ho-ban-dem-da-nang.html',
    'thue-tai-xe-theo-gio-da-nang.html', 'thue-tai-xe-theo-ngay-da-nang.html',
    'thue-tai-xe-di-tinh-da-nang.html', 'thue-tai-xe-da-nang-di-hoi-an.html',
    'thue-tai-xe-da-nang-di-hue.html', 'thue-tai-xe-dua-don-doi-tac-da-nang.html',
    'tai-xe-phuc-vu-tiec-cuoi-su-kien-da-nang.html',
}

FLOATING_CONTACT = """  <div id="floating-contact">

    <!-- Facebook -->
    <a href="https://facebook.com/profile.php?id=61583832241506" target="_blank" rel="noopener noreferrer" class="fc-btn fb-btn" aria-label="Facebook Như Ý Driver" title="Facebook Như Ý Driver">

      <div class="ripple-circle"></div>
      <div class="ripple-fill"></div>

      <svg xmlns="http://www.w3.org/2000/svg" fill="#fff" width="26" height="26" viewBox="0 0 24 24" aria-hidden="true">
        <path
          d="M22 12a10 10 0 1 0-11.5 9.9v-7h-2v-3h2v-2.3c0-2 1.2-3.1 3-3.1.9 0 1.8.1 1.8.1v2h-1c-1 0-1.3.6-1.3 1.2V12h2.3l-.4 3h-1.9v7A10 10 0 0 0 22 12" />
      </svg>
    </a>

    <!-- Zalo (TRACKING) -->
    <a href="https://zalo.me/0985666044" class="fc-btn zalo-btn"
      onclick="return gtag_report_conversion('https://zalo.me/0985666044');" aria-label="Liên hệ Như Ý Driver qua Zalo" title="Chat Zalo Như Ý Driver">

      <div class="ripple-circle"></div>
      <div class="ripple-fill"></div>

      <img src="assets/images/zalo-icon.svg" width="30" height="30" alt="" class="zalo-icon-img">
    </a>

    <!-- Phone (TRACKING) -->
    <a href="tel:0985666044" class="fc-btn call-btn" onclick="return gtag_report_conversion('tel:0985666044');" aria-label="Gọi Như Ý Driver 0985 666 044" title="Gọi hotline">

      <div class="ripple-circle"></div>
      <div class="ripple-fill"></div>

      <svg xmlns="http://www.w3.org/2000/svg" fill="#fff" width="26" height="26" viewBox="0 0 24 24" aria-hidden="true">
        <path
          d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.3 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V21c0 .6-.4 1-1 1A19 19 0 0 1 3 5c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.5.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z" />
      </svg>
    </a>

  </div>"""

CONVERSION_SCRIPT = """  <!-- Conversion snippet: Gọi khi click Zalo/Phone trực tiếp với fallback an toàn -->
  <script>
    function gtag_report_conversion(url) {
      var navigated = false;
      var callback = function () {
        if (!navigated && typeof (url) != 'undefined' && url) {
          navigated = true;
          window.location = url;
        }
      };
      setTimeout(callback, 500);
      if (typeof gtag === 'function') {
        // Tài khoản 1: có event_callback để điều hướng sau khi conversion ghi nhận
        gtag('event', 'conversion', {
          'send_to': 'AW-18148925849/knAqCJfnh6wcEJnDis5D',
          'event_callback': callback
        });
        // Tài khoản 2: thêm value + currency theo snippet Google Ads cấp
        gtag('event', 'conversion', {
          'send_to': 'AW-17783643653/SVzMCJn6lrscEIW8859C',
          'value': 1.0,
          'currency': 'VND'
        });
      } else {
        callback();
      }
      return false;
    }
  </script>"""

CANONICAL_HEADER = """  <header class="bg-gray-light sticky top-0 z-50 site-header">
    <div class="container mx-auto flex justify-between items-center py-4">
      <!-- Left section: Logo -->
      <div class="flex items-center">
        <img src="assets/images/logo-y.png" alt="Logo" class="h-14 w-auto mr-4">
      </div>

      <!-- Hamburger menu (for mobile) -->
      <div class="flex md:hidden">
        <button id="hamburger" class="text-white focus:outline-none" aria-label="Mở menu"
          aria-controls="mobile-menu-placeholder" aria-expanded="false">
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path>
          </svg>
        </button>
      </div>

      <!-- Center section: Menu -->
      <nav class="hidden md:flex md:flex-grow justify-center">
        <ul class="flex justify-center space-x-4 text-white ny-home-menu">
          <li><a href="/#home" class="hover:text-secondary font-bold">Trang Chủ</a></li>
          <li><a href="/#aboutus" class="hover:text-secondary font-bold">Giới Thiệu</a></li>
          <li><a href="/#portfolio" class="hover:text-secondary font-bold">Dịch Vụ</a></li>
          <li><a href="/#contact" class="hover:text-secondary font-bold">Liên Hệ</a></li>
          <li><a href="/tin-tuc.html" class="hover:text-secondary font-bold">Tin Tức</a></li>
        </ul>
      </nav>

      <!-- Right section: Buttons (for desktop) -->
      <div class="hidden lg:flex items-center space-x-4">
        <a href="/#quick-booking"
          class="bg-secondary hover:bg-primary text-white font-semibold px-4 py-2 rounded inline-block">Đặt Nhanh</a>
        <a href="https://zalo.me/0985666044"
          class="bg-primary hover:bg-secondary text-white font-semibold px-4 py-2 rounded inline-block">Zalo</a>
      </div>
    </div>
  </header>
  <!-- Mobile menu -->
  <nav id="mobile-menu-placeholder" class="mobile-menu hidden items-center space-y-8 md:hidden">
    <ul>
      <li><a href="/#home" class="hover:text-secondary font-bold">Trang Chủ</a></li>
      <li><a href="/#aboutus" class="hover:text-secondary font-bold">Giới Thiệu</a></li>
      <li><a href="/#portfolio" class="hover:text-secondary font-bold">Dịch Vụ</a></li>
      <li><a href="/#contact" class="hover:text-secondary font-bold">Liên Hệ</a></li>
      <li><a href="/tin-tuc.html" class="hover:text-secondary font-bold">Tin Tức</a></li>
    </ul>
    <div class="flex flex-col mt-6 space-y-2 items-center">
      <a href="/#quick-booking"
        class="bg-secondary hover:bg-primary text-white font-semibold px-4 py-2 rounded flex items-center justify-center min-w-[110px]">Đặt
        Nhanh</a>
      <a href="https://zalo.me/0985666044"
        class="bg-primary hover:bg-secondary text-white font-semibold px-4 py-2 rounded flex items-center justify-center min-w-[110px]">Zalo</a>
    </div>
  </nav>"""

CANONICAL_FOOTER = """  <footer class="bg-white text-gray-light py-16">
    <div class="container mx-auto grid grid-cols-1 md:grid-cols-4 gap-10">

      <!-- COLUMN 1: THÔNG TIN LIÊN HỆ -->
      <div class="text-center md:text-left">
        <h3 class="text-lg font-bold mb-4">Thông Tin Liên Hệ</h3>
        <ul class="space-y-2 text-sm">
          <li class="font-semibold text-base">Dịch vụ Lái Xe Hộ Đà Nẵng – Như Ý Driver</li>
          <li>Địa chỉ: 59 Khương Hữu Dụng - Hoà Xuân - Cẩm Lệ - Đà Nẵng</li>
          <li>
            Hotline:
            <a href="tel:0985666044" class="text-blue-400 hover:text-blue-300 font-bold">
              0985 666 044
            </a>
          </li>
          <li>
            Email:
            <a href="mailto:laixehodanangnhuydriver@gmail.com" class="text-blue-400 hover:text-blue-300 font-bold">
              laixehodanangnhuydriver@gmail.com
            </a>
          </li>
        </ul>
      </div>

      <!-- COLUMN 2: KHU VỰC PHỤC VỤ -->
      <div class="text-center md:text-left">
        <h3 class="text-lg font-bold mb-4">Khu Vực Phục Vụ</h3>
        <ul class="space-y-2 text-sm">
          <li><a href="khu-vuc-phuc-vu.html" class="hover:text-primary transition">Khu vực phục vụ Đà Nẵng</a></li>
          <li><a href="lai-xe-ho-hai-chau-da-nang.html" class="hover:text-primary transition">Lái xe hộ Hải Châu</a></li>
          <li><a href="lai-xe-ho-son-tra-da-nang.html" class="hover:text-primary transition">Lái xe hộ Sơn Trà</a></li>
          <li><a href="lai-xe-ho-ngu-hanh-son-da-nang.html" class="hover:text-primary transition">Lái xe hộ Ngũ Hành Sơn</a></li>
          <li><a href="lai-xe-ho-thanh-khe-da-nang.html" class="hover:text-primary transition">Lái xe hộ Thanh Khê</a></li>
          <li><a href="lai-xe-ho-cam-le-da-nang.html" class="hover:text-primary transition">Lái xe hộ Cẩm Lệ – Hoà Xuân</a></li>
          <li><a href="lai-xe-ho-lien-chieu-da-nang.html" class="hover:text-primary transition">Lái xe hộ Liên Chiểu</a></li>
        </ul>
      </div>

      <!-- COLUMN 3: DỊCH VỤ HỖ TRỢ -->
      <div class="text-center md:text-left">
        <h3 class="text-lg font-bold mb-4">Dịch Vụ Hỗ Trợ</h3>
        <ul class="space-y-2 text-sm mb-6">
          <li><a href="bang-gia-lai-xe-ho-da-nang.html" class="hover:text-primary transition">Bảng giá lái xe hộ</a></li>
          <li><a href="lai-xe-ho-o-to-da-nang.html" class="hover:text-primary transition">Lái xe hộ ô tô</a></li>
          <li><a href="lai-xe-ho-xe-may-da-nang.html" class="hover:text-primary transition">Lái xe hộ xe máy</a></li>
          <li><a href="lai-xe-ho-sau-tiec-da-nang.html" class="hover:text-primary transition">Lái xe hộ sau tiệc</a></li>
          <li><a href="thue-tai-xe-theo-gio-da-nang.html" class="hover:text-primary transition">Thuê tài xế theo giờ</a></li>
          <li><a href="thue-tai-xe-theo-ngay-da-nang.html" class="hover:text-primary transition">Thuê tài xế theo ngày</a></li>
          <li><a href="thue-tai-xe-di-tinh-da-nang.html" class="hover:text-primary transition">Thuê tài xế đi tỉnh</a></li>
          <li><a href="tin-tuc.html" class="hover:text-primary transition">Tin tức & cẩm nang</a></li>
        </ul>

        <!-- SOCIAL + LOGO -->
        <img src="assets/images/logo-y.png" alt="Như Ý Driver" class="h-16 w-auto mb-4 mx-auto md:mx-0">

        <div class="flex items-center justify-center md:justify-start space-x-4">
          <a href="https://www.facebook.com/profile.php?id=61583832241506" target="_blank"
            class="hover:scale-110 transition">
            <img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" class="w-7 h-7">
          </a>

          <a href="https://www.tiktok.com/@trannhuy4781" target="_blank" class="hover:scale-110 transition">
            <img src="https://cdn-icons-png.flaticon.com/512/3046/3046121.png" class="w-7 h-7">
          </a>

          <a href="https://zalo.me/0985666044" target="_blank" class="hover:scale-110 transition">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Icon_of_Zalo.svg"
              class="w-7 h-7 bg-white rounded-full p-1">
          </a>
        </div>
      </div>

      <!-- COLUMN 4: FANPAGE + CREDIT -->
      <div class="flex flex-col items-center md:items-start">

        <!-- FANPAGE -->
        <div class="w-full mb-4">
          <iframe
            src="https://www.facebook.com/plugins/page.php?href=https%3A%2F%2Fwww.facebook.com%2Fprofile.php%3Fid%3D61583832241506&tabs=timeline&width=340&height=300&small_header=false&adapt_container_width=true&hide_cover=false&show_facepile=true"
            width="100%" height="300" style="border:none;overflow:hidden" scrolling="no" frameborder="0"
            allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share" allowfullscreen="true">
          </iframe>

        </div>

        <!-- CREDIT -->
        <p class="text-sm text-center md:text-left">
          © 2025 – Như Ý Driver<br>
          Thiết kế & vận hành bởi
          <a href="https://www.facebook.com/wall.miin" class="text-blue-400 hover:text-blue-300 font-bold">
            wall.miin
          </a>
        </p>

      </div>

    </div>
  </footer>"""

def set_or_insert_meta(source, attr_name, attr_val, content_val):
    pattern = r'(<meta\b[^>]*' + re.escape(attr_name) + r'="' + re.escape(attr_val) + r'"[^>]*\bcontent=")[^"]*("[^>]*>)'
    if re.search(pattern, source):
        return re.sub(pattern, lambda m: m[1] + html.escape(content_val, quote=True) + m[2], source, count=1)
    pattern2 = r'(<meta\b[^>]*\bcontent=")[^"]*("[^>]*' + re.escape(attr_name) + r'="' + re.escape(attr_val) + r'"[^>]*>)'
    if re.search(pattern2, source):
        return re.sub(pattern2, lambda m: m[1] + html.escape(content_val, quote=True) + m[2], source, count=1)
    tag = f'  <meta {attr_name}="{attr_val}" content="{html.escape(content_val, quote=True)}">\n'
    if '<link rel="canonical"' in source:
        return re.sub(r'(<link rel="canonical"[^>]*>\n?)', r'\1' + tag, source, count=1)
    return source.replace('</head>', tag + '</head>', 1)

def ensure_floating_contact(source):
    if '<div id="floating-contact">' in source:
        pattern = r'<div id="floating-contact">[\s\S]*?<!-- Phone.*?-->[\s\S]*?</a>\s*</div>'
        source = re.sub(pattern, FLOATING_CONTACT.strip(), source, count=1)
    else:
        pattern = r'(<body[^>]*>)'
        source = re.sub(pattern, r'\1\n\n' + FLOATING_CONTACT + '\n', source, count=1)
    return source

def ensure_conversion_script(source):
    pattern = r'<!-- Conversion snippet:[\s\S]*?</script>'
    if re.search(pattern, source):
        source = re.sub(pattern, CONVERSION_SCRIPT.strip(), source, count=1)
    return source

def ensure_canonical_header(source):
    pattern = r'<header\b[^>]*site-header[\s\S]*?<nav\b[^>]*id="mobile-menu-placeholder"[\s\S]*?</nav>'
    if re.search(pattern, source):
        source = re.sub(pattern, lambda m: CANONICAL_HEADER.strip(), source, count=1)
    source = re.sub(r'href="(?:index\.html)?#quick-booking"', 'href="/#quick-booking"', source)
    return source

def ensure_canonical_footer(source):
    pattern = r'<footer\b[^>]*>[\s\S]*?</footer>'
    if re.search(pattern, source):
        source = re.sub(pattern, lambda m: CANONICAL_FOOTER.strip(), source, count=1)
    return source

def render_page(source, page):
    source = re.sub(r'<title>.*?</title>', lambda m: '<title>' + html.escape(page['title']) + '</title>', source, count=1, flags=re.S)
    source = set_or_insert_meta(source, 'name', 'description', page['description'])
    source = set_or_insert_meta(source, 'name', 'robots', 'index, follow')
    source = set_or_insert_meta(source, 'name', 'author', 'Như Ý Driver')
    source = set_or_insert_meta(source, 'property', 'og:site_name', 'Như Ý Driver')
    source = set_or_insert_meta(source, 'property', 'og:title', page['title'])
    source = set_or_insert_meta(source, 'property', 'og:description', page['description'])
    source = set_or_insert_meta(source, 'property', 'og:url', BASE + page['file'])
    source = set_or_insert_meta(source, 'property', 'og:image', BASE + page['hero_src'])
    source = set_or_insert_meta(source, 'property', 'og:type', 'article' if page.get('article', False) else 'website')
    source = set_or_insert_meta(source, 'property', 'og:locale', 'vi_VN')
    source = set_or_insert_meta(source, 'name', 'twitter:card', 'summary_large_image')
    source = set_or_insert_meta(source, 'name', 'twitter:title', page['title'])
    source = set_or_insert_meta(source, 'name', 'twitter:description', page['description'])
    source = set_or_insert_meta(source, 'name', 'twitter:image', BASE + page['hero_src'])
    source = re.sub(r'<link rel="canonical" href="[^"]+">', lambda m: '<link rel="canonical" href="' + BASE + page['file'] + '">', source, count=1)
    source = re.sub(r'<h1>.*?</h1>', lambda m: '<h1>' + html.escape(page['h1']) + '</h1>', source, count=1, flags=re.S)
    source = re.sub(r'<p class="lead">.*?</p>', lambda m: '<p class="lead">' + html.escape(page['intro']) + '</p>', source, count=1, flags=re.S)
    source = re.sub(r'(<img\b[^>]*src="' + re.escape(page['hero_src']) + r'"[^>]*alt=")[^"]*', lambda m: m[1] + html.escape(page['hero_alt'], quote=True), source, count=1)

    start = source.index('<div class="reading">') + len('<div class="reading">')
    end = source.rfind('</div>', start, source.index('</main>', start))
    if end < start:
        raise ValueError('Missing reading container')
    source = source[:start] + page['body_html'] + source[end:]

    def schema(match):
        data = json.loads(match[1])
        if data.get('@type') == 'Article':
            data['headline'] = page['h1']
            data['description'] = page['description']
            data['dateModified'] = page['modified']
            data['image'] = [BASE + page['hero_src']]
            data['mainEntityOfPage'] = {'@type': 'WebPage', '@id': BASE + page['file']}
        elif data.get('@type') == 'BreadcrumbList':
            data['itemListElement'][-1]['name'] = page['h1']
        return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'
    source = re.sub(r'<script type="application/ld\+json">(.*?)</script>', schema, source, flags=re.S)

    source = ensure_conversion_script(source)
    source = ensure_floating_contact(source)
    source = ensure_canonical_header(source)
    source = ensure_canonical_footer(source)
    return source

def render_hub(source, pages):
    by_file = {p['file']: p for p in pages}
    def update(match):
        card = match[0]
        target = re.search(r'class="card-image-link"\s+href="([^"]+)"', card)
        if not target or target[1] not in by_file:
            raise ValueError('Unknown news-card target')
        p = by_file[target[1]]
        topics = re.search(r'data-topics="([^"]*)"', card)[1]
        category = ('bang-gia' if p['file'] == 'bang-gia-lai-xe-ho-da-nang.html' else
                    'khu-vuc' if p['file'] in REGIONS or p['file'] == 'khu-vuc-phuc-vu.html' else
                    'dich-vu' if p['file'] in SERVICES else 'bai-viet')
        card = re.sub(r' data-(?:category|region)="[^"]*"', '', card)
        card = card.replace('<article class="card"', '<article class="card" data-category="' + category + '" data-region="' + html.escape(REGIONS.get(p['file'], ''), quote=True) + '"', 1)
        body_text = html.unescape(re.sub(r'<[^>]+>', ' ', p['body_html']))
        search = ' '.join((p['h1'] + ' ' + p['intro'] + ' ' + html.unescape(topics).replace('|', ' ') + ' ' + body_text).split())
        card = re.sub(r'data-search="[^"]*"', lambda m: 'data-search="' + html.escape(search, quote=True) + '"', card, count=1)
        card = re.sub(r'(<h3><a href="[^"]+">).*?(</a></h3>)', lambda m: m[1] + html.escape(p['h1']) + m[2], card, count=1, flags=re.S)
        card = re.sub(r'<p>.*?</p>', lambda m: '<p>' + html.escape(p['intro']) + '</p>', card, count=1, flags=re.S)
        card = re.sub(r'(<img\b[^>]*alt=")[^"]*', lambda m: m[1] + html.escape(p['hero_alt'], quote=True), card, count=1)
        return card
    source = re.sub(r'<article class="card"[^>]*>.*?</article>', update, source, flags=re.S)

    cards = re.findall(r'<article class="card"[^>]*>.*?</article>', source, re.S)
    for section, categories in [('dich-vu', {'bang-gia', 'dich-vu'}), ('khu-vuc', {'khu-vuc'}), ('bai-viet', {'bai-viet'})]:
        selected = ''.join(card for card in cards if re.search(r'data-category="([^"]+)"', card)[1] in categories)
        pattern = r'(<section id="' + section + r'"[^>]*>.*?<div class="cards">).*?(</div>\s*</section>)'
        source, count = re.subn(pattern, lambda m: m[1] + selected + m[2], source, count=1, flags=re.S)
        if count != 1:
            raise ValueError('Missing news category section: ' + section)

    hub_title = 'Tin Tức Lái Xe Hộ Đà Nẵng – Cẩm Nang, Bảng Giá & Kinh Nghiệm Đi Xe | Như Ý Driver'
    hub_desc = 'Cập nhật tin tức lái xe hộ Đà Nẵng, bảng giá dịch vụ mới nhất, kinh nghiệm lái xe an toàn và hướng dẫn đặt tài xế Như Ý Driver nhanh chóng.'
    source = re.sub(r'<title>.*?</title>', '<title>' + html.escape(hub_title) + '</title>', source, count=1, flags=re.S)
    source = set_or_insert_meta(source, 'name', 'description', hub_desc)
    source = set_or_insert_meta(source, 'name', 'robots', 'index, follow')
    source = set_or_insert_meta(source, 'name', 'author', 'Như Ý Driver')
    source = set_or_insert_meta(source, 'property', 'og:site_name', 'Như Ý Driver')
    source = set_or_insert_meta(source, 'property', 'og:title', 'Tin Tức Lái Xe Hộ Đà Nẵng – Như Ý Driver')
    source = set_or_insert_meta(source, 'property', 'og:description', hub_desc)
    source = set_or_insert_meta(source, 'property', 'og:url', BASE + 'tin-tuc.html')
    source = set_or_insert_meta(source, 'property', 'og:image', BASE + 'assets/images/og-image.png')
    source = set_or_insert_meta(source, 'property', 'og:type', 'website')
    source = set_or_insert_meta(source, 'property', 'og:locale', 'vi_VN')
    source = set_or_insert_meta(source, 'name', 'twitter:card', 'summary_large_image')
    source = set_or_insert_meta(source, 'name', 'twitter:title', 'Tin Tức Lái Xe Hộ Đà Nẵng – Như Ý Driver')
    source = set_or_insert_meta(source, 'name', 'twitter:description', hub_desc)
    source = set_or_insert_meta(source, 'name', 'twitter:image', BASE + 'assets/images/og-image.png')

    source = ensure_conversion_script(source)
    source = ensure_floating_contact(source)
    source = ensure_canonical_header(source)
    source = ensure_canonical_footer(source)
    return source

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()

    pages = json.loads((ROOT / 'content/pages.json').read_text(encoding='utf-8'))['pages']
    if len(pages) != 29:
        raise ValueError('Expected the 29 existing detail pages')

    results = {}
    for p in pages:
        path = ROOT / p['file']
        if path.parent != ROOT or p['file'] == 'index.html' or not path.is_file():
            raise ValueError('Invalid existing page')
        old = path.read_text(encoding='utf-8')
        new = render_page(old, p)
        if new != old:
            results[path] = new

    hub = ROOT / 'tin-tuc.html'
    old = hub.read_text(encoding='utf-8')
    new = render_hub(old, pages)
    if new != old:
        results[hub] = new

    site = ROOT / 'sitemap.xml'
    old = site.read_text(encoding='utf-8')
    tree = ET.fromstring(old)
    ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    dates = {BASE + p['file']: p['modified'] for p in pages}
    dates[BASE + 'tin-tuc.html'] = '2026-10-30'
    for node in tree.findall(ns + 'url'):
        loc = node.find(ns + 'loc')
        if loc.text in dates:
            last = node.find(ns + 'lastmod')
            if last is None:
                last = ET.SubElement(node, ns + 'lastmod')
            last.text = dates[loc.text]
    ET.register_namespace('', ns[1:-1])
    new = '<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(tree, encoding='unicode') + '\n'
    if new != old:
        results[site] = new

    if args.check:
        if results:
            print('Stale outputs: ' + ', '.join(p.name for p in results))
            return 1
        print('PASS: all 29 detail pages, news previews and sitemap match the content source.')
        return 0

    for path, new in results.items():
        path.write_text(new, encoding='utf-8')
    print('Rendered ' + str(len(results)) + ' changed files from content/pages.json.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
