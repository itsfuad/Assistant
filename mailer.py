import smtplib
from bot import bot, MY_CHAT_ID
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv
load_dotenv()

# login credentials
smtp2go_username = os.getenv('SMTP2GO_USERNAME')
smtp2go_password = os.getenv('SMTP2GO_PASSWORD')

# create SMTP session
smtp_server = 'mail.smtp2go.com'
smtp_port = 587

# create message
from_email = 'fuad@programmer.net'

def sendEmail(recipient, subject, body, file_info=None, auto_reply=False):
    to_email = recipient
    subject = subject
    # send message and handle errors
    try:
        print('Logging in...')
        
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as session:
            print('Connected to SMTP server!')
            session.ehlo()
            print('Starting TLS...')
            session.starttls()
            print('TLS started!')
            session.login(smtp2go_username, smtp2go_password)
            print('Email Login Successful!')

            # create a MIMEMultipart object to hold the message and attachments
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = from_email
            msg['To'] = to_email
            msg.attach(MIMEText(body))
            
            # loop through each file info and attach it to the message
            if file_info:
                file = bot.download_file(file_info.file_path)
                filename = file_info.file_path.split('/')[-1]
                attachment = MIMEApplication(file)
                attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(attachment)
                    
            session.sendmail(from_email, to_email, msg.as_string())

            print('Email sent!')

            if auto_reply:
                bot.send_message(MY_CHAT_ID, 'Auto reply sent!😎')
            else:
                bot.send_message(MY_CHAT_ID, 'Email sent!😎')

    except smtplib.SMTPException as e:
        print(f"SMTP Exception: {e}")
        handle_email_error(e, auto_reply)

    except Exception as e:
        print(f"Unexpected Exception: {e}")
        handle_email_error(e, auto_reply)


def handle_email_error(error, auto_reply):
    if auto_reply:
        bot.send_message(MY_CHAT_ID, 'Auto reply failed! Sorry..😢')
        bot.send_message(MY_CHAT_ID, f'This is the error I got: {error}')
    else:
        bot.send_message(MY_CHAT_ID, 'Email sending failed! Sorry..😢')
        bot.send_message(MY_CHAT_ID, f'This is the error I got: {error}')