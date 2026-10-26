from pathlib import Path
import qrcode

print("Nazar Tarasiuk, I-23")

NAME = "Nazar Tarasiuk"
GROUP = "I-23"
EMAIL = "gmail@gmail.com"

if EMAIL == "gmail@gmail.com" or "@" not in EMAIL:
    raise ValueError("Replace EMAIL with your real email address")

text = f"{NAME}, {GROUP}, {EMAIL}"

output_file = Path(__file__).resolve().parent / "contact.png"
image = qrcode.make(text)
image.save(output_file)

print(f"saved: {output_file.name}")