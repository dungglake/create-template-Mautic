from flask import Flask
from app.routes import check_for_new_contacts  
from app.mautic_api import get_mautic_token

app = Flask(__name__)

if __name__ == "__main__":
    # Chạy Flask với chế độ không cần giao diện
    with app.app_context():
        # Lấy token cho Mautic
        print("Lấy token từ Mautic...")
        token = get_mautic_token()
        print(f"Token nhận được: {token}")
        
        # Kiểm tra khi có người dùng mới trong Mautic và tạo thư mời
        print("Bắt đầu kiểm tra các contact mới...")
        check_for_new_contacts(token)
