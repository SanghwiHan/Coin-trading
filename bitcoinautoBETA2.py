import time
import pyupbit
import datetime

access = "WA2kUxxSfcS1LupMU64wrK4rjbCbvbUbP7wMGJwY"
secret = "pWohyZzG2IxTcmz8bovHLguxgFcbdaqvIRkw0u3w"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회(120분)"""
    df = pyupbit.get_ohlcv(ticker, interval="minute", count=120)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price


def get_target_price240(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회(240분)"""
    df = pyupbit.get_ohlcv(ticker, interval="minute", count=240)
    target_price240 = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price240


    

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

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

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-STX")
        end_time = start_time + datetime.timedelta(days=1)
        

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-STX", 0.2)
            current_price = get_current_price("KRW-STX")
            benefit_price = target_price * 1.15 # 익절조건은 타겟의 1.2배
            target_price240 = get_target_price240("KRW-STX", 0.2)
            pcrun_price = target_price * 0.9 #빤쓰런 조건
            
            if(target_price > target_price240):
            
            
                if target_price < current_price and current_price < benefit_price: # 타겟금액 이상이되고 익절조건 미만일때 매수만
                    krw = get_balance("KRW") # 이하 동일
                    if krw > 5000:
                     upbit.buy_market_order("KRW-STX", krw*0.9995)
                elif target_price < current_price and benefit_price < current_price: # 타겟금액 이상, 익절조건 이상일때
                    stx = get_balance("STX") # SAND의 잔고 조회(else: 이하와 동일)
                    if stx > 0.00008: # sand 잔량이 0.00008개 이상 되고
                     upbit.sell_market_order("KRW-STX", stx*0.9995) # 조건 부합시 매도코드입력. 수수료비용만큼은 제외하고 거래됨)
            elif(target_price < target_price240 and pcrun_price > current_price ):#손절라인
                 stx = get_balance("STX") # SAND의 잔고 조회(else: 이하와 동일)
                 if stx > 0.00008: # sand 잔량이 0.00008개 이상 되고
                    upbit.sell_market_order("KRW-STX", stx*0.9995) # 조건 부합시 매도코드입력. 수수료비용만큼은 제외하고 거래됨)
                    print ("goodmorning")
            time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)