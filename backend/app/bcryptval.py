import bcrypt
#from app import mail
from flask_mail import Mail, Message
import ssl
import datetime
import socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend


def password_hashing(token):
    SECRET_KEY='$2b$12$ag3g.9K9b.8S8n6a6SMGBO'
    hashed_token = (bcrypt.hashpw(token.encode('utf-8'), SECRET_KEY.encode('utf-8'))).decode('utf-8')
    print(f'Token : {token} & Hashed Token : {hashed_token}')
    if hashed_token:
        return hashed_token
    else:
        return None

#password_hashing('abc')
def send_mail(email, otp): #done
    try:
        print('sending email')
        body_text= f'You have now requested for new password, your OTP is {otp}'
        msg=Message('Update Password', sender='utorrentdata1@gmail.com', recipients=[email])
        msg.body= body_text
        mail.send(msg)
        return True
    except: return False

#send_mail('mohibs2001@gmail.com',1234)

# def get_ssl_certificate_expiration(url):
#     try:
#         context = ssl.create_default_context()
#         conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=url)
#         conn.connect((url, 443))
#         cert = conn.getpeercert()
#         print("got certificate")
#         not_after = cert['notAfter']
#         print(not_after)
#         return not_after        
#     except (ssl.SSLError, socket.error, KeyError):
#         print("invalid url")
#         return None
    

# def get_ssl_certificate_expiration2(url):
#     try:
#         context = ssl.create_default_context()
#         conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=url)
#         conn.connect((url, 443))
#         der_cert = conn.getpeercert(binary_form=True)
#         cert = x509.load_der_x509(der_cert, default_backend())
#         not_after = cert.not_valid_after
#         return {
#             'certificate_expiration': not_after,
#             'certificate_present': True,
#             'url_valid': True
#         }
#     except (ssl.SSLError, socket.error):
#         return {
#             'certificate_expiration': None,
#             'certificate_present': False,
#             'url_valid': False
#         }


def get_ssl_certificate_expiration(url):
    try:
        # Set a timeout for the SSL handshake
        context = ssl.create_default_context(timeout=10)

        # Establish a connection with a timeout for the connection attempt
        with socket.create_connection((url, 443), timeout=10) as conn:
            conn = context.wrap_socket(conn, server_hostname=url)
            cert = conn.getpeercert()
            not_after = cert['notAfter']
            print(not_after)
            return not_after
    except (ssl.SSLError, socket.error, KeyError, socket.timeout):
        print("Invalid URL or unable to establish a connection")
        return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None
    
print(get_ssl_certificate_expiration("visiongate.com"))
