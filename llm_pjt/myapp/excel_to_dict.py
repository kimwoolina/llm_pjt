import pandas as pd

# 엑셀 파일을 읽어들임
df = pd.read_excel('static/myapp/location.xlsx')

location_data = {}

# 각 행
for _, row in df.iterrows():
    level1 = row['1단계'] if pd.notna(row['1단계']) else None
    level2 = row['2단계'] if pd.notna(row['2단계']) else None
    level3 = row['3단계'] if pd.notna(row['3단계']) else None
    x = row['격자 X']
    y = row['격자 Y']
    
    if pd.notna(level3):
        location_data[level3] = {'x': x, 'y': y}
    elif pd.notna(level2):
        location_data[level2] = {'x': x, 'y': y}
    elif pd.notna(level1):
        location_data[level1] = {'x': x, 'y': y}

print(location_data)
