import cv2
import numpy as np
from PIL import Image

def detect_and_crop_face(image):
    # Chuyển đổi ảnh từ định dạng Pillow sang định dạng mà OpenCV có thể xử lý
    open_cv_image = np.array(image.convert('RGB'))[:, :, ::-1].copy()

    # Chuyển đổi ảnh thành ảnh xám (grayscale) để phát hiện khuôn mặt
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    # Tải mô hình Haar Cascade cho phát hiện khuôn mặt
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Phát hiện các khuôn mặt trong ảnh
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        # Nếu tìm thấy ít nhất 1 khuôn mặt, lấy khuôn mặt đầu tiên
        (x, y, w, h) = faces[0]

        # Tăng kích thước vùng cắt thêm 60% xung quanh khuôn mặt
        padding_w = int(w * 0.6)  # Thêm 60% bề rộng
        padding_h = int(h * 0.6)  # Thêm 60% chiều cao

        # Điều chỉnh lại tọa độ và kích thước cắt
        x_new = max(0, x - padding_w)
        y_new = max(0, y - padding_h)
        w_new = min(open_cv_image.shape[1] - x_new, w + 2 * padding_w)
        h_new = min(open_cv_image.shape[0] - y_new, h + 2 * padding_h)

        # Cắt khuôn mặt cùng với phần cổ
        cropped_face = open_cv_image[y_new:y_new+h_new, x_new:x_new+w_new]

        # Chuyển đổi khuôn mặt từ OpenCV trở lại Pillow để xử lý tiếp
        cropped_face_image = Image.fromarray(cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB))

        # Điều chỉnh kích thước khuôn mặt đã cắt cho khít với khung (nếu cần)
        cropped_face_image = cropped_face_image.resize((265, 268), Image.Resampling.LANCZOS)

        return cropped_face_image

    # Nếu không tìm thấy khuôn mặt, trả về None
    return None
