# Import the 'requests' library to make HTTP requests
import requests

# Define the ID of the cryptocurrency you want to check (e.g., "bitcoin")
coin_id = "bitcoin"

# Define the fiat currency you want the price in (e.g., "usd")
currency = "usd"

# Build the URL for the CoinGecko API to fetch the current price
url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}"

# Send a GET request to the API and parse the response as JSON
data = requests.get(url).json()

# Extract the specific coin's price from the JSON structure
coin_price = data[coin_id][currency]

# Print the coin's current price
print(coin_price)
