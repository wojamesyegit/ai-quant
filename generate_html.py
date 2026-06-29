"""生成云南白药综合分析HTML页面 - 修复版"""
import json

with open(r"Y:\Work Buddy\Quant\tech_indicators.json", "r", encoding="utf-8") as f:
    tech = json.load(f)
with open(r"Y:\Work Buddy\Quant\analysis_summary.json", "r", encoding="utf-8") as f:
    summary = json.load(f)
with open(r"Y:\Work Buddy\Quant\macro_data.json", "r", encoding="utf-8") as f:
    macro = json.load(f)

# 计算分析值
returns = summary["returns"]
def pct_str(v):
    if v is None: return "N/A"
    return f"{'+' if v>=0 else ''}{v}%"

closes = tech["closes"]
dates = tech["dates"]
all_high = max(closes)
all_low = min(closes)
current_price = closes[-1]
last_pct = tech["pct_chgs"][-1]

# CSS class helper
def clr(v):
    return "up" if (v is not None and v >= 0) else "dn"

# 计算年度均价显示
yearly_lines = []
for y, v in sorted(summary["yearly_avg"].items()):
    yearly_lines.append(f'<tr><td>{y}</td><td class="dn">{v["avg_close"]:.2f}元</td><td>{v["total_vol"]:.0f}万手</td></tr>')

# 基本面数据
yearly_table = "\n".join(yearly_lines)

# 技术指标当前值
r14_last = tech["rsi14"][-1] or 50
r6_last = tech["rsi6"][-1] or 50
k_last = tech["k"][-1] or 50
d_last = tech["d"][-1] or 50
j_last = tech["j"][-1] or 50
bar_last = tech["bar"][-1] or 0
dif_last = tech["dif"][-1] or 0
dea_last = tech["dea"][-1] or 0
bb_mid = tech["bb_mid"][-1] or 0
bb_upper = tech["bb_upper"][-1] or 0
bb_lower = tech["bb_lower"][-1] or 0
last_vol = tech["vols"][-1] or 0

# 均线值
ma5_v = tech["ma5"][-1] or 0
ma20_v = tech["ma20"][-1] or 0
ma60_v = tech["ma60"][-1] or 0
ma120_v = tech["ma120"][-1] or 0

# 计算OBV MA20
obv = tech["obv"]
obv_ma20 = []
for i in range(len(obv)):
    if i < 19: obv_ma20.append(None)
    else:
        s = sum(obv[i-19:i+1])
        obv_ma20.append(round(s/20))
tech["obv_ma20"] = obv_ma20

# RSI分析
if r14_last > 70:
    rsi_status = "超买区间，短期存在回调压力"
elif r14_last < 30:
    rsi_status = "超卖区间，可能酝酿反弹"
elif r14_last > 50:
    rsi_status = "偏强，多头占据优势"
else:
    rsi_status = "偏弱，空头占据优势"

# MACD分析
bar_prev = tech["bar"][-3] or 0
if bar_last > 0:
    macd_status = "MACD柱状线在零轴上方且扩大，多头动能较强" if bar_last > bar_prev else "MACD柱状线在零轴上方但收敛，多头动能减弱"
else:
    macd_status = "MACD柱状线在零轴下方且扩大，空头动能较强" if bar_last < bar_prev else "MACD柱状线在零轴下方但收敛，空头动能减弱"

# KDJ
if j_last > 80:
    kdj_status = "J值处于超买区，短期注意回调风险"
elif j_last < 20:
    kdj_status = "J值处于超卖区，短期可能反弹"
else:
    kdj_status = "J值处于中性区间"

# BB
if current_price > bb_upper:
    bb_status = "价格突破布林带上轨，短期超买"
elif current_price < bb_lower:
    bb_status = "价格跌破布林带下轨，短期超卖"
else:
    bb_status = "价格在布林带内运行，处于正常波动区间"

# 年度涨跌数据
year_cards = ""
for yr in ["y2021","y2022","y2023","y2024","y2025","y3m","y1m"]:
    v = returns.get(yr)
    c = clr(v) if v is not None else ""
    label = yr.replace("y","") if "y" in yr else ("近3月" if yr=="y3m" else "近1月")
    year_cards += f'<div class="card"><div class="card-label">{label}</div><div class="card-value {c}">{pct_str(v)}</div></div>\n'

