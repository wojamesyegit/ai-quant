"""云南白药综合分析生成脚本 - 技术分析 + 基本面 + 宏观 + HTML页面"""
import json, math

# ========== 加载数据 ==========
with open(r"Y:\Work Buddy\Quant\daily_data_5y.json", "r", encoding="utf-8") as f:
    daily_data = json.load(f)

# 按日期升序
daily_data.sort(key=lambda x: x["trade_date"])

closes = [d["close"] for d in daily_data]
highs = [d["high"] for d in daily_data]
lows = [d["low"] for d in daily_data]
opens = [d["open"] for d in daily_data]
vols = [d["vol"] for d in daily_data]
amounts = [d["amount"] for d in daily_data]
pct_chgs = [d["pct_chg"] for d in daily_data]
dates = [d["trade_date"] for d in daily_data]

n = len(closes)
print(f"数据量: {n} 个交易日, {dates[0]} ~ {dates[-1]}")

# ========== 宏观数据 ==========
macro = {
    "cpi": [{"month":"202101","cpi_yoy":-0.3},{"month":"202102","cpi_yoy":-0.2},{"month":"202103","cpi_yoy":0.4},{"month":"202104","cpi_yoy":0.9},{"month":"202105","cpi_yoy":1.3},{"month":"202106","cpi_yoy":1.1},{"month":"202107","cpi_yoy":1.0},{"month":"202108","cpi_yoy":0.8},{"month":"202109","cpi_yoy":0.7},{"month":"202110","cpi_yoy":1.5},{"month":"202111","cpi_yoy":2.3},{"month":"202112","cpi_yoy":1.5},{"month":"202201","cpi_yoy":0.9},{"month":"202202","cpi_yoy":0.9},{"month":"202203","cpi_yoy":1.5},{"month":"202204","cpi_yoy":2.1},{"month":"202205","cpi_yoy":2.1},{"month":"202206","cpi_yoy":2.5},{"month":"202207","cpi_yoy":2.7},{"month":"202208","cpi_yoy":2.5},{"month":"202209","cpi_yoy":2.8},{"month":"202210","cpi_yoy":2.1},{"month":"202211","cpi_yoy":1.6},{"month":"202212","cpi_yoy":1.8},{"month":"202301","cpi_yoy":2.1},{"month":"202302","cpi_yoy":1.0},{"month":"202303","cpi_yoy":0.7},{"month":"202304","cpi_yoy":0.1},{"month":"202305","cpi_yoy":0.2},{"month":"202306","cpi_yoy":0.0},{"month":"202307","cpi_yoy":-0.3},{"month":"202308","cpi_yoy":0.1},{"month":"202309","cpi_yoy":0.0},{"month":"202310","cpi_yoy":-0.2},{"month":"202311","cpi_yoy":-0.5},{"month":"202312","cpi_yoy":-0.3},{"month":"202401","cpi_yoy":-0.8},{"month":"202402","cpi_yoy":0.7},{"month":"202403","cpi_yoy":0.1},{"month":"202404","cpi_yoy":0.3},{"month":"202405","cpi_yoy":0.3},{"month":"202406","cpi_yoy":0.2},{"month":"202407","cpi_yoy":0.5},{"month":"202408","cpi_yoy":0.6},{"month":"202409","cpi_yoy":0.4},{"month":"202410","cpi_yoy":0.3},{"month":"202411","cpi_yoy":0.2},{"month":"202412","cpi_yoy":0.1},{"month":"202501","cpi_yoy":0.5},{"month":"202502","cpi_yoy":-0.7},{"month":"202503","cpi_yoy":-0.1},{"month":"202504","cpi_yoy":-0.1},{"month":"202505","cpi_yoy":-0.1},{"month":"202506","cpi_yoy":0.1},{"month":"202507","cpi_yoy":0.0},{"month":"202508","cpi_yoy":-0.4},{"month":"202509","cpi_yoy":-0.3},{"month":"202510","cpi_yoy":0.2},{"month":"202511","cpi_yoy":0.7},{"month":"202512","cpi_yoy":0.8},{"month":"202601","cpi_yoy":0.2},{"month":"202602","cpi_yoy":1.3},{"month":"202603","cpi_yoy":1.0},{"month":"202604","cpi_yoy":1.2},{"month":"202605","cpi_yoy":1.2}],
    "gdp": [{"quarter":"2021Q1","gdp_yoy":18.9},{"quarter":"2021Q2","gdp_yoy":13.0},{"quarter":"2021Q3","gdp_yoy":10.2},{"quarter":"2021Q4","gdp_yoy":8.6},{"quarter":"2022Q1","gdp_yoy":4.8},{"quarter":"2022Q2","gdp_yoy":2.7},{"quarter":"2022Q3","gdp_yoy":3.2},{"quarter":"2022Q4","gdp_yoy":3.1},{"quarter":"2023Q1","gdp_yoy":4.7},{"quarter":"2023Q2","gdp_yoy":5.7},{"quarter":"2023Q3","gdp_yoy":5.4},{"quarter":"2023Q4","gdp_yoy":5.4},{"quarter":"2024Q1","gdp_yoy":5.3},{"quarter":"2024Q2","gdp_yoy":5.0},{"quarter":"2024Q3","gdp_yoy":4.8},{"quarter":"2024Q4","gdp_yoy":5.0},{"quarter":"2025Q1","gdp_yoy":5.4},{"quarter":"2025Q2","gdp_yoy":5.3},{"quarter":"2025Q3","gdp_yoy":5.2},{"quarter":"2025Q4","gdp_yoy":5.0}]
}

