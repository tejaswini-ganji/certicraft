import subprocess
import sys
import os
import smtplib
import ssl

import re  # For email validation
from email.message import EmailMessage
from datetime import datetime
import random
import json
import time

# Function to install packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('img2pdf')
install('openpyxl')
install('Pillow')
install('python-dotenv')

from img2pdf import convert
from PIL import Image, ImageDraw, ImageFont
from tkinter.filedialog import askopenfile
from openpyxl import load_workbook
from dotenv import load_dotenv

load_dotenv()

# Email sender credentials
with open("config.json", "r") as file:
    config = json.load(file)

SENDER_EMAIL = config["SENDER_EMAIL"]
SENDER_PASSWORD = config["SENDER_PASSWORD"]

# Check if they are loaded correctly
if not SENDER_EMAIL or not SENDER_PASSWORD:
    raise ValueError("Email or password not found in .env file. Make sure the .env file exists and is properly formatted.")

# Function to validate email
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))


# Open Excel file
file = askopenfile(title='Select the Workbook',mode='r',filetypes=[('Microsoft Excel', '.xlsx .xlsm .xltx .xltm')])
if file is not None:
    dirpath = os.path.dirname(file.name)
else:
    sys.exit()

filepath = file.name

# Create necessary directories
allCertPath = os.path.join(dirpath, "All_Certificates")
allCertImgPath = os.path.join(allCertPath, "Images")
allCertPdfPath = os.path.join(allCertPath, "PDFs")

os.makedirs(allCertImgPath, exist_ok=True)
os.makedirs(allCertPdfPath, exist_ok=True)

wb = load_workbook(filepath, data_only=True)

for ws in wb:
    for r in range(3, 7):  # Start from row 3, assuming row 1 & 2 are headers
        cell = ws.cell(row=r, column=1)  # Read ID column

        if cell.value is None:  
            break  # Stop if no more data

        name = str(ws.cell(row=r, column=2).value).strip().title()  # Get Name
        acm_id = str(ws.cell(row=r, column=1).value).strip().upper()  # Get ID
        email_data = str(ws.cell(row=r, column=5).value).strip().lower()  # Get Emails (comma-separated)

        # Generate a unique certificate ID
        cert_id = f"CERT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"

        # Extract all valid emails
        email_list = [email.strip() for email in email_data.split(',') if is_valid_email(email.strip())]

        if not email_list:
            print(f"Invalid or missing emails for {name} (Row {r}). Skipping email sending.")
            continue  # Skip email sending if no valid email found

        eachmemberIMGpath = os.path.join(allCertImgPath, f"{acm_id}.png")
        eachmemberPDFpath = os.path.join(allCertPdfPath, f"{acm_id}.pdf")

        # Load certificate template
        certificate = Image.open('certificate_template.png')
        draw = ImageDraw.Draw(certificate)
        name_font = ImageFont.truetype('Lora-Bold.ttf', 75)
        cert_id_font = ImageFont.truetype('Lora-Bold.ttf', 40)  # Smaller font for cert ID

        # Center-align name
        bbox = draw.textbbox((0, 0), name, font=name_font)
        w = bbox[2] - bbox[0]  
        h = bbox[3] - bbox[1]  
        left = (certificate.width - w) / 2
        top = 525  

        # Add name to certificate
        draw.text((left, top), name, fill=(75, 75, 75, 255), font=name_font)

        # **Highlighting the part where Certificate ID is added**
        cert_id_bbox = draw.textbbox((0, 0), f"Certificate ID: {cert_id}", font=cert_id_font)
        cert_id_width = cert_id_bbox[2] - cert_id_bbox[0]
        cert_id_x = (certificate.width - cert_id_width) / 2 
        cert_id_y = top + 275
        draw.text((cert_id_x, cert_id_y), f"Certificate ID: {cert_id}", fill=(75, 75, 75, 255), font=cert_id_font)

        # Save certificate image
        certificate = certificate.convert('RGB')
        certificate.save(eachmemberIMGpath)

        # Convert to PDF
        pdf_bytes = convert(eachmemberIMGpath)
        with open(eachmemberPDFpath, "wb") as f:
            f.write(pdf_bytes)

        print(f"Generated certificate for {name}. Sending to {', '.join(email_list)}...")

        # Send email to each valid recipient
        msg = EmailMessage()
        msg["From"] = SENDER_EMAIL
        msg["Subject"] = "Your Certificate"
        msg["Reply-To"] = SENDER_EMAIL
        msg.set_content(f"Dear {name},\n\nPlease find attached your certificate.\nCertificate ID: {cert_id}\n\nBest Regards,\nYour Team")

        # Attach PDF file
        with open(eachmemberPDFpath, "rb") as attachment:
            msg.add_attachment(attachment.read(), maintype="application", subtype="pdf", filename=f"{name}_certificate.pdf")

        # Secure connection with SSL and send emails
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)  # Upgrade to secure TLS connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            for email in email_list:
                msg["To"] = email
                server.send_message(msg)
                print(f"Email sent successfully to {email}")
                time.sleep(10)  # Pause for 10 seconds before sending the next email

wb.save(file.name)
print("Process Completed.")
