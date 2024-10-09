from flask import Flask, render_template, redirect, url_for, request, session, jsonify, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or 'secret_key_here'

login_manager = LoginManager()
login_manager.init_app(app)

# Dummy user for authentication
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == os.getenv('PASSWORD'):
            user = User(id=1)
            login_user(user)
            return redirect(url_for('search'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/autocomplete', methods=['GET'])
@login_required
def autocomplete():
    query = request.args.get('q')
    # Call QuickBooks API to get product suggestions here
    suggestions = ['Product1', 'Product2']  # Dummy data
    return jsonify(suggestions)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        item = request.form['item']
        # Call QuickBooks API to retrieve customers and orders for the selected item
        orders = query_quickbooks(item)  # Implement QuickBooks query here

        # Create a CSV file with customer details and order history
        df = pd.DataFrame(orders)
        csv_path = 'customer_orders.csv'
        df.to_csv(csv_path, index=False)

        return send_file(csv_path, as_attachment=True)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)