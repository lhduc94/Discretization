# Discretization
Ứng dụng demo về các thuật toán discretization và binning được xây dựng với Streamlit.

## 🚀 Tính năng

- **Upload file CSV**: Tải lên file dữ liệu của bạn
- **Chọn cột numerical**: Chọn cột số để thực hiện discretization
- **Visualization**: Hiển thị histogram và KDE plot của dữ liệu gốc
- **Nhiều thuật toán**: Hỗ trợ 5 thuật toán discretization khác nhau
- **Tùy chỉnh tham số**: Điều chỉnh các tham số của từng thuật toán
- **Kết quả trực quan**: So sánh dữ liệu trước và sau discretization
- **Export kết quả**: Tải xuống kết quả dưới dạng CSV

## �� Thuật toán được hỗ trợ

1. **Equal Width Binning**: Chia dữ liệu thành các bin có độ rộng bằng nhau
2. **Equal Frequency Binning**: Chia dữ liệu thành các bin có số lượng phần tử bằng nhau
3. **K-Means Binning**: Sử dụng K-Means clustering để tạo các bin
4. **Jenks Natural Breaks**: Tìm các điểm break tự nhiên trong dữ liệu
5. **Standard Deviation Binning**: Chia dữ liệu dựa trên độ lệch chuẩn

## ��️ Cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd desscretozation
```

2. Cài đặt dependencies:
```bash
poetry install
```

3. Chạy ứng dụng:
```bash
poetry run streamlit run app.py
```

## 📖 Cách sử dụng

1. **Upload dữ liệu**: Chọn file CSV chứa dữ liệu numerical
2. **Chọn cột**: Chọn cột số bạn muốn discretize
3. **Xem phân tích**: Ứng dụng sẽ hiển thị histogram và KDE plot
4. **Chọn thuật toán**: Chọn thuật toán discretization phù hợp
5. **Điều chỉnh tham số**: Tùy chỉnh các tham số của thuật toán
6. **Áp dụng**: Nhấn nút "Áp dụng thuật toán" để xem kết quả
7. **Tải xuống**: Tải xuống kết quả dưới dạng CSV

## �� Ví dụ sử dụng

Ứng dụng có sẵn dữ liệu mẫu để test. Bạn có thể:
- Tải xuống dữ liệu mẫu
- Upload lại để test các thuật toán
- So sánh kết quả giữa các phương pháp khác nhau

## �� Screenshots

[Thêm screenshots của ứng dụng ở đây]

## �� Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo issue hoặc pull request.

## 📄 License

MIT License