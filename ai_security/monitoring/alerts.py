import logging
import smtplib
from email.mime.text import MIMEText

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Send an email alert
def send_email_alert(subject, message, recipient_email):
    logging.info("Sending email alert...")
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = 'your_email@example.com'  # Replace with your email
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:  # Replace with your SMTP server
            server.starttls()
            server.login('your_email@example.com', 'your_password')  # Replace with your email and password
            server.send_message(msg)
            logging.info("Email alert sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email alert: {e}")

# Trigger an alert
def trigger_alert(data):
    subject = "Fraud Alert Detected"
    message = f"Suspicious activity detected: {data}"
    recipient_email = "recipient@example.com"  # Replace with the recipient's email
    send_email_alert(subject, message, recipient_email)

if __name__ == "__main__":
    # Example usage
    example_data = {
        'amount': 1500,
        'time_of_day': '16:00',
        'location': 'New York',
        'is_fraud': 1
    }
    trigger_alert(example_data)
