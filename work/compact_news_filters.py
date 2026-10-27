from pathlib import Path
import re
p=Path('tin-tuc.html')
s=p.read_text(encoding='utf-8')
markup='''<section class="news-search" id="noi-dung">
<h2>Tìm nội dung bạn cần</h2>
<label for="article-search">Tìm bảng giá, dịch vụ hoặc bài viết</label>
<input id="article-search" type="search" placeholder="Ví dụ: bảng giá, xe máy, bàn giao…" aria-controls="dich-vu khu-vuc bai-viet">
<div class="topic-filters primary-filters" role="group" aria-label="Lọc nội dung">
<button type="button" data-category-filter="" aria-pressed="true">Tất cả</button>
<button type="button" data-category-filter="bang-gia" aria-pressed="false">Bảng giá</button>
<button type="button" data-category-filter="dich-vu" aria-pressed="false">Dịch vụ</button>
<button type="button" data-category-filter="khu-vuc" aria-pressed="false" aria-controls="region-filters">Khu vực</button>
<button type="button" data-category-filter="bai-viet" aria-pressed="false">Bài viết &amp; hướng dẫn</button>
</div>
<div id="region-filters" class="region-filters" hidden>
<p>Chọn khu vực</p><div id="region-options" class="topic-filters" role="group" aria-label="Lọc theo khu vực"><button type="button" data-region-filter="" aria-pressed="true">Tất cả khu vực</button></div>
</div>
<div class="filter-status"><p id="search-status" role="status" aria-live="polite" aria-atomic="true">29 nội dung</p><button id="clear-filters" type="button" hidden>Xóa bộ lọc</button></div>
<div id="search-empty" class="search-empty" hidden><p>Hãy thử từ khóa khác hoặc xóa bộ lọc để xem tất cả nội dung.</p></div>
</section>'''
s,n=re.subn(r'<section class="news-search".*?</section>',lambda m:markup,s,count=1,flags=re.S)
assert n==1
p.write_text(s,encoding='utf-8')
