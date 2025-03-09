// payment_system/static/js/payment.js

const stripe = Stripe('YOUR_STRIPE_PUBLIC_KEY'); // Replace with your Stripe public key

document.getElementById('payment-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const currency = document.getElementById('currency').value;

    // Make a request to the server to create a payment intent
    const response = await fetch('/create-payment-intent', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ currency }),
    });

    const { clientSecret } = await response.json();

    // Confirm the payment using Stripe
    const result = await stripe.confirmCardPayment(clientSecret);

    if (result.error) {
        // Show error to your customer
        document.getElementById('payment-result').innerText = result.error.message;
    } else {
        // Payment succeeded
        document.getElementById('payment-result').innerText = 'Payment successful!';
    }
});
