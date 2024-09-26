import requests
import json
from config import Config
import os
import time

# Hàm kiểm tra xem token có còn hợp lệ không, nếu hết hạn sẽ tự động làm mới
def get_valid_token():
    token_info = load_token_info()

    if token_info and 'access_token' in token_info:
        # Kiểm tra token còn hợp lệ không
        if is_token_expired(token_info):
            print("Access token đã hết hạn. Đang yêu cầu refresh token...")
            new_token_info = refresh_token(token_info.get('refresh_token'))
            if new_token_info:
                save_token_info(new_token_info)
                return new_token_info['access_token']
            else:
                # Nếu refresh token không còn hợp lệ, yêu cầu lấy token mới
                print("Không thể làm mới token. Đang yêu cầu lấy token mới...")
                return get_mautic_token()
        else:
            return token_info['access_token']
    else:
        print("Không có token hợp lệ, yêu cầu lấy token mới.")
        return get_mautic_token()

# Hàm lấy token từ Mautic bằng grant type client_credentials
def get_mautic_token():
    data = {
        'client_id': Config.MAUTIC_CLIENT_ID,
        'client_secret': Config.MAUTIC_CLIENT_SECRET,
        'grant_type': 'client_credentials',
    }

    print("Đang yêu cầu lấy token từ Mautic...")
    response = requests.post(f"{Config.MAUTIC_API_URL}oauth/v2/token", data=data)

    try:
        token_info = response.json()  # Chuyển đổi phản hồi thành JSON
        if isinstance(token_info, dict):  # Kiểm tra xem token_info có phải là dict không
            if 'access_token' in token_info:
                print("Token nhận được thành công!")
                save_token_info(token_info)
                return token_info['access_token']
            else:
                print(f"Lỗi khi lấy token: {token_info}")
                return None
        else:
            print("Lỗi: token_info không phải là một đối tượng dict hợp lệ.")
            return None
    except json.JSONDecodeError:
        print("Lỗi: Phản hồi không phải là JSON hợp lệ.")
        return None

# Hàm làm mới token khi access_token hết hạn
def refresh_token(refresh_token):
    if not refresh_token:
        print("Không có refresh token để làm mới. Yêu cầu lấy token mới...")
        return get_mautic_token()

    data = {
        'client_id': Config.MAUTIC_CLIENT_ID,
        'client_secret': Config.MAUTIC_CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }

    response = requests.post(f"{Config.MAUTIC_API_URL}oauth/v2/token", data=data)

    try:
        new_token_info = response.json()  # Chuyển đổi phản hồi thành JSON
        if isinstance(new_token_info, dict):  # Kiểm tra xem phản hồi có phải là dict không
            if 'access_token' in new_token_info:
                print("Token đã được làm mới thành công.")
                return new_token_info
            else:
                print(f"Lỗi khi làm mới token: {new_token_info}")
                return None
        else:
            print("Lỗi: token_info không phải là một đối tượng dict hợp lệ.")
            return None
    except json.JSONDecodeError:
        print("Lỗi: Phản hồi không phải là JSON hợp lệ.")
        return None

# Hàm kiểm tra token hết hạn
def is_token_expired(token_info):
    if 'expires_in' in token_info and 'created_at' in token_info:
        current_time = time.time()
        expiration_time = token_info['created_at'] + token_info['expires_in']
        return current_time > expiration_time
    return True

# Hàm lưu thông tin token vào file và thêm thời gian token được tạo
def save_token_info(token_info):
    if isinstance(token_info, dict):  # Kiểm tra xem token_info có phải là dict hay không
        token_info['created_at'] = time.time()  # Lưu lại thời gian nhận token
        with open("token_info.json", "w") as f:
            json.dump(token_info, f)
    else:
        print("Lỗi: token_info không phải là một đối tượng dict hợp lệ.")

# Hàm tải token từ file
def load_token_info():
    if os.path.exists("token_info.json"):
        with open("token_info.json", "r") as f:
            return json.load(f)
    return None

# Hàm lấy danh sách contacts từ Mautic
def get_latest_contacts(token):
    url = f"{Config.MAUTIC_API_URL}api/forms/4/submissions"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        submissions = response.json()
        return submissions.get('submissions', [])
    elif response.status_code == 401:  # Token không hợp lệ hoặc đã hết hạn
        print("Token không hợp lệ hoặc đã hết hạn. Đang yêu cầu token mới...")
        new_token = get_mautic_token()  # Yêu cầu token mới
        if new_token:
            return get_latest_contacts(new_token)  # Thử lại với token mới
        else:
            print("Lỗi khi lấy token mới.")
            return None
    else:
        print(f"Lỗi khi lấy submissions: {response.status_code}, {response.text}")
        return None

# Hàm kiểm tra contact mới
def check_for_new_contacts(token):
    contacts = get_latest_contacts(token)
    
    if contacts is None:
        print("Không có contact nào hoặc gặp lỗi khi lấy contacts.")
        return

# Lấy token hợp lệ
token = get_valid_token()
if token:
    # Thực hiện các yêu cầu khác với token hợp lệ
    check_for_new_contacts(token)
