import React from 'react';
import './Notification.css'; // Add styles for notifications

const Notification = ({ type, message }) => {
    return (
        <div className={`notification ${type}`}>
            {message}
        </div>
    );
};

export default Notification;
