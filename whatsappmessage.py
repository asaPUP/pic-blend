import sys
import pywhatkit

# Obtiene los argumentos de la linea de comandos (python3 whatsapp.py <phhone_number> <url>)

if len(sys.argv) < 3:
    print("Faltan argumentos.")
    sys.exit(1)

phone_number = sys.argv[1]
url = sys.argv[2]

message = f"""¡Hola!
Te enviamos este mensaje para avisarte que tu imagen está lista.
Puedes descargarla en:
{url}"""

try:
    pywhatkit.sendwhatmsg_instantly(phone_number, message, 30, True)
    print("Mensaje de WhatsApp enviado!")

except:
    print("Ocurrió un error al enviar el mensaje de WhatsApp.")