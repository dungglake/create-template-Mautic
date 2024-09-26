from app.mautic_api import get_latest_contacts
from app.email_sender import update_invitation_link_in_mautic_by_email
from app.invitation_creator import create_personalized_invitation
from app.invitation_uploader import upload_invitation_to_server
from config import Config
import time

# Hàm kiểm tra và xử lý contact mới
def process_contact(contact, processed_emails):
    contact_id = contact.get('id', 'Không có ID')  # Sử dụng ID để hiển thị thông tin
    email = contact.get('results', {}).get('email', 'Không có email')
    name = contact.get('results', {}).get('ho_va_ten', 'Tên không tồn tại')

    if email not in processed_emails:
        print(f"Contact mới phát hiện: {name}, ID: {contact_id}, Email: {email}")
        
        # Tạo thư mời và truyền `contact_id` vào `create_personalized_invitation`
        invitation_file, lucky_number = create_personalized_invitation(name, contact_id)
        if invitation_file:
            print(f"Thư mời được tạo cho {name}, Lucky Number: {lucky_number}")

            # Lưu lên Google Drive và lấy link
            invitation_url = upload_invitation_to_server(invitation_file, name)
            if invitation_url:
                print(f"Thư mời đã được upload lên Google Drive: {invitation_url}")
                
                # Gán link Google Drive vào trường tùy chỉnh của contact trong Mautic
                update_invitation_link_in_mautic_by_email(email, invitation_url)
            else:
                print("Lỗi khi upload thư mời lên Google Drive.")
        else:
            print(f"Lỗi khi tạo thư mời cho {name}.")

        # Thêm email vào danh sách đã xử lý
        processed_emails.add(email)
    else:
        # Bỏ qua contact có email trùng lặp, nhưng vẫn in ra ID và thông tin liên quan để biết contact nào được bỏ qua
        print(f"Email {email} (ID: {contact_id}) đã được xử lý trước đó, bỏ qua...")

# Hàm kiểm tra contact mới và xử lý ngay nếu phát hiện
def check_for_new_contacts(token):
    processed_emails = set()  # Danh sách email các contact đã xử lý

    while True:
        contacts = get_latest_contacts(token)
        new_contact_detected = False  # Đặt cờ để theo dõi nếu có contact mới được phát hiện

        # Xử lý từng contact
        for contact in contacts:
            email = contact.get('results', {}).get('email')
            contact_id = contact.get('id')  

            # Kiểm tra nếu email này chưa được xử lý
            if email and email not in processed_emails:
                process_contact(contact, processed_emails)
                new_contact_detected = True  # Đánh dấu là đã phát hiện contact mới

        if new_contact_detected:
            print("Đã phát hiện contact mới và xử lý.")
        else:
            pass

        # Kiểm tra lại sau mỗi giây (có thể tùy chỉnh thời gian chờ giữa các lần kiểm tra)
        time.sleep(1)

