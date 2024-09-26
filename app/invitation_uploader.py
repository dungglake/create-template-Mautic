from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def upload_invitation_to_server(invitation_file, name):
    # Xác thực với Google Drive
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.json")  # Tải thông tin xác thực từ file credentials
    if not gauth.credentials:
        gauth.LocalWebserverAuth()  # Xác thực OAuth2
    gauth.SaveCredentialsFile("credentials.json")  # Lưu thông tin xác thực

    drive = GoogleDrive(gauth)

    # Kiểm tra xem file invitation_file có tồn tại hay không
    if not os.path.exists(invitation_file):
        print(f"Lỗi: File {invitation_file} không tồn tại.")
        return None

    # Tạo và upload file lên Google Drive
    print(f"Đang upload thư mời {invitation_file} lên Google Drive...")
    try:
        file_drive = drive.CreateFile({'title': os.path.basename(invitation_file)})  
        file_drive.SetContentFile(invitation_file)
        file_drive.Upload()
        print(f"Đã upload thư mời {invitation_file} lên Google Drive.")

        # Lấy link download của file
        file_drive.InsertPermission({
            'type': 'anyone', 
            'value': 'anyone', 
            'role': 'reader'
        })
        invitation_url = file_drive['alternateLink']
        print(f"Link thư mời: {invitation_url}")
        return invitation_url
    except Exception as e:
        print(f"Lỗi khi upload file lên Google Drive: {e}")
        return None
