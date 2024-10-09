import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# WooCommerce API credentials
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
api_url = os.getenv('API_URL')

# Parameters for the API request
params = {
    'per_page': 100,
    'after': '2023-04-03T00:00:00',
    'page': 1
}

# List to store all the orders
all_orders = []

# Fetch all pages of orders
while True:
    response = requests.get(api_url, auth=(consumer_key, consumer_secret), params=params)
    
    if response.status_code == 200:
        orders = response.json()
        if not orders:
            break
        all_orders.extend(orders)
        params['page'] += 1
    else:
        print(f"Failed to retrieve orders. Status code: {response.status_code}")
        break

# List to store order details for the CSV
order_data = []

# Loop through each order and extract relevant details
for order in all_orders:
    email = order['billing']['email']
    order_date = order['date_created']
    products = ", ".join([item['name'] for item in order['line_items']])
    
    order_data.append({
        'Customer Email': email,
        'Order Date': order_date,
        'Products': products
    })

# Create a DataFrame from the list
df = pd.DataFrame(order_data)

# Save the DataFrame to a CSV file
df.to_csv('woocommerce_orders.csv', index=False)

print(f"Data has been successfully written to woocommerce_orders.csv. Total orders: {len(all_orders)}")