# ========== 技术指标计算 ==========
# SMA
def sma(data, period):
    result = [None] * len(data)
    for i in range(period-1, len(data)):
        result[i] = round(sum(data[i-period+1:i+1]) / period, 2)
    return result

# EMA
def ema(data, period):
    result = [None] * len(data)
    k = 2.0 / (period + 1)
    result[period-1] = sum(data[:period]) / period
    for i in range(period, len(data)):
        result[i] = round(data[i] * k + result[i-1] * (1-k), 4)
    return result

# MACD
ema12 = ema(closes, 12)
ema26 = ema(closes, 26)
dif = [round(ema12[i] - ema26[i], 4) if (ema12[i] and ema26[i]) else None for i in range(n)]
dea = ema([d if d else 0 for d in dif], 9)
bar = [round(2*(dif[i]-dea[i]), 4) if (dif[i] and dea[i]) else None for i in range(n)]

# RSI
def rsi(data, period):
    gains, losses = [], []
    for i in range(1, len(data)):
        d = data[i] - data[i-1]
        gains.append(max(d, 0))
        losses.append(max(-d, 0))
    result = [None] * len(data)
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(data)):
        if avg_loss == 0:
            result[i] = 100.0
        else:
            result[i] = round(100 - 100/(1 + avg_gain/avg_loss), 2)
        avg_gain = (avg_gain*(period-1) + gains[i-1]) / period
        avg_loss = (avg_loss*(period-1) + losses[i-1]) / period
    return result

rsi6 = rsi(closes, 6)
rsi14 = rsi(closes, 14)
rsi24 = rsi(closes, 24)

# KDJ
high_n = [max(highs[max(0,i-8):i+1]) for i in range(n)]
low_n = [min(lows[max(0,i-8):i+1]) for i in range(n)]
rsv, k_val, d_val, j_val = [None]*n, [None]*n, [None]*n, [None]*n
for i in range(8, n):
    rng = high_n[i] - low_n[i]
    rsv[i] = round((closes[i]-low_n[i])/rng*100 if rng>0 else 50, 2)
    if i == 8:
        k_val[i] = round(2/3*50 + 1/3*rsv[i], 2)
        d_val[i] = round(2/3*50 + 1/3*k_val[i], 2)
    else:
        k_val[i] = round(2/3*k_val[i-1] + 1/3*rsv[i], 2)
        d_val[i] = round(2/3*d_val[i-1] + 1/3*k_val[i], 2)
    j_val[i] = round(3*k_val[i] - 2*d_val[i], 2)

# Bollinger Bands
sma20 = sma(closes, 20)
bb_upper, bb_mid, bb_lower = [None]*n, [None]*n, [None]*n
for i in range(19, n):
    subset = closes[i-19:i+1]
    mean = sum(subset)/20
    std = math.sqrt(sum((x-mean)**2 for x in subset)/20)
    bb_mid[i] = round(mean, 2)
    bb_upper[i] = round(mean + 2*std, 2)
    bb_lower[i] = round(mean - 2*std, 2)

# OBV
obv = [0] * n
for i in range(1, n):
    if closes[i] > closes[i-1]:
        obv[i] = obv[i-1] + vols[i]
    elif closes[i] < closes[i-1]:
        obv[i] = obv[i-1] - vols[i]
    else:
        obv[i] = obv[i-1]

