import numpy as np
import pandas as pd

def simulate_bitcoin(days=60, S0=50000, mu=0.001, sigma=0.04, seed=42):
    np.random.seed(seed)
    dt = 1
    prices = [S0]
    for _ in range(1, days):
        Z = np.random.normal(0, 1)
        St = prices[-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
        prices.append(St)
    return prices

def run_simulation():
    # 1. Simulate 60 days of Bitcoin price data
    days = 60
    prices = simulate_bitcoin(days=days, S0=50000, seed=123)

    dates = pd.date_range(start='2023-01-01', periods=days, freq='D')
    df = pd.DataFrame({'Date': dates, 'Price': prices})

    # 2. Calculate 7-day and 30-day Moving Averages
    df['7_SMA'] = df['Price'].rolling(window=7).mean()
    df['30_SMA'] = df['Price'].rolling(window=30).mean()

    # 3. Implement 'Golden Cross' trading algorithm
    initial_balance = 100000.0 # $100k
    balance = initial_balance
    btc_held = 0.0

    print("=== Daily Ledger ===")

    for i in range(1, len(df)):
        date = df.loc[i, 'Date'].strftime('%Y-%m-%d')
        price = df.loc[i, 'Price']
        sma7 = df.loc[i, '7_SMA']
        sma30 = df.loc[i, '30_SMA']

        prev_sma7 = df.loc[i-1, '7_SMA']
        prev_sma30 = df.loc[i-1, '30_SMA']

        # Check if moving averages are available
        if pd.isna(sma30) or pd.isna(prev_sma30):
            continue

        # Golden Cross (Buy): 7-day crosses above 30-day
        if prev_sma7 <= prev_sma30 and sma7 > sma30:
            if balance > 0:
                btc_bought = balance / price
                print(f"{date}: BUY  {btc_bought:.4f} BTC at ${price:,.2f} | 7-SMA: ${sma7:,.2f}, 30-SMA: ${sma30:,.2f}")
                btc_held += btc_bought
                balance = 0.0

        # Death Cross (Sell): 7-day crosses below 30-day
        elif prev_sma7 >= prev_sma30 and sma7 < sma30:
            if btc_held > 0:
                amount_received = btc_held * price
                print(f"{date}: SELL {btc_held:.4f} BTC at ${price:,.2f} | 7-SMA: ${sma7:,.2f}, 30-SMA: ${sma30:,.2f}")
                balance += amount_received
                btc_held = 0.0

    # 4. Final portfolio performance
    final_price = df.iloc[-1]['Price']
    final_portfolio_value = balance + (btc_held * final_price)

    print("\n=== Final Portfolio Performance ===")
    print(f"Initial Balance: ${initial_balance:,.2f}")
    print(f"Final Balance:   ${final_portfolio_value:,.2f}")

    roi = ((final_portfolio_value - initial_balance) / initial_balance) * 100
    print(f"Return on Investment (ROI): {roi:.2f}%")
    print(f"Final BTC Held: {btc_held:.4f}")
    print(f"Final Cash Balance: ${balance:,.2f}")

if __name__ == "__main__":
    run_simulation()
