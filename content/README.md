# Nguồn nội dung của các trang chi tiết

`pages.json` là nguồn biên tập cho toàn bộ 29 trang bài viết, dịch vụ, bảng giá và khu vực hiện có. Mỗi mục có URL/tệp giữ nguyên, mục đích trang, tiêu đề SEO, mô tả, mở đầu, alt ảnh và nội dung HTML hoàn chỉnh.

Sau khi sửa nội dung trong JSON, chạy ở thư mục dự án:

```powershell
py scripts/render-content.py
py scripts/render-content.py --check
```

Script dùng thư viện chuẩn Python 3, không cần cài gói. Nó cập nhật các phần nội dung và metadata của HTML hiện có, đồng bộ thẻ bài ở Tin Tức và sitemap. Nó không sửa `index.html`, header/footer, CSS, JavaScript đặt xe, mã theo dõi hoặc ảnh.

HTML đầu ra là tệp tĩnh đầy đủ; GitHub Pages không cần chạy Python, và người đọc không cần JavaScript để xem bài hoặc bấm link cơ bản. Đưa cả HTML đã tạo ra lên GitHub sau khi duyệt.

`body_html` là nội dung bên trong `.reading`: các mục H2/H3, bảng, FAQ, mục lục, chủ đề, liên kết liên quan và khối liên hệ. Giữ ID đã có khi chỉnh mục lục để không làm hỏng liên kết neo. Ảnh và giá phải khớp thông tin được chủ dịch vụ xác nhận.

Các script trong `work/` là bản ghi thao tác của các lượt trước, **không phải lệnh build hiện hành**. Không chạy lại chúng để xuất bản nội dung: chúng có thể chứa bản nháp cũ. Lệnh tạo lại được hỗ trợ là `scripts/render-content.py` ở trên.

Nếu chỉnh trực tiếp HTML cho một tình huống đặc biệt, cập nhật cùng nội dung tương ứng trong JSON trước khi chạy lại script; `--check` sẽ phát hiện HTML không còn khớp nguồn.
