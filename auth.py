from pydrive.auth import GoogleAuth

# Khởi tạo đối tượng GoogleAuth
gauth = GoogleAuth()

# Tải thông tin từ file client_secrets.json (đã tải từ Google Cloud Console)
gauth.LoadClientConfigFile("client_secrets.json")

# Xác thực qua trình duyệt web (mở trình duyệt để đăng nhập và cấp quyền)
gauth.LocalWebserverAuth()

# Lưu thông tin xác thực đã nhận được vào file credentials.json
gauth.SaveCredentialsFile("credentials.json")
