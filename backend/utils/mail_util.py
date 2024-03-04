import random
import string
import smtplib
from email.mime.text import MIMEText

verification_codes = {}

def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def send_verification_code(email, code):
    sender_email = 'philnicient@gmail.com'
    sender_password = 'iptn yepq feta yeel'

    message_body = f"Hello,\n\nYou recently requested a password reset for your account. "\
                   f"Please use the following verification code to proceed:\n\n"\
                   f"Verification Code: {code}\n\n"\
                   f"If you did not request this password reset, please disregard this email "\
                   f"and ensure your account security.\n\n"\
                   f"Thank you."

    message = MIMEText(message_body)
    message['Subject'] = 'Password Reset Verification Code'
    message['From'] = sender_email
    message['To'] = email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(message)
    
    verification_codes[email] = code