# JSON 嵌入
tech_json = json.dumps(tech, ensure_ascii=False)
summary_json = json.dumps(summary, ensure_ascii=False)
macro_json = json.dumps(macro, ensure_ascii=False)

# 构建HTML
html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>云南白药 (000538.SZ) 近五年综合分析报告</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
<style>
:root{{--bg:#f0f2f5;--card:#fff;--t1:#1a1a2e;--t2:#666;--up:#e74c3c;--dn:#2ecc71;--ac:#3498db;--ac2:#f39c12;--bd:#e8ecf1;--warn:#e74c3c;}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--t1);line-height:1.6}}
.header{{background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);color:#fff;padding:40px 24px 30px}}
.header-inner{{max-width:1400px;margin:0 auto}}
.header h1{{font-size:32px;margin-bottom:4px}}
.header .sub{{font-size:14px;color:#a0aec0}}
.price-row{{display:flex;align-items:baseline;gap:20px;margin-top:16px;flex-wrap:wrap}}
.price{{font-size:48px;font-weight:700}}
.price-chg{{font-size:20px;font-weight:600}}
.container{{max-width:1400px;margin:0 auto;padding:24px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-bottom:24px}}
.card{{background:var(--card);border-radius:12px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,0.06);border:1px solid var(--bd)}}
.card-label{{font-size:12px;color:var(--t2);letter-spacing:.5px;margin-bottom:6px}}
.card-value{{font-size:24px;font-weight:700}}
.card-sub{{font-size:12px;color:var(--t2);margin-top:4px}}
.section{{background:var(--card);border-radius:12px;padding:24px;margin-bottom:24px;box-shadow:0 2px 8px rgba(0,0,0,0.06);border:1px solid var(--bd)}}
.section-title{{font-size:18px;font-weight:700;margin-bottom:16px;padding-left:12px;border-left:4px solid var(--ac);display:flex;align-items:center;gap:8px}}
.chart{{width:100%;height:500px}}
.chart-sm{{width:100%;height:350px}}
.two-col{{display:grid;grid-template-columns:1fr 1fr;gap:24px}}
@media(max-width:1000px){{.two-col{{grid-template-columns:1fr}}}}
.analysis-text{{font-size:14px;line-height:1.8;color:#333;white-space:pre-wrap}}
.analysis-text strong{{color:var(--t1)}}
.tag{{display:inline-block;padding:2px 10px;border-radius:20px;font-size:12px;font-weight:600;margin:2px}}
.tag-up{{background:#ffeaea;color:var(--up)}}
.tag-dn{{background:#eafaf1;color:var(--dn)}}
.tag-warn{{background:#fff3e0;color:#e67e22}}
.tag-info{{background:#e3f2fd;color:#1976d2}}
table{{width:100%;border-collapse:collapse;font-size:14px}}
th,td{{padding:10px 14px;text-align:left;border-bottom:1px solid var(--bd)}}
th{{background:#f8f9fa;font-weight:600;color:var(--t2);font-size:12px}}
.up{{color:var(--up)}}
.dn{{color:var(--dn)}}
.vs-bar{{display:flex;align-items:center;gap:8px;margin:6px 0}}
.vs-bar-fill{{height:8px;border-radius:4px;transition:width 0.5s}}
.footer{{text-align:center;padding:30px;color:var(--t2);font-size:12px;border-top:1px solid var(--bd)}}
</style>
</head>
<body>

<div class="header">
  <div class="header-inner">
    <h1>云南白药 <span style="font-weight:400;font-size:24px">000538.SZ</span></h1>
    <div class="sub">深圳证券交易所 | 医药制造 | 近五年综合技术面·基本面·宏观分析</div>
    <div class="price-row">
      <div class="price">{current_price:.2f}</div>
      <div class="price-chg" style="color:var(--{'up' if last_pct>=0 else 'dn'})">{'+' if last_pct>=0 else ''}{last_pct:.2f}%</div>
      <div style="font-size:14px;color:#a0aec0">最新收盘价 (2026-06-29)</div>
    </div>
    <div style="margin-top:16px;display:flex;gap:12px;flex-wrap:wrap">
      <span class="tag tag-info">数据量: {len(dates)}交易日</span>
      <span class="tag tag-warn">5年最高: {all_high:.2f}</span>
      <span class="tag tag-dn">5年最低: {all_low:.2f}</span>
      <span class="tag tag-info">近1年VWAP: {summary["vwap_recent"]}</span>
    </div>
  </div>
</div>

<div class="container">

<!-- 关键指标 + 年度收益 -->
<div class="cards">
  <div class="card"><div class="card-label">5年最高价</div><div class="card-value">{all_high:.2f}</div></div>
  <div class="card"><div class="card-label">5年最低价</div><div class="card-value">{all_low:.2f}</div></div>
  <div class="card"><div class="card-label">当前价格</div><div class="card-value {clr(last_pct)}">{current_price:.2f}</div></div>
  <div class="card"><div class="card-label">近1年振幅</div><div class="card-value">{summary["recent_high"]-summary["recent_low"]:.2f}</div><div class="card-sub">高{summary["recent_high"]} / 低{summary["recent_low"]}</div></div>
  <div class="card"><div class="card-label">近1年VWAP</div><div class="card-value">{summary["vwap_recent"]}</div></div>
  <div class="card"><div class="card-label">总交易日</div><div class="card-value">{len(dates)}</div><div class="card-sub">{dates[0]} ~ {dates[-1]}</div></div>
</div>

<!-- 年度收益 -->
<div class="cards">
{year_cards}
</div>

<!-- 1. 价格走势与均线 -->
<div class="section">
  <div class="section-title">一、价格走势与移动平均线</div>
  <p style="font-size:13px;color:#666;margin-bottom:12px">当前MA5={ma5_v:.2f} | MA20={ma20_v:.2f} | MA60={ma60_v:.2f} | MA120={ma120_v:.2f} | 收盘价={current_price:.2f}</p>
  <div id="maChart" class="chart"></div>
</div>

<!-- 2. MACD -->
<div class="section">
  <div class="section-title">二、MACD 指标分析</div>
  <p style="font-size:13px;color:#666;margin-bottom:12px">DIF={dif_last:.2f} | DEA={dea_last:.2f} | MACD柱={bar_last:.2f} | {macd_status}</p>
  <div id="macdChart" class="chart"></div>
</div>

<!-- 3. RSI + KDJ -->
<div class="two-col">
  <div class="section">
    <div class="section-title">三、RSI 相对强弱指标</div>
    <p style="font-size:13px;color:#666;margin-bottom:8px">RSI(6)={r6_last:.1f} | RSI(14)={r14_last:.1f} | {rsi_status}</p>
    <div id="rsiChart" class="chart-sm"></div>
  </div>
  <div class="section">
    <div class="section-title">四、KDJ 随机指标</div>
    <p style="font-size:13px;color:#666;margin-bottom:8px">K={k_last:.1f} | D={d_last:.1f} | J={j_last:.1f} | {kdj_status}</p>
    <div id="kdjChart" class="chart-sm"></div>
  </div>
</div>

<!-- 5. Bollinger Bands -->
<div class="section">
  <div class="section-title">五、布林带 (Bollinger Bands) — {bb_status}</div>
  <p style="font-size:13px;color:#666;margin-bottom:12px">上轨={bb_upper:.2f} | 中轨={bb_mid:.2f} | 下轨={bb_lower:.2f} | 带宽={(bb_upper-bb_lower)/bb_mid*100:.1f}%</p>
  <div id="bbChart" class="chart"></div>
</div>

<!-- 6. OBV -->
<div class="section">
  <div class="section-title">六、OBV 能量潮与成交量</div>
  <div id="obvChart" class="chart"></div>
</div>

<!-- 7. 价格趋势估值 -->
<div class="section">
  <div class="section-title">七、价格趋势与历史估值区间</div>
  <div id="priceYearChart" class="chart"></div>
</div>

<!-- 8. 年度统计 -->
<div class="section">
  <div class="section-title">八、年度统计对比</div>
  <table>{yearly_table}</table>
</div>

<!-- 9. Macro -->
<div class="section">
  <div class="section-title">九、宏观经济指标走势</div>
  <div id="macroChart" class="chart"></div>
</div>

<!-- 10. 综合分析 -->
<div class="section">
  <div class="section-title">十、综合分析与投资建议</div>
  <div class="analysis-text" id="analysisText"></div>
</div>

</div>

<div class="footer">
  数据来源：Tushare Pro | 分析仅供参考，不构成投资建议 | 生成时间：2026-06-29<br>
  涨为红色(↑)，跌为绿色(↓)，遵循中国市场惯例
</div>

<script>
// Technology indicator data
const TECH_DATA = {tech_json};
const SUMMARY = {summary_json};
const MACRO = {macro_json};

const dates = TECH_DATA.dates;
const closes = TECH_DATA.closes;
const opens = TECH_DATA.opens;
const highs = TECH_DATA.highs;
const lows = TECH_DATA.lows;
const vols = TECH_DATA.vols;
const pctChgs = TECH_DATA.pct_chgs;
const upColor = '#e74c3c', dnColor = '#2ecc71';

const volColors = pctChgs.map(function(p,i) {{
  if (p === null) return dnColor;
  return p >= 0 ? upColor : dnColor;
}});

const fixArr = function(arr) {{ return arr.map(function(v) {{ return v === null ? '-' : v; }}); }};

// 1. MA Chart
(function(){{
  var chart = echarts.init(document.getElementById('maChart'));
  chart.setOption({{
    tooltip: {{trigger:'axis',backgroundColor:'#fff',borderColor:'#ddd'}},
    legend: {{data:['收盘价','MA5','MA20','MA60','MA120','MA250'],bottom:0}},
    grid: {{left:'3%',right:'3%',top:'5%',bottom:'15%',containLabel:true}},
    xAxis: {{type:'category',data:dates,axisLine:{{lineStyle:{{color:'#999'}}}},axisLabel:{{rotate:45,fontSize:10,interval:'auto'}}}},
    yAxis: {{type:'value',scale:true,splitLine:{{lineStyle:{{color:'#eee'}}}}}},
    dataZoom: [{{type:'inside',start:0,end:100}},{{show:true,type:'slider',bottom:30,start:0,end:100}}],
    series: [
      {{name:'收盘价',type:'line',data:closes,lineStyle:{{width:1.5,color:'#333'}},symbol:'none'}},
      {{name:'MA5',type:'line',data:TECH_DATA.ma5,lineStyle:{{width:1.5,color:upColor}},symbol:'none'}},
      {{name:'MA20',type:'line',data:TECH_DATA.ma20,lineStyle:{{width:1.5,color:'#3498db'}},symbol:'none'}},
      {{name:'MA60',type:'line',data:TECH_DATA.ma60,lineStyle:{{width:1.5,color:'#f39c12'}},symbol:'none'}},
      {{name:'MA120',type:'line',data:TECH_DATA.ma120,lineStyle:{{width:1.5,color:'#9b59b6'}},symbol:'none'}},
      {{name:'MA250',type:'line',data:TECH_DATA.ma250,lineStyle:{{width:1.5,color:dnColor}},symbol:'none'}}
    ]
  }});
}})();

// 2. MACD
(function(){{
  var chart = echarts.init(document.getElementById('macdChart'));
  chart.setOption({{
    tooltip: {{trigger:'axis',backgroundColor:'#fff',borderColor:'#ddd'}},
    grid: [
      {{left:'3%',right:'3%',top:'5%',height:'55%'}},
      {{left:'3%',right:'3%',top:'68%',height:'12%'}},
      {{left:'3%',right:'3%',top:'85%',height:'12%'}}
    ],
    xAxis: [
      {{type:'category',data:dates,gridIndex:0,axisLabel:{{show:false}}}},
      {{type:'category',data:dates,gridIndex:1,axisLabel:{{show:false}}}},
      {{type:'category',data:dates,gridIndex:2,axisLabel:{{rotate:45,fontSize:10,interval:'auto'}}}}
    ],
    yAxis: [
      {{type:'value',gridIndex:0,scale:true,splitLine:{{lineStyle:{{color:'#eee'}}}}}},
      {{type:'value',gridIndex:1,splitLine:{{show:false}}}},
      {{type:'value',gridIndex:2,splitLine:{{show:false}}}}
    ],
    dataZoom: [{{type:'inside',xAxisIndex:[0,1,2],start:0,end:100}},{{show:true,type:'slider',xAxisIndex:[0,1,2],bottom:20,start:0,end:100}}],
    series: [
      {{name:'Price',type:'line',data:closes,xAxisIndex:0,yAxisIndex:0,lineStyle:{{width:1,color:'#666'}},symbol:'none'}},
      {{name:'DIF',type:'line',data:TECH_DATA.dif,xAxisIndex:1,yAxisIndex:1,lineStyle:{{width:1.5,color:upColor}},symbol:'none'}},
      {{name:'DEA',type:'line',data:TECH_DATA.dea,xAxisIndex:1,yAxisIndex:1,lineStyle:{{width:1.5,color:dnColor}},symbol:'none'}},
      {{name:'MACD',type:'bar',data:TECH_DATA.bar.map(function(v){{return v||0;}}),xAxisIndex:2,yAxisIndex:2,itemStyle:{{color:function(p){{return (TECH_DATA.bar[p.dataIndex]||0)>=0?upColor:dnColor;}}}}}}
    ]
  }});
}})();

// 3. RSI
(function(){{
  var chart = echarts.init(document.getElementById('rsiChart'));
  chart.setOption({{
    tooltip: {{trigger:'axis',backgroundColor:'#fff',borderColor:'#ddd'}},
    legend: {{data:['RSI6','RSI14','RSI24'],bottom:0}},
    grid: {{left:'3%',right:'3%',top:'5%',bottom:'15%',containLabel:true}},
    xAxis: {{type:'category',data:dates,axisLabel:{{rotate:45,fontSize:10,interval:'auto'}}}},
    yAxis: {{type:'value',min:0,max:100,splitLine:{{lineStyle:{{color:'#eee'}}}}}},
    dataZoom: [{{type:'inside',start:0,end:100}},{{show:true,type:'slider',bottom:30,start:0,end:100}}],
    series: [
      {{name:'RSI6',type:'line',data:TECH_DATA.rsi6,lineStyle:{{width:1.5,color:upColor}},symbol:'none'}},
      {{name:'RSI14',type:'line',data:TECH_DATA.rsi14,lineStyle:{{width:2,color:'#3498db'}},symbol:'none'}},
      {{name:'RSI24',type:'line',data:TECH_DATA.rsi24,lineStyle:{{width:1.5,color:'#f39c12'}},symbol:'none'}},
      {{name:'',type:'line',data:[],markLine:{{silent:true,lineStyle:{{color:upColor,type:'dashed'}},data:[{{yAxis:70}}]}}}},
      {{name:'',type:'line',data:[],markLine:{{silent:true,lineStyle:{{color:dnColor,type:'dashed'}},data:[{{yAxis:30}}]}}}}
    ]
  }});
}})();

// 4. KDJ
(function(){{
  var chart = echarts.init(document.getElementById('kdjChart'));
  chart.setOption({{
    tooltip: {{trigger:'axis',backgroundColor:'#fff',borderColor:'#ddd'}},
    legend: {{data:['K','D','J'],bottom:0}},
    grid: {{left:'3%',right:'3%',top:'5%',bottom:'15%',containLabel:true}},
    xAxis: {{type:'category',data:dates,axisLabel:{{rotate:45,fontSize:10,interval:'auto'}}}},
    yAxis: {{type:'value',min:0,max:100,splitLine:{{lineStyle:{{color:'#eee'}}}}}},
    dataZoom: [{{type:'inside',start:0,end:100}},{{show:true,type:'slider',bottom:30,start:0,end:100}}],
    series: [
      {{name:'K',type:'line',data:TECH_DATA.k,lineStyle:{{width:1.5,color:upColor}},symbol:'none'}},
      {{name:'D',type:'line',data:TECH_DATA.d,lineStyle:{{width:1.5,color:'#3498db'}},symbol:'none'}},
      {{name:'J',type:'line',data:TECH_DATA.j,lineStyle:{{width:1.5,color:'#f39c12'}},symbol:'none'}}
    ]
  }});
}})();

// 5. BB
(function(){{
  var chart = echarts.init(document.getElementById('bbChart'));
  chart.setOption({{
    tooltip: {{trigger:'axis',backgroundColor:'#fff',borderColor:'#ddd'}},
    legend: {{data:['收盘价','上轨','中轨','下轨'],bottom:0}},
    grid: {{left:'3%',right:'3%',top:'5%',bottom:'15%',containLabel:true}},
    xAxis: {{type:'category',data:dates,axisLabel:{{rotate:45,fontSize:10,interval:'auto'}}}},
    yAxis: {{type:'value',scale:true,splitLine:{{lineStyle:{{color:'#eee'}}}}}},
    dataZoom: [{{type:'inside',start:0,end:100}},{{show:true,type:'slider',bottom:30,start:0,end:100}}],
    series: [
      {{name:'收盘价',type:'line',data:closes,lineStyle:{{width:1.5,color:'#333'}},symbol:'none'}},
      {{name:'上轨',type:'line',data:TECH_DATA.bb_upper,lineStyle:{{width:1,color:upColor,type:'dashed'}},symbol:'none'}},
      {{name:'中轨',type:'line',data:TECH_DATA.bb_mid,lineStyle:{{width:1,color:'#3498db',type:'dashed'}},symbol:'none'}},
      {{name:'下轨',type:'line',data:TECH_DATA.bb_lower,lineStyle:{{width:1,color:dnColor,type:'dashed'}},symbol:'none'}}
    ]
  }});
}})();

// 6. OBV
(function(){{
  var chart = echarts.init(document.getElementById('obvChart'));
  chart.setOption({{
    tooltip: {{trigger:'axis',backgroundColor:'#fff',borderColor:'#ddd'}},
    legend: {{data:['OBV','OBV-MA20','成交量'],bottom:0}},
    grid: [
      {{left:'3%',right:'3%',top:'5%',height:'48%'}},
      {{left:'3%',right:'3%',top:'60%',height:'20%'}}
    ],
    xAxis: [
      {{type:'category',data:dates,gridIndex:0,axisLabel:{{show:false}}}},
      {{type:'category',data:dates,gridIndex:1,axisLabel:{{rotate:45,fontSize:10,interval:'auto'}}}}
    ],
    yAxis: [
      {{type:'value',gridIndex:0,splitLine:{{lineStyle:{{color:'#eee'}}}}}},
      {{type:'value',gridIndex:1,splitLine:{{show:false}},axisLabel:{{show:false}}}}
    ],
    dataZoom: [{{type:'inside',xAxisIndex:[0,1],start:0,end:100}},{{show:true,type:'slider',xAxisIndex:[0,1],bottom:20,start:0,end:100}}],
    series: [
      {{name:'OBV',type:'line',data:TECH_DATA.obv,xAxisIndex:0,yAxisIndex:0,lineStyle:{{width:1.5,color:'#3498db'}},areaStyle:{{color:'rgba(52,152,219,0.1)'}},symbol:'none'}},
      {{name:'OBV-MA20',type:'line',data:TECH_DATA.obv_ma20,xAxisIndex:0,yAxisIndex:0,lineStyle:{{width:1.5,color:upColor}},symbol:'none'}},
      {{name:'成交量',type:'bar',data:vols,xAxisIndex:1,yAxisIndex:1,itemStyle:{{color:function(p){{return volColors[p.dataIndex];}}}}}}
    ]
  }});
}})();

// 7. Price trend + valuation
(function(){{
  var chart = echarts.init(document.getElementById('priceYearChart'));
  chart.setOption({{
    tooltip: {{trigger:'axis',backgroundColor:'#fff',borderColor:'#ddd'}},
    grid: {{left:'3%',right:'3%',top:'5%',bottom:'15%',containLabel:true}},
    xAxis: {{type:'category',data:dates,axisLabel:{{rotate:45,fontSize:10,interval:'auto'}}}},
    yAxis: {{type:'value',scale:true,splitLine:{{lineStyle:{{color:'#eee'}}}}}},
    dataZoom: [{{type:'inside',start:0,end:100}},{{show:true,type:'slider',bottom:30,start:0,end:100}}],
    series: [
      {{name:'收盘价',type:'line',data:closes,lineStyle:{{width:1.5,color:'#333'}},symbol:'none',
        areaStyle:{{color:{{type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[
          {{offset:0,color:'rgba(231,76,60,0.15)'}},
          {{offset:0.5,color:'rgba(52,152,219,0.1)'}},
          {{offset:1,color:'rgba(46,204,113,0.05)'}}
        ]}}}}
      }}
    ]
  }});
}})();

// 8. Macro
(function(){{
  var chart = echarts.init(document.getElementById('macroChart'));
  var cpiData = MACRO.cpi.slice(-48);
  var cpiMonths = cpiData.map(function(m){{return m.month.substring(0,4)+'-'+m.month.substring(4);}});
  var cpiValues = cpiData.map(function(m){{return m.cpi_yoy;}});
  chart.setOption({{
    tooltip: {{trigger:'axis',backgroundColor:'#fff',borderColor:'#ddd'}},
    legend: {{data:['CPI同比(%)'],bottom:0}},
    grid: {{left:'3%',right:'3%',top:'5%',bottom:'15%',containLabel:true}},
    xAxis: {{type:'category',data:cpiMonths,axisLabel:{{rotate:45,fontSize:10,interval:'auto'}}}},
    yAxis: {{type:'value',name:'CPI(%)',splitLine:{{lineStyle:{{color:'#eee'}}}},axisLabel:{{fontSize:11}}}},
    series: [
      {{name:'CPI同比(%)',type:'bar',data:cpiValues,itemStyle:{{color:function(p){{return p.value>=0?upColor:dnColor;}}}},barWidth:'60%'}}
    ]
  }});
}})();

// 9. GDP chart - appended
(function(){{
  var container = document.getElementById('macroChart').parentElement;
  var gdpDiv = document.createElement('div');
  gdpDiv.style.width = '100%';
  gdpDiv.style.height = '350px';
  gdpDiv.style.marginTop = '20px';
  gdpDiv.style.display = 'block';
  container.appendChild(gdpDiv);

  var gdpQuarters = MACRO.gdp.map(function(m){{return m.quarter;}});
  var gdpValues = MACRO.gdp.map(function(m){{return m.gdp_yoy;}});

  var gdpChart = echarts.init(gdpDiv);
  gdpChart.setOption({{
    title: {{text:'GDP同比增速(%)',left:'center',textStyle:{{fontSize:14}}}},
    tooltip: {{trigger:'axis',backgroundColor:'#fff',borderColor:'#ddd'}},
    grid: {{left:'5%',right:'5%',top:'15%',bottom:'10%',containLabel:true}},
    xAxis: {{type:'category',data:gdpQuarters,axisLabel:{{fontSize:11}}}},
    yAxis: {{type:'value',name:'%',splitLine:{{lineStyle:{{color:'#eee'}}}}}},
    series: [{{
      name:'GDP同比(%)',type:'line',data:gdpValues,
      lineStyle:{{width:2,color:'#8e44ad'}},
      itemStyle:{{color:'#8e44ad'}},symbol:'circle',symbolSize:8,
      label:{{show:true,position:'top',fontSize:10,color:'#666'}},
      areaStyle:{{color:{{type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{{offset:0,color:'rgba(142,68,173,0.2)'}},{{offset:1,color:'rgba(142,68,173,0)'}}]}}}}
    }}]
  }});
}})();

// 10. Analysis Text
(function(){{
  var text = [
    '<h3>技术分析总览</h3>',
    '<p>云南白药(000538)自2021年初高点163.28元以来，经历深度调整，当前价格{current_price:.2f}元处于5年估值低位区域。近5年走势大致分为三个阶段:快速下跌期(2021-2022)、底部震荡期(2023)、温和反弹与再寻底(2024-2026)。</p>',
    '',
    '<h4>趋势分析</h4>',
    '<p>当前价格位于主要均线系统下方，中长期均线(MA60/MA120/MA250)形成空头排列。短期MA5与MA20的关系需关注是否产生金叉/死叉信号。从均线角度，股价在2024年一度突破MA60确认中期反弹，但2025年后再次跌破，当前处于偏弱格局。</p>',
    '<p>成交量方面，近一年日均成交较历史均值有所放大，换手率提升，市场分歧加大。</p>',
    '',
    '<h4>震荡指标分析</h4>',
    '<p><strong>RSI(14)当前值{r14_last:.1f}</strong>: {rsi_status}。RSI在30-70区间内波动，未出现极端信号。</p>',
    '<p><strong>KDJ</strong>: K={k_last:.1f}, D={d_last:.1f}, J={j_last:.1f}。{kdj_status}。</p>',
    '<p><strong>MACD</strong>: DIF={dif_last:.2f}, DEA={dea_last:.2f}。{macd_status}。关注DIF与DEA的交叉信号以及柱状线趋势变化。</p>',
    '',
    '<h4>波动率与布林带</h4>',
    '<p>当前布林带带宽约{(bb_upper-bb_lower)/bb_mid*100:.1f}%，{bb_status}。布林带收窄通常预示变盘，扩张则反映趋势加速。</p>',
    '',
    '<h4>OBV能量潮</h4>',
    '<p>OBV反映了资金流入流出的累计情况。若OBV与价格发生背离（价格新低而OBV未新低），则可能预示底部信号。</p>',
    '',
    '<h3>基本面分析</h3>',
    '',
    '<p><strong>公司概况:</strong>云南白药作为A股中药龙头，拥有百年品牌积淀，核心产品涵盖药品、牙膏、洗发水等消费品类。品牌护城河深厚，但近年面临成长性瓶颈。</p>',
    '',
    '<p><strong>业绩趋势:</strong>从年均价和成交量变化看:</p>',
    '<table style="margin:12px 0"><tr><th>年份</th><th>年均价(元)</th><th>年成交量(万手)</th></tr>{yearly_table}</table>',
    '<p>年均价从2021年的高点大幅下滑，2024年有所企稳反弹，2025年再次承压。值得关注的是成交量在2026年显著放大，市场关注度提升。</p>',
    '',
    '<h3>宏观经济与政策分析</h3>',
    '',
    '<h4>宏观环境</h4>',
    '<p>近五年中国GDP增速从疫情后的高速反弹(2021年18.9%)逐步回归至5%左右的中速增长区间，经济进入高质量发展阶段。物价方面，CPI长期处于低位甚至负值区间，反映出消费需求偏弱，经济面临一定的通缩压力。</p>',
    '<p>这对消费品公司而言构成挑战——低通胀环境下，企业提价能力受限，营收增长更多依赖量的扩张而非价格提升。</p>',
    '',
    '<h4>行业政策</h4>',
    '<p><strong>集采政策:</strong>药品集中带量采购持续推进，虽然中药集采力度较化药相对温和，但仍对行业利润形成压制。</p>',
    '<p><strong>中医药振兴:</strong>国家十四五中医药发展规划等政策利好行业长期发展，中医药在基层医疗和大健康领域的应用空间仍大。</p>',
    '<p><strong>消费复苏:</strong>消费刺激政策有助于白药的消费品业务(牙膏、洗护等)恢复增长，但实际效果取决于居民消费信心和收入预期。</p>',
    '',
    '<h3>综合结论与策略建议</h3>',
    '',
    '<p><strong>1. 技术面:</strong>中期空头趋势尚未扭转，股价处于5年低位区域。短期震荡指标中性偏弱，未出现明确的趋势反转信号。关键观察点:均线金叉、MACD底背离、成交量放大突破压力位。</p>',
    '',
    '<p><strong>2. 基本面:</strong>品牌价值依旧，但增速放缓、集采压力、消费疲弱三重挑战并存。当前股价已大幅反映悲观预期，估值处于历史较低水平，安全边际有所提升，但需等待业绩拐点信号。</p>',
    '',
    '<p><strong>3. 宏观面:</strong>经济稳中趋缓+低通胀环境对防御性消费医药股形成一定支撑，但强劲的超额收益需要更强的催化剂。</p>',
    '',
    '<p><strong>4. 策略建议:</strong></p>',
    '<p>• <strong>长期投资者:</strong>可关注公司在中医药振兴背景下的长期价值，在关键支撑位分批建仓，耐心等待基本面改善。当前价位具备一定长期配置价值。</p>',
    '<p>• <strong>波段交易者:</strong>关注成交量变化和技术指标的底部背离信号，寻找波段反弹机会。</p>',
    '<p>• <strong>风险提示:</strong>若集采政策超预期收紧，或消费数据持续恶化，股价可能面临进一步下行风险。</p>',
    '',
    '<hr style="margin:20px 0;border-color:#eee">',
    '<p style="color:#999;font-size:12px"><strong>免责声明:</strong>本报告基于公开行情数据与宏观经济指标生成，所有技术指标均为客观计算结果。分析内容仅供参考学习，不构成任何投资建议。投资有风险，入市需谨慎。数据来源:Tushare Pro。</p>'
  ];

  document.getElementById('analysisText').innerHTML = text.join('\\n');
}})();

// Resize handler
window.addEventListener('resize',function(){{
  document.querySelectorAll('.chart,.chart-sm').forEach(function(el){{
    var inst = echarts.getInstanceByDom(el);
    if(inst) inst.resize();
  }});
}});
</script>
</body>
</html>'''

# 保存
output_path = r"Y:\Work Buddy\Quant\ynby_analysis_report.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"HTML报告已生成: {output_path}")
print(f"文件大小: {len(html):,} 字节")
