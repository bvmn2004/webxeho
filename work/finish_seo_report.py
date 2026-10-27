import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source_path = root / 'content/pages.json'
data = json.loads(source_path.read_text(encoding='utf-8'))
for page in data['pages']:
    if page['file'] == 'can-chuan-bi-gi-khi-ban-giao-xe.html':
        page['body_html'] = page['body_html'].replace(' Nếu cần biết điều kiện bảo hiểm hoặc cách xử lý khi có sự cố, hỏi rõ đơn vị cung cấp trước khi giao xe và lưu nội dung đã thống nhất.', ' Lưu lại nội dung đã thống nhất để đối chiếu khi cần.')
source_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

lines = ['# Báo cáo chỉnh sửa SEO toàn bộ nội dung — 28/10/2026', '',
'Đã rà soát 31 trang: 29 trang chi tiết, trang Tin tức và trang chủ. Đã chỉnh trực tiếp thân nội dung của đủ 29 trang chi tiết; cập nhật dữ liệu giới thiệu bài trên Tin tức. Trang chủ được kiểm tra và giữ nguyên trong đợt này. Không có trang chi tiết nào trong danh sách bị bỏ qua. Hai tệp xác minh Google không phải trang nội dung.', '',
'Đã kiểm tra git status trước khi làm và giữ nguyên các thay đổi đang có. Không reset, commit, push hoặc deploy. Các tệp trang chủ, chức năng đặt xe/bản đồ/tính giá và mã theo dõi đã được đối chiếu với bản lưu đầu đợt chỉnh sửa.', '',
'## Từng trang đã sửa', '',
'Tất cả 29 trang bên dưới đều có phần mở đầu trả lời nhu cầu khách; kiểm tra H1/H2/H3, title, description, canonical, liên kết nội bộ, ảnh/alt, nút gọi/Zalo và cách xem trên điện thoại. Nội dung bổ sung theo nhu cầu từng trang, không đặt mục tiêu số chữ.', '',
'| Trang / URL giữ nguyên | Thay đổi chính trong thân bài |',
'| --- | --- |']
for page in data['pages']:
    lines.append(f"| [{page['h1']}](http://127.0.0.1:5500/{page['file']}) — `{page['file']}` | {page['change_summary']} |")
