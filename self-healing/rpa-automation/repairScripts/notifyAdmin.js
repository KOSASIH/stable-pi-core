// stable-pi-core/self-healing/rpa-automation/repairScripts/notifyAdmin.js

const nodemailer = require('nodemailer'); // For sending emails
const winston = require('winston'); // For logging

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
    // Create a transporter object using SMTP
    const transporter = nodemailer.createTransport({
        host: process.env.SMTP_HOST, // SMTP server host
        port: process.env.SMTP_PORT, // SMTP server port
        secure: process.env.SMTP_SECURE === 'true', // true for 465, false for other ports
        auth: {
            user: process.env.SMTP_USER, // SMTP user
            pass: process.env.SMTP_PASS, // SMTP password
        },
    });

    // Email options
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
 * Notify admin of an issue.
 * @param {string} issueType - The type of issue detected.
 * @param {string} details - Additional details about the issue.
 */
async function notifyAdmin(issueType, details) {
    const subject = `Alert: ${issueType} Detected`;
    const message = `An issue of type "${issueType}" has been detected.\n\nDetails:\n${details}`;
    
    await sendEmailNotification(subject, message);
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
