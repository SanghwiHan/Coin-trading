import time
import pyupbit
import datetime

access = "WA2kUxxSfcS1LupMU64wrK4rjbCbvbUbP7wMGJwY"
secret = "pWohyZzG2IxTcmz8bovHLguxgFcbdaqvIRkw0u3w"

coin_code = "MANA" # 종목코드


# 20분 이평선삭제버전

def get_ma5(ticker): # 분봉 22분 조회, 5분 이평선
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=22)
    ma5 = df['close'].rolling(5).mean().iloc[-2] # 전 분봉으로 조회(-2)
    return ma5

def get_ma10(ticker): # 분봉 22, 조회 10분 이평선
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=22)
    ma10 = df['close'].rolling(10).mean().iloc[-2] # 전 분봉으로 조회(-2)
    return ma10


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_current_price(ticker=ticker)

#def get_current_price2(ticker):
    """현재가 조회"""
  #  return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
    
def get_high_price(ticker): #전 분봉 high값 조회
    df = pyupbit.get_ohlcv(ticker, interval="minute1")
    high_price = df.iloc[-2]['high']
    return high_price

    


# def get_ma20(ticker): # 분봉 22, 조회 20분 이평선
#     df = pyupbit.get_ohlcv(ticker, interval="minute1", count=22)
#     ma20 = df['close'].rolling(20).mean().iloc[-2] #전 분봉으로 조회(-2)
#     return ma20

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



# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        ma5 = get_ma5("KRW-"+coin_code) # ma5 값 차트 불러오는 함수
        ma10 = get_ma10("KRW-"+coin_code) # ma10 값 차트 불러오는 함수
        # ma20 = get_ma20("KRW-"+coin_code) # ma20 값 차트 불러오는 함수
        #current_price2 = get_current_price2("KRW-"+coin_code) # 현재값 오더북에서 불러오는 함수
        current_price = get_current_price("KRW-"+coin_code)
        
        high_price = get_high_price("KRW-"+coin_code)

        run_price = avg_ticker_price*0.95


        if ma10 < ma5 and current_price >= high_price: 
            krw = get_balance("KRW")
            if krw > 5000:
                upbit.buy_market_order("KRW-"+coin_code, krw*0.9995)
                avg_ticker_price = avg_ticker_price("KRW-"+coin_code) ##수정한부분 (사진 뒤 평균가 읽어오도록)
                time.sleep(60)
                print("매수")

        if avg_ticker_price*1.015 < current_price:
            coin_volume = get_balance(coin_code)
            if coin_volume > 0.00008:
                upbit.sell_market_order("KRW-"+coin_code, coin_volume*0.9995)
                time.sleep(60)
                print("익절")

        elif ma10 > ma5 and run_price > current_price:
            coin_volume = get_balance(coin_code)
            if coin_volume > 0.00008:
                upbit.sell_market_order("KRW-"+coin_code, coin_volume*0.9995)
                time.sleep(60)
                print("손절")
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)