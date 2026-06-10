import smtplib
import os
import glob
from email.message import EmailMessage
import config

SENDER_EMAIL = config.SENDER_EMAIL
RECEIVER_EMAIL = config.RECEIVER_EMAIL
APP_PASSWORD = config.APP_PASSWORD

def send_error_email(error_summary):
    # Find the latest log file in the /logs directory
    log_dir = "logs"
    list_of_files = glob.glob(os.path.join(log_dir, "*.log"))
    
    latest_log = None
    if list_of_files:
        latest_log = max(list_of_files, key=os.path.getctime)

    # Setup the Email
    msg = EmailMessage()
    msg["Subject"] = "🚨 Scraper Alert: Budget Query Error"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.set_content(f"The scraper crashed. Summary:\n\n{error_summary}\n\nSee the attached log for full details.")

    # Attach the log file (if it exists)
    if latest_log:
        with open(latest_log, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(latest_log)
            
        msg.add_attachment(
            file_data,
            maintype='application',
            subtype='octet-stream',
            filename=file_name
        )

    # Send it
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")