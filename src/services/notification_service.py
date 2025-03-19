import asyncio
import aiohttp
import logging
from jinja2 import Template
from email.mime.text import MIMEText
from twilio.rest import Client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, notification_channels: dict):
        """
        Initialize the NotificationService with a dictionary of notification channels.
        :param notification_channels: A dictionary where keys are channel names and values are channel configurations.
        """
        self.notification_channels = notification_channels
        self.templates = {}

    async def send_notification(self, channel: str, recipient: str, template_name: str, data: dict):
        """
        Send a notification to the specified recipient through the specified channel.
        :param channel: The channel to use for sending the notification.
        :param recipient: The recipient of the notification.
        :param template_name: The name of the template to use for rendering the notification content.
        :param data: The data to use for rendering the notification content.
        """
        channel_config = self.notification_channels.get(channel)
        if not channel_config:
            logger.error(f"No configuration found for channel: {channel}")
            return

        template = self.templates.get(template_name)
        if not template:
            logger.error(f"No template found for name: {template_name}")
            return

        try:
            rendered_content = template.render(data)
            if channel == 'email':
                await self.send_email(recipient, rendered_content, channel_config)
            elif channel == 'sms':
                await self.send_sms(recipient, rendered_content, channel_config)
            elif channel == 'in-app':
                await self.send_in_app_notification(recipient, rendered_content, channel_config)
            logger.info(f"Notification sent to {recipient} through {channel}")
        except Exception as e:
            logger.error(f"Error sending notification to {recipient} through {channel}: {e}")

    async def send_email(self, recipient: str, content: str, channel_config: dict):
        """
        Send an email notification to the specified recipient.
        :param recipient: The recipient of the email notification.
        :param content: The content of the email notification.
        :param channel_config: The configuration for the email channel.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(channel_config['url'], data={'recipient': recipient, 'content': content}) as response:
                response.raise_for_status()

    async def send_sms(self, recipient: str, content: str, channel_config: dict):
        """
        Send an SMS notification to the specified recipient.
        :param recipient: The recipient of the SMS notification.
        :param content: The content of the SMS notification.
        :param channel_config: The configuration for the SMS channel.
        """
        account_sid = channel_config['account_sid']
        auth_token = channel_config['auth_token']
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=content,
            from_=channel_config['from_number'],
            to=recipient
        )

    async def send_in_app_notification(self, recipient: str, content: str, channel_config: dict):
        """
        Send an in-app notification to the specified recipient.
        :param recipient: The recipient of the in-app notification.
        :param content: The content of the in-app notification.
        :param channel_config: The configuration for the in-app channel.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(channel_config['url'], data={'recipient': recipient, 'content': content}) as response:
                response.raise_for_status()

    def load_templates(self, template_dir: str):
        """
        Load notification templates from the specified directory.
        :param template_dir: The directory containing the notification templates.
        """
        import os
        for filename in os.listdir(template_dir):
            if filename.endswith('.j2'):
                template_name = os.path.splitext(filename)[0]
                with open(os.path.join(template_dir, filename), 'r') as file:
                    template_content = file.read()
                    self.templates[template_name] = Template(template_content)

# Example usage
async def main():
    notification_channels = {
        'email': {'url': 'https://example.com/email'},
        'sms': {'account_sid': 'your_account_sid', 'auth_token': 'your_auth_token', 'from_number': 'your_from_number'},
        'in-app': {'url': 'https://example.com/in-app'}
    }
    notification_service = NotificationService(notification_channels)
    notification_service.load_templates('templates')

    await notification_service.send_notification('email', 'recipient@example.com', 'hello', {'name': 'John'})
    await notification_service.send_notification('sms', '+1234567890', 'hello', {'name': 'John'})
    await notification_service.send_notification('in-app', 'recipient@example.com', 'hello', {'name': 'John'})

if __name__ == "__main__":
    asyncio.run(main())
