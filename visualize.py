import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the database
conn = sqlite3.connect("portfolio.db")

# Load all data into a pandas DataFrame
df = pd.read_sql_query("SELECT * FROM investments", conn)

# Close connection
conn.close()

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Convert 'sell' from 1/0 to -1/1 for plotting (buy = +, sell = -)
df["signed_amount"] = df["amount"] * df["sell"].apply(lambda x: -1 if x == 1 else 1)

# Plot
plt.figure(figsize=(10, 5))
for coin in df["coin_id"].unique():
    coin_data = df[df["coin_id"] == coin]
    plt.plot(coin_data["date"], coin_data["signed_amount"].cumsum(), marker="o", label=coin)

plt.title("Crypto Investment Value Over Time")
plt.xlabel("Date")
plt.ylabel("Cumulative Amount")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
