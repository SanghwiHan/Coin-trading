import time
import pyupbit
import datetime

access = "WA2kUxxSfcS1LupMU64wrK4rjbCbvbUbP7wMGJwY"
secret = "pWohyZzG2IxTcmz8bovHLguxgFcbdaqvIRkw0u3w"

coin_code = "BORA" # 종목코드


def get_ma5(ticker): # 분봉 22분 조회, 5분 이평선
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=22)
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma5

def get_ma10(ticker): # 분봉 22, 조회 10분 이평선
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=22)
    ma10 = df['close'].rolling(10).mean().iloc[-1]
    return ma10

def get_ma20(ticker): # 분봉 22, 조회 20분 이평선
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=22)
    ma20 = df['close'].rolling(20).mean().iloc[-1]
    return ma20


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


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

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        ma5 = get_ma5("KRW-"+coin_code) # ma5 값 차트 불러오는 함수
        ma10 = get_ma10("KRW-"+coin_code) # ma10 값 차트 불러오는 함수
        ma20 = get_ma20("KRW-"+coin_code) # ma20 값 차트 불러오는 함수
        if ma10 < ma5 and ma20 * 1.01 < ma5: # 5분이평선이 10분이평선보다 크고 / 5분 이평선이 20분이평선의 2%이상일 경우(상승추세고려)
            krw = get_balance("KRW")
            current_price = get_current_price("KRW-"+coin_code)
            run_price = current_price*0.95
            
            if krw > 5000:
                upbit.buy_market_order("KRW-"+coin_code, krw*0.9995)

        elif ma10 > ma5 and current_price < run_price: #손절라인
            
            coin_volume = get_balance(coin_code)
            if coin_volume > 0.00008:
                upbit.sell_market_order("KRW-"+coin_code, coin_volume*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)