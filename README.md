# 💰 Cryptocurrency Portfolio Manager

This project is a **command-line tool** to manage cryptocurrency investments using **Python** and **SQLite**.

## 🧠 Built With

- `sqlite3` module from Python's standard library
- `click` for command-line interface
- `requests` to fetch live crypto prices from CoinGecko
- `csv` for import/export functionality
- `dataclasses` to model investment rows as Python objects

---

## 📋 Key Features

✅ SQLite is a file-based database  
✅ Parameterized SQL queries (protect against SQL injection)  
✅ Row factories transform query results into Python dataclasses  
✅ Automatically calculates live value of portfolio  
✅ Import/export CSV support  
✅ Clean and modular CLI

---

## 🛠️ Commands

```bash
# Show price
python main_2.py show-coin-price --coin_id=bitcoin --currency=usd

# Add investment
python main_2.py add-investment --coin_id=bitcoin --currency=usd --amount=1.0
python main_2.py add-investment --coin_id=bitcoin --currency=usd --amount=0.5 --sell

# Calculate total portfolio value
python main_2.py get-investment-value --coin_id=bitcoin --currency=usd

# Import from CSV
python main_2.py import-investments --csv_file=investments.csv

# Export to CSV
python main_2.py export-investments --csv_file=my_export.csv

