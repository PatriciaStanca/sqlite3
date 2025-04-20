import sqlite3
import requests
import click
import datetime
import csv
from dataclasses import dataclass

# SQL: Create investments table if it doesn't exist
CREATE_INVESTMENTS_SQL = """
CREATE TABLE IF NOT EXISTS investments (
    coin_id TEXT,
    currency TEXT,
    amount REAL,
    sell INT,
    date TIMESTAMP
);
"""

# Dataclass for investment entries
@dataclass
class Investment:
    coin_id: str
    currency: str
    amount: float
    sell: bool
    date: datetime.datetime

    def compute_value(self) -> float:
        return self.amount * get_coin_price(self.coin_id, self.currency)

# Factory function to map DB rows to Investment objects
def investment_row_factory(_, row):
    return Investment(
        coin_id=row[0],
        currency=row[1],
        amount=row[2],
        sell=bool(row[3]),
        date=datetime.datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S.%f")
    )

# === Fetch current price from CoinGecko ===
def get_coin_price(coin_id, currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}"
    response = requests.get(url)
    data = response.json()
    coin_price = data[coin_id][currency]
    print(f"The price of {coin_id} is {coin_price:.2f} {currency.upper()}")
    return coin_price

# === CLI Setup ===
@click.group()
def cli():
    pass

# === 1. Show price ===
@click.command()
@click.option("--coin_id", default="bitcoin", help="Coin ID (e.g., bitcoin)")
@click.option("--currency", default="usd", help="Currency (e.g., usd)")
def show_coin_price(coin_id, currency):
    get_coin_price(coin_id, currency)

# === 2. Add investment ===
@click.command()
@click.option("--coin_id", required=True)
@click.option("--currency", required=True)
@click.option("--amount", required=True, type=float)
@click.option("--sell", is_flag=True, help="Set if this is a sell")
def add_investment(coin_id, currency, amount, sell):
    sql = "INSERT INTO investments VALUES (?, ?, ?, ?, ?);"
    values = (coin_id, currency, amount, int(sell), datetime.datetime.now())
    cursor.execute(sql, values)
    database.commit()
    print(f"Added {'sell' if sell else 'buy'} of {amount} {coin_id}")

# === 3. Calculate total holdings ===
@click.command()
@click.option("--coin_id", required=True)
@click.option("--currency", required=True)
def get_investment_value(coin_id, currency):
    coin_price = get_coin_price(coin_id, currency)
    sql = "SELECT * FROM investments WHERE coin_id=? AND currency=? AND sell=?;"
    buys = cursor.execute(sql, (coin_id, currency, 0)).fetchall()
    sells = cursor.execute(sql, (coin_id, currency, 1)).fetchall()
    buy_amount = sum(row.amount for row in buys)
    sell_amount = sum(row.amount for row in sells)
    total = buy_amount - sell_amount
    print(f"You own a total of {total} {coin_id} worth {total * coin_price:.2f} {currency.upper()}")

# === 4. Import from CSV ===
@click.command()
@click.option("--csv_file", required=True)
def import_investments(csv_file):
    with open(csv_file, "r") as f:
        rdr = csv.reader(f)
        try:
            next(rdr)  # Skip header
        except StopIteration:
            print("CSV file is empty.")
            return

        rows = []
        for row in rdr:
            if len(row) != 5:
                print(f"Skipping invalid row: {row}")
                continue
            coin, curr, amt, sell, date = row
            try:
                rows.append((coin, curr, float(amt), int(sell), date))
            except ValueError:
                print(f"Failed to convert row: {row}")

        if not rows:
            print("No valid rows to import.")
            return

        sql = "INSERT INTO investments VALUES (?, ?, ?, ?, ?);"
        cursor.executemany(sql, rows)
        database.commit()
        print(f"Imported {len(rows)} investments from {csv_file}")

# === 5. Export to CSV ===
@click.command()
@click.option("--csv_file", required=True)
def export_investments(csv_file):
    cursor.execute("SELECT * FROM investments;")
    rows = cursor.fetchall()
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["coin_id", "currency", "amount", "sell", "date"])
        writer.writerows(rows)
    print(f"Exported {len(rows)} investments to {csv_file}")

# === Register CLI commands ===
cli.add_command(show_coin_price)
cli.add_command(add_investment)
cli.add_command(get_investment_value)
cli.add_command(import_investments)
cli.add_command(export_investments)

# === Main entry point: open DB, setup, run CLI ===
if __name__ == "__main__":
    database = sqlite3.connect("portfolio.db")
    database.row_factory = investment_row_factory
    cursor = database.cursor()
    cursor.execute(CREATE_INVESTMENTS_SQL)
    cli()