# ========== 关键支撑阻力位 ==========
recent_idx = min(250, n)
recent_high = max(highs[-recent_idx:])
recent_low = min(lows[-recent_idx:])
all_high = max(highs)
all_low = min(lows)
current_price = closes[-1]

# 计算成交量加权均价
vwap_recent = sum(a*b for a,b in zip(closes[-recent_idx:], vols[-recent_idx:])) / sum(vols[-recent_idx:])

# ========== 阶段涨跌统计 ==========
def calc_return(data, start_idx, end_idx):
    if start_idx < 0: return None
    return round((data[end_idx] - data[start_idx]) / data[start_idx] * 100, 2)

periods = {
    "y2021": [0, min(242, n-1)],
    "y2022": [242, min(484, n-1)],
    "y2023": [484, min(726, n-1)],
    "y2024": [726, min(968, n-1)],
    "y2025": [968, min(1210, n-1)],
    "ytd": [-len([d for d in dates if d>="20260101"]), -1],
    "y3m": [max(0, n-63), -1],
    "y1m": [max(0, n-22), -1],
}

ret_stats = {}
for k, (s, e) in periods.items():
    if s < n:
        ret_stats[k] = calc_return(closes, s, e)

# ========== 基本面分析 (基于行情推导) ==========
# daily_basic 数据用于估值分析
# 由于没有财务接口权限,基于价格和成交量推导基本面趋势

# 计算年平均价和年交易量
yearly_avg = {}
yearly_vol = {}
for d in daily_data:
    y = d["trade_date"][:4]
    if y not in yearly_avg:
        yearly_avg[y] = {"prices": [], "vols": []}
    yearly_avg[y]["prices"].append(d["close"])
    yearly_avg[y]["vols"].append(d["vol"])

for y in yearly_avg:
    yearly_avg[y]["avg_close"] = round(sum(yearly_avg[y]["prices"])/len(yearly_avg[y]["prices"]), 2)
    yearly_avg[y]["total_vol"] = round(sum(yearly_avg[y]["vols"])/10000, 2)

# ========== 波动率分析 ==========
volatility = []
for i in range(20, n):
    subset = pct_chgs[i-19:i+1]
    mean = sum(subset)/20
    vol = math.sqrt(sum((x-mean)**2 for x in subset)/20) * math.sqrt(252)
    volatility.append(round(vol, 2))

# ========== 生成HTML数据JSON ==========
tech_data = {
    "dates": dates,
    "closes": closes,
    "opens": opens,
    "highs": highs,
    "lows": lows,
    "vols": vols,
    "pct_chgs": pct_chgs,
    "ma5": sma(closes, 5),
    "ma10": sma(closes, 10),
    "ma20": sma20,
    "ma60": sma(closes, 60),
    "ma120": sma(closes, 120),
    "ma250": sma(closes, 250),
    "dif": dif,
    "dea": dea,
    "bar": bar,
    "rsi6": rsi6,
    "rsi14": rsi14,
    "rsi24": rsi24,
    "k": k_val,
    "d": d_val,
    "j": j_val,
    "bb_upper": bb_upper,
    "bb_mid": bb_mid,
    "bb_lower": bb_lower,
    "obv": obv,
    "volatility": [None]*20 + volatility,
}

summary = {
    "ts_code": "000538.SZ",
    "name": "云南白药",
    "current_price": current_price,
    "date_range": f"{dates[0]} ~ {dates[-1]}",
    "total_days": n,
    "all_time_high": all_high,
    "all_time_low": all_low,
    "recent_high": recent_high,
    "recent_low": recent_low,
    "vwap_recent": round(vwap_recent, 2),
    "returns": ret_stats,
    "yearly_avg": yearly_avg,
}

# 保存技术指标数据
with open(r"Y:\Work Buddy\Quant\tech_indicators.json", "w", encoding="utf-8") as f:
    json.dump(tech_data, f, ensure_ascii=False)
print("技术指标已保存: tech_indicators.json")

# 保存摘要数据
with open(r"Y:\Work Buddy\Quant\analysis_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False)
print("分析摘要已保存: analysis_summary.json")

# 保存宏观数据
with open(r"Y:\Work Buddy\Quant\macro_data.json", "w", encoding="utf-8") as f:
    json.dump(macro, f, ensure_ascii=False)
print("宏观数据已保存: macro_data.json")

print(f"\n=== 摘要 ===")
print(f"当前价格: {current_price}")
print(f"5年最高: {all_high}, 最低: {all_low}")
for k, v in ret_stats.items():
    sign = "+" if v and v >= 0 else ""
    print(f"  {k}: {sign}{v}%")
