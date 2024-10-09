import requests
import base64

# QuickBooks API credentials
client_id = 'ABwEFkI3FaaF0U2nEVgQM9MkPhIDkAzUbxxfRjd0jHzk80mnyG'
client_secret = 'ZWJLcJ4gwx0MJegqhQiQO7vzPa67S88SLVOOuyli'
refresh_token = 'AB11737230662DiDqH5qhJmoRNCf3SNGUahe6iG4p6hHdwJlg3'
company_id = '9130354953631806'  # Your QuickBooks Company ID

# Encode the client_id and client_secret as Base64
encoded_credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

# Step 1: Refresh the Access Token
url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {encoded_credentials}"
}
data = {
    "grant_type": "refresh_token",
    "refresh_token": refresh_token
}

response = requests.post(url, headers=headers, data=data)

# Step 2: Check if token was refreshed successfully
if response.status_code == 200:
    tokens = response.json()
    access_token = tokens['access_token']
    print("New Access Token:", access_token)
    
    # Now make requests to QuickBooks API using the new Access Token

    # Example: Fetch customers or invoices
    query_url = f"https://quickbooks.api.intuit.com/v3/company/{company_id}/query"
    query = "SELECT * FROM Invoice WHERE Line.Description LIKE '%Kanonkop Paul Sauer%' OR Line.Description LIKE '%Kanoncop Cabernet Sauvignon%'"
    query_headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    invoice_response = requests.get(f"{query_url}?query={query}", headers=query_headers)
    
    # Process the response and save data to CSV
    if invoice_response.status_code == 200:
        invoices = invoice_response.json()
        # You can add logic to process and save data here
        print("Invoices found:", invoices)
    else:
        print(f"Failed to retrieve invoices. Status code: {invoice_response.status_code}")
else:
    print(f"Failed to refresh token. Status code: {response.status_code}")