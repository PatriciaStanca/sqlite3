# Import the 'requests' module to make HTTP requests
import requests

# Import the 'click' module to create command-line interface (CLI) commands
import click

# Define a CLI command using the Click decorator
@click.command()
# Define an option for the coin ID with a default value of "bitcoin"
@click.option("--coin_id", default="bitcoin")
# Define an option for the currency with a default value of "usd"
@click.option("--currency", default="usd")
def get_coin_price(coin_id, currency):
    # Construct the API URL to get the price of the specified coin in the specified currency
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}"
    
    # Send a GET request to the API and convert the response to JSON
    data = requests.get(url).json()
    
    # Extract the price of the coin from the JSON response
    coin_price = data[coin_id][currency]
    
    # Print the result with 2 decimal places, in uppercase currency (e.g., USD)
    print(f"The price of {coin_id} is {coin_price:.2f} {currency.upper()}")

# This ensures the CLI command runs only when the script is executed directly
if __name__ == "__main__": 
    get_coin_price()
