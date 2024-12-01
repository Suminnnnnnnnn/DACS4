import cv2
import socket
import struct
import pickle
import threading
import time

# Địa chỉ của server signaling
SERVER_IP = '192.168.191.131'
SIGNALING_PORT = 7777
PEER_PORT = 15000  # Sử dụng cổng cố định cho P2P

# Tạo socket và kết nối đến server signaling
signaling_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
signaling_socket.connect((SERVER_IP, SIGNALING_PORT))
print("Kết nối đến server signaling thành công, chờ thông tin từ client khác...")

# Nhận thông tin của client kia từ server
peer_info = signaling_socket.recv(1024).decode()
peer_ip, peer_port = peer_info.split(":")
peer_port = int(peer_port)
print(f"IP, PORT của người kia: {peer_ip}, {peer_port}")
signaling_socket.close()

# Thiết lập socket cho kết nối P2P
peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
peer_socket.bind(('0.0.0.0', PEER_PORT))  # Cố định cổng để chờ kết nối từ peer

# Thử kết nối đến peer
connected = False
for attempt in range(5):
    try:
        peer_socket.connect((peer_ip, peer_port))
        print(f"Đã kết nối đến peer {peer_ip}:{peer_port}")
        connected = True
        break
    except socket.error:
        print(f"Thử kết nối đến peer {peer_ip}:{peer_port}, lần thử {attempt + 1}...")
        time.sleep(2)

# Nếu không kết nối được, chuyển sang chế độ chờ
if not connected:
    peer_socket.listen(1)
    print(f"Chờ peer khác kết nối trên cổng {PEER_PORT}...")
    peer_socket, _ = peer_socket.accept()
    print("Đã kết nối với peer khác")

# Hàm nhận video từ peer và hiển thị
def receive_video():
    data = b""
    payload_size = struct.calcsize("Q")

    while True:
        try:
            while len(data) < payload_size:
                packet = peer_socket.recv(4096)
                if not packet:
                    return
                data += packet

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += peer_socket.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data)
            cv2.imshow("Video từ peer", frame)
            if cv2.waitKey(1) == ord("q"):
                break
        except Exception as e:
            print("Lỗi khi nhận video:", e)
            break

# Tạo luồng cho quá trình nhận video từ peer
threading.Thread(target=receive_video).start()

# Lấy video từ camera và gửi đến peer
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    data = pickle.dumps(frame)
    message = struct.pack("Q", len(data)) + data
    try:
        peer_socket.sendall(message)
    except Exception as e:
        print("Lỗi khi gửi video:", e)
        break

    cv2.imshow("Video từ camera của bạn", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
peer_socket.close()
cv2.destroyAllWindows()