import requests
import pandas as pd

# WooCommerce API credentials
consumer_key = 'ck_7822d16ee5153756e6d5f0bbfcef3e9ec1d19f0d'
consumer_secret = 'cs_db796e329d7a7d32acf244b6cc0cffc21a6d01dd'
api_url = "https://southernwines.com/wp-json/wc/v3/orders"

# Parameters for the API request
params = {
    'per_page': 100,  # Max number of orders per page (100 is the limit)
    'after': '2023-04-03T00:00:00',  # Fetch orders after April 3, 2023
    'page': 1  # Start with the first page
}

# List to store all the orders
all_orders = []

# Fetch all pages of orders
while True:
    # API request to fetch orders for the current page
    response = requests.get(api_url, auth=(consumer_key, consumer_secret), params=params)

    # Check if the request was successful
    if response.status_code == 200:
        orders = response.json()

        # Break the loop if no more orders are returned
        if not orders:
            break

        # Append the current batch of orders to the list
        all_orders.extend(orders)

        # Move to the next page
        params['page'] += 1
    else:
        print(f"Failed to retrieve orders. Status code: {response.status_code}")
        break

# List to store order details for the CSV
order_data = []

# Loop through each order and extract relevant details
for order in all_orders:
    email = order['billing']['email']  # Customer's email
    order_date = order['date_created']  # Date of the order
    products = ", ".join([item['name'] for item in order['line_items']])  # Product names
    
    # Append the extracted data to the list
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