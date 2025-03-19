// stable-pi-core/self-healing/rpa-automation/repairScripts/notifyAdmin.js

const nodemailer = require('nodemailer'); // For sending emails
const winston = require('winston'); // For logging
const axios = require('axios'); // For sending HTTP requests (e.g., to Slack or Discord)

// Configure logging
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ filename: 'notifyAdmin.log' }),
        new winston.transports.Console()
    ]
});

/**
 * Sends an email notification to the admin.
 * @param {string} subject - The subject of the email.
 * @param {string} message - The message body of the email.
 */
async function sendEmailNotification(subject, message) {
    const transporter = nodemailer.createTransport({
        host: process.env.SMTP_HOST, // SMTP server host
        port: process.env.SMTP_PORT, // SMTP server port
        secure: process.env.SMTP_SECURE === 'true', // true for 465, false for other ports
        auth: {
            user: process.env.SMTP_USER, // SMTP user
            pass: process.env.SMTP_PASS, // SMTP password
        },
    });

    const mailOptions = {
        from: process.env.SMTP_FROM, // Sender address
        to: process.env.ADMIN_EMAIL, // List of recipients
        subject: subject,
        text: message,
    };

    try {
        const info = await transporter.sendMail(mailOptions);
        logger.info('Email sent: %s', info.messageId);
    } catch (error) {
        logger.error('Error sending email:', error);
    }
}

/**
 * Sends a message to a Slack channel.
 * @param {string} message - The message to send.
 */
async function sendSlackNotification(message) {
    const slackWebhookUrl = process.env.SLACK_WEBHOOK_URL;

    try {
        await axios.post(slackWebhookUrl, { text: message });
        logger.info('Slack notification sent successfully.');
    } catch (error) {
        logger.error('Error sending Slack notification:', error);
    }
}

/**
 * Sends a message to a Discord channel.
 * @param {string} message - The message to send.
 */
async function sendDiscordNotification(message) {
    const discordWebhookUrl = process.env.DISCORD_WEBHOOK_URL;

    try {
        await axios.post(discordWebhookUrl, { content: message });
        logger.info('Discord notification sent successfully.');
    } catch (error) {
        logger.error('Error sending Discord notification:', error);
    }
}

/**
 * Notify admin of an issue.
 * @param {string} issueType - The type of issue detected.
 * @param {string} details - Additional details about the issue.
 */
async function notifyAdmin(issueType, details) {
    const subject = `Alert: ${issueType} Detected`;
    const message = `An issue of type "${issueType}" has been detected.\n\nDetails:\n${details}`;

    // Send notifications
    await sendEmailNotification(subject, message);
    await sendSlackNotification(message);
    await sendDiscordNotification(message);
}

// Example usage
if (require.main === module) {
    const issueType = process.argv[2]; // Get the issue type from command line arguments
    const details = process.argv[3]; // Get additional details from command line arguments

    if (!issueType || !details) {
        logger.error('Issue type and details are required as command line arguments.');
        process.exit(1);
    }
    
    notifyAdmin(issueType, details);
}

module.exports = notifyAdmin;
