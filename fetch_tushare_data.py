import tushare as ts
import datetime
import json

# 使用用户提供的token
token = '9446dfa6d3538bf5b45984d3d745cca9d04b47ee474918664a71dd94'
ts.set_token(token)
pro = ts.pro_api()

# 获取云南白药(000538.SZ)近一年日线数据
# 计算日期范围
end_date = datetime.datetime.now().strftime('%Y%m%d')
start_date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y%m%d')

print(f"获取云南白药(000538)行情数据: {start_date} 至 {end_date}")

df = pro.daily(ts_code='000538.SZ', start_date=start_date, end_date=end_date)

# 按日期升序排列
df = df.sort_values('trade_date', ascending=True)

# 保存为CSV
csv_path = r'Y:\Work Buddy\Quant\yunnan_baiyao_daily.csv'
df.to_csv(csv_path, index=False, encoding='utf-8-sig')
print(f"CSV数据已保存至: {csv_path}")

# 同时输出JSON供HTML页面使用
df['trade_date'] = df['trade_date'].astype(str)
data_records = df.to_dict(orient='records')
json_path = r'Y:\Work Buddy\Quant\yunnan_baiyao_daily.json'
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data_records, f, ensure_ascii=False, indent=2)
print(f"JSON数据已保存至: {json_path}")

# 输出摘要信息
print(f"\n数据摘要:")
print(f"总交易日数: {len(df)}")
print(f"日期范围: {df['trade_date'].min()} ~ {df['trade_date'].max()}")
print(f"最高价: {df['high'].max():.2f}")
print(f"最低价: {df['low'].min():.2f}")
print(f"最新收盘价: {df['close'].iloc[-1]:.2f}")

# 计算涨跌幅度
total_change = (df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0] * 100
print(f"近一年涨跌幅: {total_change:.2f}%")
