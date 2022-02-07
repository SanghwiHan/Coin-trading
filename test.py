import pyupbit


access = "WA2kUxxSfcS1LupMU64wrK4rjbCbvbUbP7wMGJwY"
secret = "pWohyZzG2IxTcmz8bovHLguxgFcbdaqvIRkw0u3w"



upbit = pyupbit.Upbit(access, secret)

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0




def avg_ticker_price(ticker):
        balances = upbit.get_balances()
        for balance in balances:
            if ticker.split('-')[1] == balance['currency']:
                return float(balance['avg_buy_price'])
        
        return 0.0

#print(pyupbit.get_ohlcv("KRW-BTC", interval="minute1")) 

#print(pyupbit.get_ohlcv("KRW-BTC", interval="minute" , count=1))


def get_high_price(ticker): #전 분봉 high값 조회
    df = pyupbit.get_ohlcv(ticker, interval="minute1")
    high_price = df.iloc[-2]['high']
    return high_price

balance = get_balance("KRW")
avg_ticker_price = avg_ticker_price("KRW-NEAR")
high_price = get_high_price("KRW-NEAR")

print(high_price)
print(balance)
print(avg_ticker_price)
