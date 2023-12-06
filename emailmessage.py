import sys
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("Entro al script emailmessage.py")

sender_email = "sistemin.uabc@outlook.com"
subject = "SISTEMIN: Tu imagen está lista"
receiver_email = sys.argv[1]
url = sys.argv[2]
message = f"""¡Hola!
Te enviamos este mensaje para avisarte que tu imagen está lista.
Puedes descargarla en:
{url}"""

print(f"Receptor: {receiver_email}")
print(f"URL: {url}")
print(f"Mensaje: {message}")

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

    print("Enviando correo electrónico...")

    # Send message
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context=context)
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print("Correo electrónico enviado exitosamente.")

except Exception as e:
    print(f"Ocurrió un error al enviar el correo electrónico: {e}")