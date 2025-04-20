## Hướng dẫn sử dụng trò chơi Pac-Man

### Cài đặt

Sau khi clone repository về, chạy:

```bash
pip install -r requirements.txt
```

Sau đó chạy:

```bash
python main.py
```

### Giao diện Menu chính

Menu của trò chơi sẽ được khởi tạo sau khi chạy `main.py`.

- Chọn **Play** để vào chế độ chơi Pac-Man tự do.
- Chọn **Watch Algorithm** để kiểm tra và quan sát hoạt động của các thuật toán tìm đường.

---

### Chế độ Play

- Dùng các phím mũi tên `↑ ← ↓ →` để di chuyển Pac-Man thu thập tiền và tránh né các Bóng ma.
- Tiền lớn sẽ mang lại nhiều điểm hơn.
- Nhấn `Esc` để tạm dừng trò chơi. Nhấn `Esc` lần nữa để quay về Menu, hoặc nhấn `Enter` để tiếp tục.

**Khi Pac-Man nhặt hết toàn bộ tiền:**

- Hiển thị chiến thắng.
- Nhấn phím bất kỳ để chuyển sang bản đồ kế tiếp.
- Có **4 bản đồ**. Sau khi hoàn thành bản đồ 4, trò chơi sẽ quay lại bản đồ 1.

**Nếu Pac-Man bị Bóng ma chạm trúng:**

- Hiển thị thất bại.
- Nhấn phím bất kỳ để chơi lại màn hiện tại.

---

### Chế độ Algorithm Watch

- Dùng phím trái/phải `← →` để chọn bản đồ.
- Nhấn `Enter` để xác nhận, `Esc` để quay lại Menu.

**Trong chế độ này:**

- Pac-Man và Bóng ma sẽ xuất hiện ở trạng thái bất động.
- Di chuyển Pac-Man bằng phím `W A S D`.
- Di chuyển Bóng ma bằng mũi tên `↑ ← ↓ →`.
- Một **đường thẳng màu xanh** sẽ xuất hiện trên bản đồ, biểu diễn đường đi mà Bóng ma tìm được đến Pac-Man.

**Nhấn các phím số để thay đổi loại thuật toán của Bóng ma:**

- `1`: Bóng ma đỏ - DFS
- `2`: Bóng ma xanh - BFS
- `3`: Bóng ma hồng - UCS
- `4`: Bóng ma cam - A*

**Thông tin hiển thị:**

- Thời gian thực thi
- Bộ nhớ sử dụng
- Số node mở rộng
- Độ dài đường đi

Nhấn `Esc` để quay lại màn hình chọn bản đồ.
