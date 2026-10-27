from pathlib import Path
import json

manifest=json.loads(Path('work/new-content-manifest.json').read_text(encoding='utf-8'))
gen=json.loads(Path('work/generated-area-manifest.json').read_text(encoding='utf-8'))
supplied=json.loads(Path('work/new-source-assets.json').read_text(encoding='utf-8'))
uniforms=json.loads(Path('work/uniform-assets.json').read_text(encoding='utf-8'))
qa=json.loads(Path('work/qa-new-content.json').read_text(encoding='utf-8'))
text='''# Báo cáo bổ sung khu vực và bài viết — Như Ý Driver

Đã lưu tại `D:\\MINHNGUYET\\webxeho`. Không commit, push, deploy hoặc sửa website đang chạy. Các thay đổi chưa commit từ những lượt trước được giữ nguyên.

## Kết quả chính

- Tạo 6 trang khu vực hoàn chỉnh và 4 bài hướng dẫn mới, giữ nguyên trang chủ và các URL cũ.
- Tin Tức hiện có 29 thẻ nội dung trong HTML; thêm nhóm khu vực, thẻ chủ đề và tìm kiếm có dấu/không dấu. Cả ảnh lẫn tiêu đề/nút đều mở đúng trang chi tiết.
- Trang khu vực tổng hợp có liên kết tới 6 trang riêng và 3 ảnh người mặc đồng phục do chủ website cung cấp.
- 4 ảnh minh họa mới đã đổi sang khuôn mặt trong ảnh Anh_Anh_Y, dùng đúng gile đỏ, polo đen hoặc áo khoác đen theo mẫu. Không dùng các bản nháp với người mẫu khác.
- Các trang mới dùng nguyên header, menu điện thoại và footer của index; chỉ đổi đường dẫn neo để về đúng phần của trang chủ.
- Sitemap có 31 URL: trang chủ và 30 trang nội dung. Robots vẫn cho phép thu thập.

## Trang khu vực mới

| Trang | Điểm riêng của nội dung |
|---|---|
'''
for d in manifest['areas']:
 text+=f'| [{d["name"]}](http://127.0.0.1:5500/{d["slug"]}.html) — `{d["slug"]}.html` | '+ '; '.join(t for t,b in d['focus'])+' |\n'
text+='''
Các khu vực đã được liệt kê trong website trước khi thực hiện. Không tạo chi nhánh hoặc địa chỉ mới. Nội dung riêng dựa trên cách định vị, bàn giao và nhu cầu cụ thể; không chỉ thay tên khu vực trên cùng một bài.

Cẩm Lệ và Hòa Xuân được gộp trong một trang như yêu cầu. Dùng “khu vực” trong tiêu đề để tránh mặc định địa giới quận trước đây vẫn là phạm vi hiện tại. Tên địa danh được đối chiếu [nguồn Chính phủ về sắp xếp địa danh](https://xaydungchinhsach.chinhphu.vn/toan-van-nghi-quyet-so-1659-nq-ubtvqh15-sap-xep-cac-dvhc-cap-xa-cua-thanh-pho-da-nang-nam-2025-119250616202714604.htm). Không tạo danh sách điểm đón hay tuyến đường được khẳng định sẵn có.

## Bài hướng dẫn mới

'''
for d in manifest['articles']:
 text+=f'- **{d["title"]}** — `{d["slug"]}.html`. '+d['desc']+'\n'
text+='''
Các bài Hội An và Huế tập trung vào kế hoạch chuyến, điểm nhận/trả, lượt về, thời gian chờ và báo giá; không công bố chi phí hay giờ chạy cố định. Hai bài không lặp lại trang dịch vụ đi tỉnh, mà liên kết đến đó.

Bài đưa đón đối tác tập trung vào ba vai trò: người đặt, người giao xe và hành khách. Bài tiệc cưới/sự kiện tập trung vào danh sách từng xe, giờ nhận, điểm trả và người điều phối. Không tuyên bố có sẵn đội xe, tài xế ngoại ngữ hoặc đủ người nhận nhiều xe cùng lúc.

## Nội dung gộp/cập nhật

- Bổ sung mục “Nên hỏi gì về trách nhiệm trước khi bàn giao?” vào `can-chuan-bi-gi-khi-ban-giao-xe.html`, thêm link trong mục lục. Không tạo một bài trùng ý định tìm kiếm.
- Mục bổ sung hướng dẫn hỏi đầu mối xử lý, ghi nhận tình trạng xe và điều kiện sử dụng. Không đặt chính sách bảo hiểm/bồi thường hay quyết định trách nhiệm pháp lý của các bên.
- Cập nhật `khu-vuc-phuc-vu.html` bằng 6 thẻ khu vực, liên kết và phần nhận diện đồng phục.
- Cập nhật `tin-tuc.html` bằng 10 thẻ mới, nhóm khu vực, bộ lọc địa bàn/chủ đề và tìm kiếm.

## Danh sách tệp của lượt này

10 tệp HTML mới được liệt kê ở trên.

Tệp đã sửa: `khu-vuc-phuc-vu.html`, `tin-tuc.html`, `can-chuan-bi-gi-khi-ban-giao-xe.html`, `sitemap.xml`, `assets/css/news-content.css`, `assets/js/content.js`.

Tệp/tài nguyên thêm: 6 ảnh WebP từ ảnh bài viết/khu vực đã có, 4 ảnh minh họa WebP mới, 6 bản WebP đồng phục trong `assets/images/team/`. Các tệp ở `work/` là nguồn tạo nội dung, kiểm tra, manifest ảnh và ảnh chụp QA; không cần đưa thư mục work lên GitHub Pages.

Trang chủ, `booking.js`, `script.js`, CSS cũ, `CNAME`, `robots.txt`, `package.json` và tệp xác minh Google đã được so hash với đầu lượt này: không đổi. Giữ các mã Analytics/Ads hiện có; trang mới nạp cùng các mã đó. Không sửa công thức giá.

## Ảnh từ thư mục đã có

| Nguồn | Bản dùng trong dự án | Dung lượng |
|---|---|---|
'''
for key,v in supplied.items():
 text+=f'| {Path(v["src"]).name} | `{v["output"]}` | {v["bytes"]:,} byte |\n'
