from quickbooks import QuickBooks
import requests
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from dotenv import load_dotenv
import os
import pandas as pd
import logging

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or 'secret_key_here'
app.config['TEMPLATES_AUTO_RELOAD'] = True

login_manager = LoginManager()
login_manager.init_app(app)

# Logging configuration
logging.basicConfig(level=logging.DEBUG)

# Dummy user for authentication
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def home():
    return render_template('index.html')

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

# Refresh token function to get a new access token when expired
def refresh_access_token():
    url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
    auth_header = f"Basic {os.getenv('CLIENT_ID')}:{os.getenv('CLIENT_SECRET')}"
    
    headers = {
        "Authorization": auth_header,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": os.getenv("REFRESH_TOKEN")
    }
    
    response = requests.post(url, headers=headers, data=payload)
    token_info = response.json()
    
    if response.status_code == 200:
        new_access_token = token_info['access_token']
        new_refresh_token = token_info.get('refresh_token', os.getenv("REFRESH_TOKEN"))  # May not always return a new refresh token
        
        # Update the environment with the new tokens
        os.environ['ACCESS_TOKEN'] = new_access_token
        os.environ['REFRESH_TOKEN'] = new_refresh_token

        # Save new tokens to the Render environment
        logging.info(f"Access token refreshed successfully. New access token: {new_access_token}")
        
        return new_access_token
    else:
        logging.error("Error refreshing access token")
        return None

# Function to retrieve access token, refresh it if needed
def get_access_token():
    access_token = os.getenv('ACCESS_TOKEN')
    if access_token is None or len(access_token) == 0:
        return refresh_access_token()
    return access_token

# Query QuickBooks API for products
def query_quickbooks(query):
    realm_id = os.getenv('REALM_ID')  # Ensure to set your realm ID in the environment
    api_url = f"https://quickbooks.api.intuit.com/v3/company/{realm_id}/query"
    access_token = get_access_token()
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    
    sql_query = f"SELECT * FROM Item WHERE Name LIKE '{query}%'"
    params = {'query': sql_query}
    
    response = requests.get(api_url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        products = [item['Name'] for item in data.get('QueryResponse', {}).get('Item', [])]
        return products
    else:
        logging.error(f"Error fetching products: {response.status_code}")
        return []

@app.route('/autocomplete', methods=['GET'])
@login_required
def autocomplete():
    query = request.args.get('q')
    suggestions = query_quickbooks(query)
    return jsonify(suggestions)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        item = request.form['item']
        orders = query_quickbooks(item)
        
        # Create a CSV file with customer details and order history
        df = pd.DataFrame(orders)
        csv_path = 'customer_orders.csv'
        df.to_csv(csv_path, index=False)

        return send_file(csv_path, as_attachment=True)
    return render_template('search.html')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)