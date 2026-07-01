from preprocessor import preprocess
import helper

with open("chat_with_hafsat.txt", encoding="utf-8") as f:
    data = f.read()

df = preprocess(data)

print(helper.fetch_stats("Overall", df))
print(helper.most_busy_users(df)[0])
print(helper.monthly_timeline("Overall", df).head())
print(helper.emoji_analysis("Overall", df).head())