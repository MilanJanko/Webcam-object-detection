import smtplib
from email.message import EmailMessage
import imghdr
from envvar import username, password, receiver


def send_email(image_path):
    email_message = EmailMessage()
    email_message['Subject'] = 'New Object showed up!'
    email_message.set_content('Your webcam detected new object, '
                              'attached in the email below.')

    with open(image_path, 'rb') as file:
        content = file.read()

    email_message.add_attachment(content, maintype='image',
                                 subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(username, password)
    gmail.sendmail(username, receiver, msg=email_message.as_string())
    gmail.quit()


if __name__ == '__main__':
    send_email("images/19.png")

