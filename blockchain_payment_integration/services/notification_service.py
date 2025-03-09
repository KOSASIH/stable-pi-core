import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, smtp_server, smtp_port, smtp_user, smtp_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    def send_email(self, to_email, subject, body):
        """Send an email notification."""
        msg = MIMEMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            logger.info("Email sent successfully to: %s", to_email)
        except Exception as e:
            logger.error("Failed to send email to %s: %s", to_email, e)

    def notify_payment_status(self, user_email, payment_id, status):
        """Notify the user about the payment status."""
        subject = f"Payment Status Update: {payment_id}"
        body = f"Your payment with ID {payment_id} is now {status}."
        self.send_email(user_email, subject, body)
