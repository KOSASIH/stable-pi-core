# payment_system/app.py

from flask import Flask, render_template
from payment_routes import payment_routes

app = Flask(__name__)

# Register payment routes
app.register_blueprint(payment_routes)

@app.route('/')
def index():
    return render_template('payment_form.html')

if __name__ == '__main__':
    app.run(port=5000)
