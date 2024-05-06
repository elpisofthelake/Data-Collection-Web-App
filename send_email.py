from email.mime.text import MIMEText
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(email,ani_name, max_anime):
    from_email = os.getenv('send_email')
    from_password = os.getenv('password')
    to_email = email

    subject = "Anime name"
    message = f"Hello, your favourite anime is {ani_name} and the most popular anime is {max_anime}"

    

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)