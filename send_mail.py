import smtplib
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
receiver_emails = pd.read_csv('csv_file.csv') #read file
receiver_emails = receiver_emails.loc[:,"E-mail"]  # get the column named "E-mail  inside csv"
receiver_emails=receiver_emails.dropna() #remove nan values if any
receiver_emails=receiver_emails.to_list() #convert to a list

# Email details
sender_email = "trial@trial.com"
cc_emails = ["cc@cc.com"]
all_emails=receiver_emails+cc_emails

subject = "Testing"
html_message = """
<html>
<body>
    
    I am the Best<br>

<a href="https://bbc.com/">BBC</a><br>
<br>
</body>
</html>
"""

image_path = "path/image.jpg" 
pdf_path = "path/file.pdf"


def send_mail():
    print("Attempting to send email...")  # Log for debug

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ','.join(receiver_emails)
    msg['Cc'] = ','.join(cc_emails)
    msg['Subject'] = subject


    # Attach HTML body
    msg.attach(MIMEText(html_message, 'html'))
#------------------------------------------------FOR PDF/IMAGES attachment--------------------------------------
    # Attach the image
    try:
        with open(image_path, 'rb') as img:
            mime_image = MIMEImage(img.read())
            mime_image.add_header('Content-Disposition', 'attachment', filename="meme.jpg")
            msg.attach(mime_image)
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")

        # Attach the PDF file
    try:
        with open(pdf_path, 'rb') as pdf_file:
            mime_base = MIMEBase('application', 'pdf')
            mime_base.set_payload(pdf_file.read())
            encoders.encode_base64(mime_base)  # Encode PDF file as base64
            mime_base.add_header('Content-Disposition', 'attachment', filename="example.pdf")
            msg.attach(mime_base)
        print("PDF attached successfully.")
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
#----------------------------------------------------------------------------------------------------------------
    # Send the email
    try:
        server = smtplib.SMTP("0.0.0.0", 25)   #IP Address of SMTP Server with port number
        server.sendmail(sender_email, all_emails, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

# Scheduling
my_time="17:30"

days = [
            schedule.every().monday, 
            schedule.every().tuesday,
            schedule.every().wednesday,
            schedule.every().thursday,
            schedule.every().friday
            ]
for day in days:
    day.at(my_time).do(send_mail)  


# Keep the script running to check the schedule
print("Scheduler is running...")
while True:
    schedule.run_pending()
    time.sleep(60)
