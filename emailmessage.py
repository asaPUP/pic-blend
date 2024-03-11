import sys
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("Entering emailmessage.py script")

sender_email = "sistemin.uabc@outlook.com"
subject = "SISTEMIN: Your image is ready"
receiver_email = sys.argv[1]
url = sys.argv[2]
message = f"""Hello!
We're sending you this message to let you know that your image is ready.
You can download it from:
{url}"""

print(f"Receiver: {receiver_email}")
print(f"URL: {url}")
print(f"Message: {message}")

smtp_server = "smtp.office365.com"
smtp_port = 587
smtp_username = sender_email
smtp_password = "Sistemin2023!"

try:
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    print("Sending email...")

    # Send message
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context=context)
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print("Email sent successfully.")

except Exception as e:
    print(f"An error occurred while sending the email: {e}")
