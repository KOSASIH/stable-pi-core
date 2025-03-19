# ebs/signal_detector.py

import logging
import random
import time

class SignalDetector:
    def __init__(self):
        logging.info("Signal Detector initialized.")
        self.detection_threshold = 0.1  # Default threshold for signal detection
        self.signal_detected = False

    def set_detection_threshold(self, threshold):
        """
        Set the detection threshold for signals.
        :param threshold: Probability threshold for detecting a signal (0 to 1).
        """
        if 0 <= threshold <= 1:
            self.detection_threshold = threshold
            logging.info(f"Detection threshold set to {self.detection_threshold}.")
        else:
            logging.error("Threshold must be between 0 and 1.")
            raise ValueError("Threshold must be between 0 and 1.")

    def detect_signal(self):
        """
        Simulate the detection of a quantum signal from space.
        :return: A simulated signal or None if no signal is detected.
        """
        # Simulate a random chance of detecting a signal based on the threshold
        detection_probability = random.random()
        logging.debug(f"Detection probability: {detection_probability}, Threshold: {self.detection_threshold}")

        if detection_probability < self.detection_threshold:
            self.signal_detected = True
            signal = "Quantum Signal Detected!"
            logging.info(signal)
            return signal
        else:
            self.signal_detected = False
            logging.info("No signal detected.")
            return None

    def listen_for_signals(self, duration=10):
        """
        Continuously listen for signals for a specified duration.
        :param duration: Duration in seconds to listen for signals.
        """
        end_time = time.time() + duration
        detected_signals = []

        while time.time() < end_time:
            signal = self.detect_signal()
            if signal:
                detected_signals.append(signal)
            time.sleep(1)  # Wait for a second before the next detection attempt

        if detected_signals:
            logging.info(f"Detected signals: {detected_signals}")
        else:
            logging.info("No signals detected during the listening period.")

        return detected_signals
