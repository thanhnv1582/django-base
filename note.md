<!-- step 1: plan.md -->
<!-- /plan -->
<!-- /create -->

<!-- Tạo Model: /create Tạo module 'Products' với các trường dữ liệu [A, B, C], tích hợp sẵn validation và các phương thức trong Model Manager.

Tạo API: /create Viết các API Viewsets cho module 'Products' sử dụng Django Rest Framework, kèm theo Serializers và phân quyền (Permissions). -->

<!-- 1. Tại sao vẫn nên có môi trường local?
Tốc độ IDE (PyCharm/VSCode): Khi bạn cài đặt thư viện ở local, IDE sẽ hỗ trợ IntelliSense, Code Completion, và Jump to Definition cực nhanh. Nếu chỉ chạy trong Docker, một số IDE cần config phức tạp hơn mới hiểu được các thư viện trong container.
Debugging: Việc đặt breakpoint và debug trực tiếp trên môi trường native thường đơn giản và ổn định hơn so với remote debugging vào trong container.
Hiệu năng (Performance): Trên macOS/Windows, việc mount volume vào Docker (bind mounts) có thể gây chậm do quá trình đồng bộ file hệ thống. Chạy app trực tiếp ở local sẽ cho t ốc độ hot-reload nhanh hơn đáng kể.
Các công cụ bổ trợ: Các lệnh như ruff (linter), pytest (test), pre-commit chạy ở local sẽ phản hồi gần như tức thì, giúp bạn giữ nhịp code tốt hơn. -->

<!-- 2. Tại sao vẫn nên có môi trường Docker?
Tính nhất quán (Consistency): "It works on my machine" sẽ không còn là vấn đề. Mọi người trong team (hoặc bạn khi deploy lên server) đều chạy chính xác cùng một phiên bản hệ điều hành, cùng một phiên bản thư viện hệ thống (như PostgreSQL, Redis). Điều này loại bỏ lỗi do môi trường khác biệt.
Đóng gói (Packaging): Docker cho phép bạn đóng gói ứng dụng và tất cả các dependencies của nó vào một "container". Khi bạn push container này lên cloud (AWS ECS, Google Cloud Run, Azure), nó sẽ chạy y hệt như lúc bạn test ở local.
Quản lý tài nguyên: Docker giúp bạn giới hạn lượng RAM, CPU mà ứng dụng sử dụng, tránh việc một ứng dụng "ngốn" hết tài nguyên của máy.
Triển khai (Deployment): Việc deploy ứng dụng lên server trở nên đơn giản hơn rất nhiều. Thay vì phải cài đặt thủ công từng bước (apt-get install python3, pip install, v.v.), bạn chỉ cần chạy lệnh docker run hoặc docker-compose up. -->