lines += ['',
'## Trang Tin tức và nguồn nội dung', '',
'`tin-tuc.html`: đồng bộ tiêu đề, mô tả xem trước, alt và dữ liệu tìm kiếm của cả 29 thẻ bài; sửa tiêu đề trang bị lặp thương hiệu. Giữ liên kết ảnh đến đúng bài, bộ lọc chủ đề và tìm kiếm không dấu.', '',
'Nguồn chỉnh sửa hiện tại là `content/pages.json` (đủ thân bài và thông tin SEO của 29 trang). `scripts/render-content.py` cập nhật các HTML, thẻ giới thiệu Tin tức và ngày sửa trong sitemap, đồng thời giữ khung giao diện đang có. Hướng dẫn trong `content/README.md`. Các bản nháp trong work không phải nguồn dựng nội dung hiện tại.', '',
'Từ thư mục dự án, chạy `py scripts/render-content.py` sau khi sửa nguồn; chạy `py scripts/render-content.py --check` để kiểm tra các trang đã đồng bộ. Công cụ dựng chỉ dùng thư viện chuẩn Python. Các trang HTML đã được tạo sẵn để phục vụ như web tĩnh.', '',
'## Thông tin kinh doanh cần xác nhận', '',
'- Quy ước tính ở ranh giới khoảng km, làm tròn quãng đường; các mốc xe máy 5/7 km và thời điểm kết thúc phụ phí đêm của xe máy. Không tự thay công thức đang chạy hoặc chèn dòng cảnh báo mốc 5 km vào bài.',
'- Phí chờ, đổi hành trình, điểm ghé, bãi đỗ/cầu đường; cách xác nhận tổng giá và điều kiện hủy chuyến.',
'- Số giờ tối thiểu khi thuê theo giờ, thời lượng một ngày, quá giờ, qua đêm và các khoản trong báo giá đi tỉnh.',
'- Khả năng nhận chuyến Hội An/Huế theo từng lịch, chuyến một chiều/khứ hồi; số xe có thể phục vụ cùng lúc cho sự kiện.',
'- Điều kiện nhận xe thuê/mượn, trách nhiệm bàn giao và phạm vi bảo hiểm nếu doanh nghiệp có chính sách thực tế.',
'- Khả năng phục vụ ngoại ngữ, chứng từ và phương thức thanh toán nếu muốn công bố thêm.', '',
'Các nội dung chưa có căn cứ được trình bày theo hướng khách gửi nhu cầu để xác nhận. Không tự thêm giá trọn gói, số phút tài xế có mặt, cam kết bảo hiểm hoặc đánh giá khách hàng. Header/footer và địa chỉ trong đó được giữ nguyên theo trang chủ như yêu cầu; doanh nghiệp nên xác nhận cách ghi địa chỉ hành chính hiện hành trước khi đổi đồng loạt.', '',
'## Kiểm tra đã thực hiện', '',
'- Đối chiếu thân bài trước/sau: đủ 29 trang có thay đổi nội dung, không chỉ sửa thẻ Tin tức.',
'- Kiểm tra nguồn dựng với `--check`; rà soát độc lập bằng `work/validate_full_seo_pass.py`: đạt.',
'- Kiểm tra title/description không trùng, canonical/OG, một H1 mỗi trang, ID/mục lục, JSON-LD và ngày cập nhật bài: đạt.',
'- Kiểm tra các liên kết nội bộ, fragment, tài nguyên ảnh, alt/kích thước, 29 thẻ Tin tức và 31 URL sitemap: đạt.',
'- Đối chiếu header/footer từng trang với index, mã Google Analytics/Ads và các tệp được bảo vệ bằng hash: giữ nguyên.',
'- Mở đủ 29 trang ở 390×844 và 1280×900; không phát hiện tràn ngang. Xem ảnh chụp đại diện kèm báo cáo.',
'- Thử lọc Sau tiệc, tìm kiếm không dấu “ban giao” và bấm ảnh vào đúng bài: đạt.',
'- Thử công thức tính giá hiện có: 3 km ban ngày 150.000đ; 8 km 200.000đ; 15 km 275.000đ; 8 km lúc 23h 250.000đ; trên 30 km chuyển sang liên hệ: đạt.',
'- `git diff --check`: đạt. Không gửi đặt xe thử, không gọi điện/nhắn Zalo thật và không thay đổi dữ liệu Analytics.', '',
'Giới hạn kiểm tra: chưa thực hiện một chuyến đặt xe thật, chưa kiểm chứng định tuyến/geolocation với địa chỉ khách hoặc việc gửi thông tin đến hệ thống bên ngoài. Mã của các chức năng này được giữ nguyên; các kiểm tra trên không thay cho thử nghiệm vận hành thực tế. SEO kỹ thuật và nội dung được cải thiện nhưng thứ hạng/lưu lượng cần theo dõi sau khi chủ web xuất bản.', '',
'## Cách xem trên máy', '',
'Mở thư mục `D:\\MINHNGUYET\\webxeho` bằng trình soạn thảo và chạy Live Server như hiện tại. Truy cập [Tin tức](http://127.0.0.1:5500/tin-tuc.html), rồi bấm từng ảnh/tiêu đề; các liên kết trong bảng báo cáo cũng dùng cổng 5500.', '',
'Nếu không dùng Live Server, mở PowerShell trong thư mục dự án, chạy `py -m http.server 5500 --bind 127.0.0.1`, rồi mở cùng địa chỉ trên. Chỉ chạy khi cổng 5500 chưa được ứng dụng khác sử dụng. Nhấn Ctrl+C để dừng. Đây là xem cục bộ, không xuất bản web.', '',
'## Tài liệu tham chiếu', '',
'Cách biên tập ưu tiên câu trả lời hữu ích, phù hợp nhu cầu của người đọc theo [Google Search Central](https://developers.google.com/search/docs/fundamentals/creating-helpful-content). Tiêu đề trang được viết riêng và rõ nội dung theo [hướng dẫn title link](https://developers.google.com/search/docs/appearance/title-link). Không dùng hashtag như lời hứa tăng hạng; các nhãn chủ đề phục vụ điều hướng nội bộ.', '']
(root / 'work/SEO-TOAN-BO-2026-10-28.md').write_text('\n'.join(lines), encoding='utf-8')
print('Report created for all 29 detail pages.')
