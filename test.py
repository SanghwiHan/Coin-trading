import pyupbit

def get_va(df, n):
    return df['volume'].rolling(window=n).mean()


df = pyupbit.get_ohlcv()
va5 = get_va(df, 5)
va20 = get_va(df, 20)

if va5.iloc[-2] < va20.iloc[-2] and va5.iloc[-1] > va20.iloc[-1]:
    print('골든 크로스')

if va5.iloc[-2] > va20.iloc[-2] and va5.iloc[-1] < va20.iloc[-1]:
    print('데드 크로스')