text+='''
Đã đọc được toàn bộ 6 ảnh nguồn cần cho các trang mới: Hải Châu, Sơn Trà, đối tác, sự kiện, Hội An và Huế. Không thiếu tệp nào trong nhóm này. Chúng là ảnh chủ website cung cấp, giữ nguyên nội dung, tỷ lệ và chữ; chỉ tạo bản WebP, không sửa/xóa PNG nguồn.

## Ảnh mới được chọn

| Khu vực | Tệp WebP trong dự án | Tham chiếu nhân vật | Dung lượng |
|---|---|---|---|
'''
for key,v in gen.items():
 text+=f'| {key} | `{v["output"]}` | `{Path(v["reference"]).name}` | {v["bytes"]:,} byte |\n'
text+='''
Tổng 4 ảnh khoảng 616 KB. Tạo bằng công cụ image_gen tích hợp (không dùng CLI). Ảnh cuối đã được mở kiểm tra khuôn mặt, trang phục, bố cục và các chi tiết chính. Ảnh được ghi rõ là minh họa tạo bằng AI trên trang, không là bằng chứng ảnh chụp tại địa chỉ hoặc một chuyến đi thật. Logo/chữ nhỏ trên áo vẫn là chi tiết tổng hợp; ảnh mẫu gốc là nguồn đối chiếu chính xác.

Prompt cảnh, prompt chỉnh đúng nhân vật, đường dẫn ảnh tham chiếu và tệp kết quả được lưu trong `PROMPT-ANH-KHU-VUC.json` đi kèm báo cáo. Các PNG do công cụ tạo giữ ở thư mục generated_images ban đầu; không xóa bản nháp hay nguồn.

## Ảnh đồng phục

'''
for name,v in uniforms.items():text+=f'- `{name}` → `{v["output"]}`.\n'
text+='''
Ba ảnh Anh_Anh_Y mặc gile, polo, áo khoác được hiển thị tại trang khu vực tổng hợp. Ba ảnh mẫu áo được lưu làm tài nguyên tham chiếu, chưa chèn thêm vào các trang để tránh lặp và nặng nội dung. Giữ nguyên cả 6 PNG trong OneDrive.

## Những thông tin còn cần chủ dịch vụ xác nhận

1. Phạm vi nhận chuyến theo địa chỉ cụ thể và thời điểm ở từng khu vực; tên khu vực có sẵn không có nghĩa luôn có tài xế ở mọi điểm.
2. Khả năng nhận lịch đi Hội An/Huế, một chiều/khứ hồi, chờ và qua đêm. Các bài chỉ hướng dẫn liên hệ kiểm tra, chưa công bố lịch nhận mặc định.
3. Số xe/tài xế có thể bố trí cho một sự kiện, điều kiện đón đối tác, ngoại ngữ hoặc hỗ trợ ngoài việc lái.
4. Phí chờ, vượt giờ, ăn nghỉ, cầu đường, bãi xe, đổi/hủy lịch và các khoản bao gồm trong báo giá từng yêu cầu.
5. Quy trình xử lý sự cố, điều khoản bàn giao, bảo hiểm hoặc bồi thường nếu có. Không tự viết chính sách khi chưa có xác nhận.
6. Bảng giá xe máy ở các mốc ranh giới, cách cộng khi vượt 10 km và thời gian áp dụng phụ phí khuya vẫn nên được chủ dịch vụ làm rõ trong vận hành; lượt này không sửa giá hoặc công thức.

Không bịa số liệu Search Console, lượng tìm kiếm, thứ hạng, đánh giá, tác giả chuyên gia hoặc chi nhánh. Không thêm mức phạt pháp luật. Không hứa lên top Google.

## Kiểm tra đã hoàn tất

- Toàn bộ 30 trang nội dung: title, meta description riêng, canonical, đúng một H1, đích neo, ảnh và liên kết tương đối hợp lệ; không trùng ID.
- 10 trang mới có nội dung hoàn chỉnh trong HTML, breadcrumb, mục lục, ít nhất 3 FAQ và nút gọi/Zalo.
- JSON-LD hợp lệ; dùng Article ở 4 bài hướng dẫn mới, BreadcrumbList ở các trang mới. Không có review/rating giả hoặc lời hứa FAQ rich result.
- 29 thẻ Tin Tức có ảnh bấm được đúng trang, đủ chủ đề tương ứng; các link và nội dung cơ bản vẫn nằm trong HTML khi không chạy JavaScript.
- Sitemap 31 URL thực, không trùng. Robots không chặn.
- Kiểm tra trình duyệt cả 10 trang mới ở 390×844 và 1280×900: không tràn ngang. Đã xem ảnh chụp đại diện trang khu vực và bài hướng dẫn.
- Bộ lọc “Khu vực” trả 7 nội dung (trang tổng hợp + 6 trang riêng). Kết hợp tìm “cam le” không dấu trả 2 nội dung phù hợp (tổng hợp + trang Cẩm Lệ – Hòa Xuân). Bấm ảnh khu vực mở đúng bài. Menu điện thoại mở/đóng và hiển thị đúng 5 mục cùng nút Đặt Nhanh/Zalo.
- Hàm giá cũ được chạy kiểm tra trực tiếp với 3, 8, 15 km, phụ phí đêm và trường hợp trên 30 km: đạt.
- Trang chủ có form, ô đón/đến, giá và canvas bản đồ. Không gửi đặt xe, email hay cuộc gọi thật; chưa kiểm tra trọn luồng định vị, API tìm đường và gửi yêu cầu. Một số lỗi xuất hiện từ tiện ích Facebook nhúng, không thuộc mã mới.
- `node --check assets/js/content.js` và `git diff --check`: đạt.
- Các tệp bảo vệ đã so hash với bản đầu lượt: không thay đổi.

## Cách mở xem thử trên máy

1. Mở `D:\\MINHNGUYET\\webxeho` trong VS Code.
2. Mở `index.html` bằng Live Server. Nếu dùng cổng 5500, vào `http://127.0.0.1:5500/tin-tuc.html`.
3. Chọn bộ lọc “Khu vực”, thử các tên Hải Châu, Sơn Trà hoặc “cam le”. Bấm ảnh để mở trang riêng.
4. Mở `khu-vuc-phuc-vu.html` để xem đủ 6 khu vực và hình đồng phục. Kiểm tra ảnh mới dùng đúng mặt Anh_Anh_Y.
5. Mở bài Hội An/Huế, đối tác, sự kiện và bài bàn giao đã bổ sung trách nhiệm.
6. Dùng chế độ thiết bị của trình duyệt để kiểm tra điện thoại. Tắt JavaScript nếu muốn đối chiếu việc nội dung và link cơ bản vẫn có trong trang.
7. Cổng 5500 không chạy trong lúc QA nên đã dùng máy chủ kiểm tra tạm 8765 tại máy; máy chủ tạm được dừng sau khi hoàn tất. Bạn có thể dùng lại Live Server để xem bất cứ lúc nào.

## Tự đưa lên GitHub sau khi duyệt

1. Rà lại nội dung và các điều kiện cần xác nhận ở trên. Sửa trong đúng tệp HTML nếu có thông tin bổ sung.
2. Trong Source Control của VS Code, xem toàn bộ thay đổi. Có cả công việc các lượt trước chưa commit; không coi mọi tệp đang thay đổi là chỉ thuộc lượt này.
3. Stage đúng các HTML đã duyệt, `assets/css/`, `assets/js/`, các ảnh cần dùng và `sitemap.xml`. Không stage thư mục `work/`, ảnh QA hoặc dữ liệu tạm nếu không muốn đưa vào repo.
4. Chạy `git diff --check` và kiểm tra lại `git status`.
5. Commit với mô tả rõ, ví dụ `Add regional pages and trip planning guides`. Nhánh hiện tại là `main`.
6. Chỉ khi muốn thay đổi website thật, dùng Push/Sync Changes trong VS Code tới remote hiện có. Tôi chưa thực hiện bước này.
7. Kiểm tra GitHub Settings → Pages để xác nhận nhánh/thư mục đang xuất bản; giữ nguyên CNAME.
8. Sau khi GitHub Pages hoàn tất, kiểm tra các URL mới trên `https://laixehodanang.me/`, ảnh, menu, gọi/Zalo và bản đồ/đặt xe. Trong Search Console, gửi lại sitemap bằng tài khoản của bạn nếu cần.

Báo cáo này không xác nhận dữ liệu tìm kiếm hay thứ hạng mới; cần theo dõi thực tế sau khi nội dung được duyệt và xuất bản.
'''
Path('work/BAO-CAO-KHU-VUC-VA-BAI-VIET.md').write_text(text,encoding='utf-8')
print('Detailed report prepared with page list, assets, open questions, QA and publishing instructions.')
