import pandas as pd

# 讀取 CSV
df = pd.read_csv('cnyes_headlines_202504.csv')
df.columns = df.columns.str.strip()
df = df.rename(columns={'時間': 'date', '標題': 'title'})
df['date'] = pd.to_datetime(df['date']).dt.date

# 關鍵詞設定
positive_keywords = [
    '創高', '創新高', '成長', '營收創高', '強勁', '回升', '擴張',
    '超預期', '買盤強勁', '收紅', '創新紀錄', '業績亮眼'
]
negative_keywords = [
    '下跌', '崩跌', '重挫', '利空', '疲弱', '萎縮', '下修',
    '衰退', '賣壓沉重', '收黑', '虧損擴大', '低迷'
]

# 標題轉換為情緒分數
def get_sentiment(title):
    if pd.isna(title):
        return 0
    for word in positive_keywords:
        if word in title:
            return 1
    for word in negative_keywords:
        if word in title:
            return -1
    return 0

df['sentiment'] = df['title'].apply(get_sentiment)

# 每日原始總分
daily_sentiment = df.groupby('date')['sentiment'].sum().reset_index()
daily_sentiment = daily_sentiment.rename(columns={'date': '日期', 'sentiment': '每日原始總分'})

# 正規化為 -1 / 0 / 1
def normalize(score):
    if score > 0:
        return 1
    elif score < 0:
        return -1
    else:
        return 0

daily_sentiment['情緒分類'] = daily_sentiment['每日原始總分'].apply(normalize)

# 輸出 CSV
daily_sentiment.to_csv('daily_sentiment_result.csv', index=False, encoding='utf-8-sig')
print("已輸出含每日原始總分與情緒分類的結果為 daily_sentiment_result.csv")

