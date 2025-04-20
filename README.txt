Sau khi clone về, chạy 
pip install -r requirements.txt 

Chạy main.py:

Menu của trò chơi được khởi tạo.
Chọn Play để vào chế độ chơi Pac-man tự do, Watch Algorithm để kiểm tra thuật toán

Chế độ Play:
	Dùng các phím mũi tên ↑←↓→ để di chuyển Pac-man thu thập hết toàn bộ tiền và tránh né các Bóng ma. Thu thập tiền lớn sẽ nhận lượng điểm lớn hơn.
	Nhấn Esc để dừng trò chơi. Nhấn Esc lần nữa để quay lại Menu, hoặc nhấn Enter để tiếp tục trò chơi.
	Sau khi nhặt hết toàn bộ tiền, Pac-man sẽ chiến thắng màn chơi. Nhấn phím bất kỳ để qua bản đồ kế tiếp. Trò chơi hiện có 4 bản đồ, sau khi xong bản đồ 4 sẽ quay lại bản đồ 1.
	Khi bị Bóng ma chạm trúng, Pac-man sẽ thất bại. Nhấn phím bất kỳ để chơi lại màn.

Chế độ Algorithm Watch:
	Dùng các phím ← → để lựa chọn bản đồ. Nhấn Enter để xác nhận, Esc để quay lại Menu.
	Màn hình vào chế độ Algorithm Watch, trên bản đồ xuất hiện Pac-man và Bóng ma (mặc định là Bóng ma đỏ - DFS) bất động
	Di chuyển Pac-man bằng WASD, di chuyển Bóng ma bằng các phím mũi tên ↑←↓→
	Trên bản đồ sẽ xuất hiện đường thẳng xanh, thể hiện đường đi của Bóng ma đến Pac-man.
	Nhấn 1, 2, 3, 4 để đổi Bóng ma: 1 - Bóng ma đỏ DFS, 2 - Bóng ma xanh BFS, 3 - Bóng ma hồng UCS, 4 - Bóng ma cam A*
	Màn hình có xuất hiện thông tin về thời gian, bộ nhớ, số node mở rộng và độ dài đường đi.
	Nhấn Esc để quay lại màn hình chọn bản đồ.
