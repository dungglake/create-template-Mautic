import requests
from config import Config

# Hàm tìm kiếm contact theo email trong Mautic
def get_contact_by_email(email):
    url = f"{Config.MAUTIC_API_URL}api/contacts"
    params = {
        'search': f"email:{email}"  # Tìm kiếm theo email
    }
    response = requests.get(url, params=params, auth=Config.MAUTIC_AUTH)
    
    if response.status_code == 200:
        contacts = response.json().get('contacts', [])
        if contacts:
            # Trả về contact đầu tiên tìm thấy
            return list(contacts.values())[0]
        else:
            print(f"Không tìm thấy contact với email: {email}")
            return None
    else:
        print(f"Lỗi khi tìm kiếm contact theo email: {response.status_code} - {response.text}")
        return None

# Hàm cập nhật link Google Drive vào trường tùy chỉnh 'invitation_link' cho contact dựa trên email
def update_invitation_link_in_mautic_by_email(email, invitation_url):
    contact = get_contact_by_email(email)  # Lấy contact dựa trên email
    if contact:
        contact_id = contact['id']
        existing_invitation_link = contact['fields']['all'].get('invitation_link')

        # Kiểm tra nếu contact đã có link, nếu có thì bỏ qua
        if existing_invitation_link and isinstance(existing_invitation_link, str) and existing_invitation_link:
            print(f"Contact với email {email} đã có link thư mời, bỏ qua cập nhật.")
            return  # Không thực hiện cập nhật nếu đã có link

        # Nếu chưa có link thì thực hiện cập nhật
        url = f"{Config.MAUTIC_API_URL}api/contacts/{contact_id}/edit"
        payload = {
            'invitation_link': invitation_url  # Cập nhật URL thư mời
        }
        print(f"Gửi yêu cầu để cập nhật contact {contact_id} (email: {email}) với link thư mời {invitation_url}")
        response = requests.patch(url, json=payload, auth=Config.MAUTIC_AUTH)

        if response.status_code == 200:
            print(f"Đã cập nhật link Google Drive cho contact {contact_id} (email: {email})")
        else:
            print(f"Lỗi khi cập nhật link cho contact {contact_id} (email: {email}): {response.status_code} - {response.text}")
    else:
        print(f"Không thể cập nhật link, không tìm thấy contact với email {email}")
