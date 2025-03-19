# Multi-Currency Payment System

This project implements a multi-currency payment system using Stripe, allowing users to make payments in various fiat and cryptocurrency options. The system is designed to be integrated into the **stable-pi-core** project, providing a seamless payment experience.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The multi-currency payment system allows users to select their preferred currency and process payments securely using the Stripe API. This system supports various currencies, including USD, EUR, GBP, and cryptocurrencies like Bitcoin.

## Features

- **Multi-Currency Support**: Users can select from multiple fiat and cryptocurrency options.
- **Secure Payments**: Utilizes Stripe for secure payment processing.
- **User -Friendly Interface**: Simple and intuitive HTML form for payment selection.
- **Real-Time Payment Confirmation**: Users receive immediate feedback on payment success or failure.

## Technologies Used

- **Python**: The primary programming language for the backend.
- **Flask**: A lightweight web framework for building the application.
- **Stripe**: Payment processing API for handling transactions.
- **HTML/CSS/JavaScript**: For the frontend user interface.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/KOSASIH/stable-pi-core.git
   cd stable-pi-core/payment_system
   ```

2. **Create a Virtual Environment (Optional but Recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Stripe API Keys**:
   - Replace `YOUR_STRIPE_SECRET_KEY` and `YOUR_STRIPE_PUBLIC_KEY` in `payment_routes.py` and `payment.js` with your actual Stripe API keys.

## Usage

1. **Run the Application**:
   ```bash
   python app.py
   ```

2. **Access the Payment Form**:
   Open your web browser and navigate to `http://localhost:5000` to access the payment form.

3. **Make a Payment**:
   - Select your preferred currency from the dropdown menu.
   - Click the "Pay" button to initiate the payment process.
   - Follow the prompts to complete the payment.

## Directory Structure

```
stable-pi-core/
│
├── payment_system/                   # Directory for the payment system
│   ├── __init__.py                   # Makes payment_system a package
│   ├── app.py                        # Main application file for the payment system
│   ├── payment_routes.py             # Routes for handling payment requests
│   ├── payment_processor.py           # Logic for processing payments
│   ├── templates/                    # Directory for HTML templates
│   │   ├── payment_form.html         # HTML form for payment
│   ├── static/                       # Directory for static files (CSS, JS)
│   │   ├── js/
│   │   │   ├── payment.js            # JavaScript for handling payment interactions
│   ├── requirements.txt              # Python dependencies for the payment system
│   └── README.md                     # Documentation for the payment system
│
├── main.py                           # Main entry point for the stable-pi-core project
└── ...
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
