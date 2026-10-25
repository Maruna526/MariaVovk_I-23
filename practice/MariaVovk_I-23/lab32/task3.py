
# Maria Vovk, I-23
import qrcode
from pathlib import Path

name = "Maria Vovk"
group = "I-23"
email = "vovkmaria1202@gmail.com"

contact = f"Name: {name}\nGroup: {group}\nEmail: {email}"

img = qrcode.make(contact)
output_path = Path(__file__).resolve().parent / "contact.png"
img.save(output_path)

print("QR-код збережено у файлі contact.png")
print(contact)
