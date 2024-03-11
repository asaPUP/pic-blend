import sys
import pywhatkit

# Obtiene los argumentos de la linea de comandos (python3 whatsapp.py <phhone_number> <url>)
# Obtains the command line arguments (python3 whatsapp.py <phhone_number> <url>)

if len(sys.argv) < 3:
    print("Missing arguments.")
    sys.exit(1)

phone_number = sys.argv[1]
url = sys.argv[2]

message = f"""Hello!
We send you this message to let you know that your image is ready.
You can download it at:
{url}"""

try:
    pywhatkit.sendwhatmsg_instantly(phone_number, message, 30, True)
    print("WhatsApp message sent!")

except:
    print("An error occurred while sending the WhatsApp message.")