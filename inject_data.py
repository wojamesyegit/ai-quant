import json

# Read the JSON data
with open(r'Y:\Work Buddy\Quant\yunnan_baiyao_daily.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Read the HTML template
with open(r'Y:\Work Buddy\Quant\yunnan_baiyao_chart.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the placeholder with the actual data
html = html.replace('DATA_PLACEHOLDER', json.dumps(data, ensure_ascii=False))

# Write the final HTML file
with open(r'Y:\Work Buddy\Quant\yunnan_baiyao_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("最终HTML文件已生成: Y:\Work Buddy\Quant\yunnan_baiyao_dashboard.html")
