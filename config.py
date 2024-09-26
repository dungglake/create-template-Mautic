import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MAUTIC_API_URL = os.getenv("MAUTIC_API_URL")
    MAUTIC_CLIENT_ID = os.getenv("MAUTIC_CLIENT_ID")
    MAUTIC_CLIENT_SECRET = os.getenv("MAUTIC_CLIENT_SECRET")
    MAUTIC_REDIRECT_URI = os.getenv("MAUTIC_REDIRECT_URI")
    MAUTIC_USERNAME = os.getenv("MAUTIC_USERNAME")
    MAUTIC_PASSWORD = os.getenv("MAUTIC_PASSWORD")
    FORM_ID = os.getenv("MAUTIC_FORM_ID")
    INVITATION_LINK_FIELD = os.getenv('MAUTIC_INVITATION_LINK_FIELD')
    
    # Cấu hình xác thực bằng tên đăng nhập và mật khẩu (Basic Auth)
    MAUTIC_AUTH = (MAUTIC_USERNAME, MAUTIC_PASSWORD)

    # Các đường dẫn hoặc cài đặt khác
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = os.path.join(BASE_DIR, 'generated_invitations')
    INVITATION_TEMPLATE = os.path.join(BASE_DIR, 'app/templates/thiep-moi.png')
    
    # Đường dẫn đến logo mặc định
    DEFAULT_AVATAR = os.path.join(BASE_DIR, 'app/templates/itprospeak-xanh.png')
    
