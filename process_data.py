import json, os

# Read the raw MCP data file
raw_path = r'C:\Users\test\.workbuddy\projects\y-Work Buddy-Quant\47b63767-2c16-43f9-9dc3-18a009351ced\tool-results\mcp-connector-proxy-tushareMcp_daily-1782747925829-09215f.txt'
with open(raw_path, 'r') as f:
    data = json.load(f)

# Sort by date ascending
data.sort(key=lambda x: x['trade_date'])

print(f"Total trading days: {len(data)}")
print(f"Date range: {data[0]['trade_date']} to {data[-1]['trade_date']}")

# Save processed data
output_path = r'Y:\Work Buddy\Quant\daily_data_5y.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

print(f"Data saved to {output_path}")
