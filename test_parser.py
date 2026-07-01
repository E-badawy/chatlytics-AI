from preprocessor import preprocess

with open("chat_with_hafsat.txt", "r", encoding="utf-8") as f:
    data = f.read()

df = preprocess(data)

print(df.head())
print()
print(df.info())
print()
print(df.columns)
print()
print(df.sample(5))

print(df["date"].isna().sum())

print(df["user"].value_counts())