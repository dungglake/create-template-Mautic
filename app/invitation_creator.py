from PIL import Image, ImageDraw, ImageFont
import requests
import random
import os
from config import Config
from app.face_extractor import detect_and_crop_face

# Hàm xử lý avatar URL từ contact_id
def get_avatar_url(contact_id):
    base_url = "https://mautic.mkt.vietnix.vn/forms/results/file/"
    complete_url = f"{base_url}{contact_id}/anh_dai_dien"
    return complete_url

def crop_to_circle(image):
    # Tạo một mask hình tròn với cùng kích thước với ảnh
    size = image.size
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)

    # Tạo một ảnh nền mới với cùng kích thước và giữ nguyên màu của ảnh gốc
    result = Image.new("RGBA", size, (255, 255, 255, 0))  # Nền trong suốt

    # Dán ảnh gốc lên nền mới với mask hình tròn
    result.paste(image, (0, 0), mask=mask)

    return result

def create_personalized_invitation(name, contact_id):
    print(f"Tạo thư mời cho {name}...")

    # Đảm bảo rằng thư mục OUTPUT_DIR đã tồn tại
    if not os.path.exists(Config.OUTPUT_DIR):
        os.makedirs(Config.OUTPUT_DIR)
        print(f"Đã tạo thư mục: {Config.OUTPUT_DIR}")

    sanitized_name = name.replace(" ", "_")
    
    # Kiểm tra xem file đã tồn tại chưa
    existing_files = [f for f in os.listdir(Config.OUTPUT_DIR) if f.startswith(sanitized_name)]
    if existing_files:
        print(f"Thư mời cho {name} đã tồn tại: {existing_files[0]}. Bỏ qua việc tạo mới.")
        existing_path = os.path.join(Config.OUTPUT_DIR, existing_files[0])
        return existing_path, existing_files[0].split('_')[-1].split('.')[0]  # Trả về file và mã số may mắn

    # Mở template thiệp mời
    invitation = Image.open(Config.INVITATION_TEMPLATE)
    print(f"Đã mở template thiệp mời từ: {Config.INVITATION_TEMPLATE}")

    avatar_image = None
    if contact_id:
        try:
            avatar_url = get_avatar_url(contact_id)
            print(f"Lấy ảnh đại diện từ URL: {avatar_url}")
            response = requests.get(avatar_url, stream=True)
            if response.status_code == 200:
                avatar_image = Image.open(response.raw)

                # Phát hiện và cắt khuôn mặt
                cropped_face = detect_and_crop_face(avatar_image)
                if cropped_face:
                    avatar_image = cropped_face  # Sử dụng ảnh đã cắt nếu phát hiện được khuôn mặt
                else:
                    print(f"Không tìm thấy khuôn mặt, sử dụng logo mặc định: {Config.DEFAULT_AVATAR}")
                    avatar_image = Image.open(Config.DEFAULT_AVATAR)
            else:
                print(f"Lỗi khi tải ảnh từ URL, mã lỗi {response.status_code}. Sử dụng logo mặc định.")
                avatar_image = Image.open(Config.DEFAULT_AVATAR)
        except Exception as e:
            print(f"Lỗi khi lấy ảnh đại diện: {e}. Sử dụng logo mặc định.")
            avatar_image = Image.open(Config.DEFAULT_AVATAR)
    else:
        print(f"Contact ID không hợp lệ, sử dụng logo mặc định: {Config.DEFAULT_AVATAR}")
        avatar_image = Image.open(Config.DEFAULT_AVATAR)

    # Resize ảnh đại diện với kích thước cố định, giữ nguyên tỷ lệ
    if avatar_image != Image.open(Config.DEFAULT_AVATAR):
        avatar_image.thumbnail((264, 270), Image.Resampling.LANCZOS)  # Resize ảnh đại diện nếu không phải logo
    else:
        avatar_image = avatar_image.resize((264, 270), Image.Resampling.LANCZOS)

    # Cắt viền của ảnh theo hình tròn, giữ nguyên màu
    avatar_image = crop_to_circle(avatar_image)

    # Dán ảnh đại diện vào vị trí trong thư mời (vị trí hình tròn đã định)
    invitation.paste(avatar_image, (138, 245), avatar_image)
    print("Đã chèn ảnh đại diện vào thiệp mời.")

    # Thêm tên và số may mắn
    draw = ImageDraw.Draw(invitation)
    font = ImageFont.truetype("arial.ttf", 50)  # Phông chữ lớn hơn cho tên

    # Xử lý tọa độ dựa trên số lượng từ trong tên
    name_words = name.split()  # Tách tên thành các từ
    word_count = len(name_words)

    if word_count == 1:
        text_position = (710, 260)  # Nếu tên có 1 từ
    elif word_count == 2:
        text_position = (670, 260)  # Nếu tên có 2 từ
    elif word_count == 3:
        text_position = (600, 260)  # Nếu tên có 3 từ
    else:
        text_position = (500, 260)  # Nếu tên có 4 từ trở lên

    draw.text(text_position, name, font=font, fill="white")
    print(f"Đã thêm tên {name} vào thiệp mời.")

    # Tạo mã số may mắn
    lucky_number = random.randint(100000, 999999)
    font_lucky = ImageFont.truetype("arial.ttf", 45)
    draw.text((802, 953), f"{lucky_number}", font=font_lucky, fill="white")
    print(f"Đã thêm mã số may mắn: {lucky_number}")

    # Đặt tên file và lưu
    sanitized_name = name.replace(" ", "_")
    invitation_filename = f"{sanitized_name}_{lucky_number}.png"
    invitation_path = os.path.join(Config.OUTPUT_DIR, invitation_filename)

    if not os.path.exists(Config.OUTPUT_DIR):
        os.makedirs(Config.OUTPUT_DIR)
        print(f"Đã tạo thư mục: {Config.OUTPUT_DIR}")

    try:
        # Đảm bảo ảnh giữ nguyên phông nền và định dạng PNG
        if invitation.mode in ("RGBA", "LA"):  # Kiểm tra nếu ảnh có kênh alpha (trong suốt)
            invitation = invitation.convert("RGBA")  # Đảm bảo ảnh có nền trong suốt
        else:
            invitation = invitation.convert("RGB")  # Nếu không có kênh trong suốt, sử dụng chế độ RGB

        # Lưu ảnh với định dạng PNG để giữ nguyên phông nền
        invitation.save(invitation_path, format="PNG")
        print(f"Thư mời đã được lưu tại {invitation_path}")
        return invitation_path, lucky_number
    except Exception as e:
        print(f"Lỗi khi tạo thư mời: {e}")
        return None, None
