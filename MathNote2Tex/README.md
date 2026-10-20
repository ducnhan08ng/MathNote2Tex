##Math2Latex - Công cụ tự động chuẩn hóa ghi chú Toán học sang LaTeX

Công cụ CLI viết bằng Python tích hợp **Google Gemini API** giúp sinh viên tự động chuyển đổi các bản ghi chú bài giảng Toán đại cương (Giải tích, Đại số tuyến tính) dạng văn bản thô sang mã nguồn **LaTeX** chuẩn học thuật.

## Tính năng chính
- Tự động nhận diện và phân loại cấu trúc: Định lý, Công thức, Ma trận và Bài tập.
- Chuyển đổi các ký hiệu toán học gõ tắt (`<=`, `->`, ma trận `[a b; c d]`) sang cú pháp `amsmath` chuẩn xác.
- Làm sạch đầu ra tự động bằng Regular Expressions (Regex), xuất file `.tex` sẵn sàng biên dịch sang PDF.

## Minh họa kết quả (Demo)
![Demo Screenshot](demo.png)

## Cài đặt & Sử dụng
1. Cài đặt thư viện: