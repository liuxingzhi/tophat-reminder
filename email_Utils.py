from email.message import EmailMessage
import smtplib


def send_email_message(sender, receivers, content, subject=None):
    # creates SMTP session, for gmail, use 465
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    # Authentication
    server.login("courselytest@gmail.com", "course2019")

    # message to be sent
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receivers
    msg.set_content(content)

    server.send_message(msg)

    # terminating the session
    server.quit()


if __name__ == '__main__':
    sender = "courselytest@gmail.com"
    receivers = ["abelliu2018@gmail.com"]
    content = "就是没有提示？"
    send_email_message(sender, receivers, content, subject="再试一次")
