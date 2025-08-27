from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import read_user_inputs as readUserInputs

def send_email_with_attachment(attachment_paths):
    input = readUserInputs.getInputs();
    from_address = input['from_address'];
    app_password = input['app_password'];
    recipients = input['recipients'];
    # Create the email object
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = ', '.join(recipients)
    strDate = datetime.now().strftime("%d%m%Y_%H%M%S")

    JOB_NAME = "BSE Data Summary"
    formatted_date = strDate.split("_")[0]
    formatted_time = strDate.split("_")[1]
    
    # Email body
    msg['Subject'] = f"Scheduled Job Completed – {JOB_NAME} | {formatted_date} {formatted_time}";

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <p>Dear User,</p>
        <p>The scheduled job <strong>{JOB_NAME}</strong> has completed successfully on 
        <strong>{formatted_date} at {formatted_time} IST</strong>.</p>
        <p>Please find the attached output file for your reference.</p>
        <br>
        <p>Regards,<br>
        <em>Automation Script</em></p>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_body, 'html'))

    # Attach multiple files
    for file_path in attachment_paths:
        print("Attaching file:", file_path)
        try:
            with open(file_path, "rb") as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{file_path.split("//")[-1]}"')
                msg.attach(part)
        except Exception as e:
            print(f"Failed to attach {file_path}: {e}")

    # Send the email via Gmail's SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_address, app_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")