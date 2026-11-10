import csv
import os
from datetime import datetime

# Sample current prices (S&P 500 Dataset jaisa)
CURRENT_PRICES = {
    "AAPL": 232.50, "【entity-MSFT¦canonical_name=MSFT】": 428.15, "GOOGL": 172.30, "【entity-AMZN¦canonical_name=AMZN】": 201.20,
    "【entity-META¦canonical_name=META】": 585.40, "NVDA": 131.80, "TSLA": 248.90, "NFLX": 762.10,
    "【entity-RELIANCE¦canonical_name=RELIANCE】": 2450.75, "TCS": 4150.20, "INFY": 1850.60, "HDFCBANK": 1640.35,
    "SBIN": 810.45, "ITC": 485.20,
}

def load_prices_from_csv(filename="sp500_tickers.csv"):
    prices = {}
    if os.path.exists(filename):
        try:
            with open(filename, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ticker = (row.get("Ticker") or row.get("ticker") or row.get("Symbol") or "").strip().upper()
                    price = row.get("Current_Price") or row.get("Price") or row.get("price") or row.get("Close")
                    if ticker and price:
                        try:
                            prices[ticker] = float(price)
                        except ValueError:
                            pass
        except Exception:
            pass
    return prices

def get_current_price(ticker, price_map):
    if ticker in price_map:
        return price_map[ticker], "CSV/Sample"
    try:
        import yfinance as yf
        data = yf.Ticker(ticker).history(period="1d")
        if not data.empty:
            return float(data["Close"].iloc[-1]), "Live (yfinance)"
    except Exception:
        pass
    while True:
        try:
            p = float(input(f"Current price for {ticker} not found. Enter current price: Rs/$ "))
            return p, "Manual"
        except ValueError:
            print("Please enter a valid number.")

def main():
    print("=" * 60)
    print("  STOCK PORTFOLIO PERFORMANCE TRACKER")
    print("=" * 60)

    price_map = {**CURRENT_PRICES, **load_prices_from_csv()}

    # Portfolio positions in dictionary structure
    portfolio = {}

    print("\nEnter your holdings (type 'done' to finish)\n")
    while True:
        ticker = input("Enter stock ticker symbol (e.g. AAPL) or 'done': ").strip().upper()
        if ticker == "DONE":
            break
        if not ticker:
            continue
        try:
            buy_price = float(input(f"  Buy price for {ticker}: "))
            quantity = float(input(f"  Share quantity for {ticker}: "))
        except ValueError:
            print("  Invalid input. Please enter numbers only.")
            continue
        if buy_price <= 0 or quantity <= 0:
            print("  Buy price and quantity must be > 0.")
            continue

        if ticker in portfolio:
            old = portfolio[ticker]
            total_qty = old["quantity"] + quantity
            avg_buy = (old["buy_price"] * old["quantity"] + buy_price * quantity) / total_qty
            portfolio[ticker] = {"buy_price": avg_buy, "quantity": total_qty}
        else:
            portfolio[ticker] = {"buy_price": buy_price, "quantity": quantity}
        print(f"  Added {ticker} - {quantity} shares @ {buy_price}\n")

    if not portfolio:
        print("No holdings entered. Exiting.")
        return

    rows = []
    total_invested = 0
    total_current = 0

    print("\n" + "=" * 90)
    print(f"{'Ticker':<10} {'Qty':<8} {'Buy Price':<12} {'Curr Price':<12} {'Invested':<12} {'Current':<12} {'Gain/Loss %':<12}")
    print("=" * 90)

    for ticker, data in portfolio.items():
        buy_price = data["buy_price"]
        qty = data["quantity"]
        current_price, source = get_current_price(ticker, price_map)

        invested = buy_price * qty
        current_value = current_price * qty
        gain_loss = current_value - invested
        gain_loss_pct = (gain_loss / invested * 100) if invested != 0 else 0

        total_invested += invested
        total_current += current_value

        print(f"{ticker:<10} {qty:<8} {buy_price:<12.2f} {current_price:<12.2f} {invested:<12.2f} {current_value:<12.2f} {gain_loss_pct:+.2f}%")

        rows.append({
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Ticker": ticker,
            "Quantity": qty,
            "Buy_Price": round(buy_price, 2),
            "Current_Price": round(current_price, 2),
            "Invested_Value": round(invested, 2),
            "Current_Value": round(current_value, 2),
            "Gain_Loss": round(gain_loss, 2),
            "Gain_Loss_Percent": round(gain_loss_pct, 2),
            "Price_Source": source
        })

    total_gain = total_current - total_invested
    total_gain_pct = (total_gain / total_invested * 100) if total_invested else 0

    print("=" * 90)
    print(f"Total Invested Capital : {total_invested:.2f}")
    print(f"Total Current Value   : {total_current:.2f}")
    print(f"Total Gain/Loss       : {total_gain:+.2f} ({total_gain_pct:+.2f}%)")
    print("=" * 90)

    # Write results into portfolio_summary.csv using csv module
    output_file = "portfolio_summary.csv"
    file_exists = os.path.exists(output_file)
    fieldnames = ["Date", "Ticker", "Quantity", "Buy_Price", "Current_Price",
                  "Invested_Value", "Current_Value", "Gain_Loss", "Gain_Loss_Percent", "Price_Source"]

    with open(output_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)
        writer.writerow({
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Ticker": "TOTAL",
            "Quantity": "",
            "Buy_Price": "",
            "Current_Price": "",
            "Invested_Value": round(total_invested, 2),
            "Current_Value": round(total_current, 2),
            "Gain_Loss": round(total_gain, 2),
            "Gain_Loss_Percent": round(total_gain_pct, 2),
            "Price_Source": "Summary"
        })

    print(f"\nSaved! Transaction summary logged to '{output_file}'")

if __name__ == "__main__":
    main()