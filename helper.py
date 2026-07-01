from collections import Counter
import pandas as pd
from wordcloud import WordCloud
import emoji


def filter_user(selected_user, df):
    """
    Returns either the whole dataframe or a single user's dataframe.
    """
    if selected_user == "Overall":
        return df
    return df[df["user"] == selected_user]


# ==============================
# Basic Statistics
# ==============================

def fetch_stats(selected_user, df):

    df = filter_user(selected_user, df)

    total_messages = df.shape[0]
    total_words = df["word_count"].sum()
    total_media = df["is_media"].sum()
    total_links = df["is_link"].sum()
    total_emojis = df["emoji_count"].sum()

    return (
    int(total_messages),
    int(total_words),
    int(total_media),
    int(total_links),
    int(total_emojis),
    )


# ==============================
# Busy Users
# ==============================

def most_busy_users(df):

    x = df["user"].value_counts().head()

    percentage = (
        round(df["user"].value_counts() / df.shape[0] * 100, 2)
        .reset_index()
    )

    percentage.columns = ["User", "Percentage"]

    return x, percentage


# ==============================
# Monthly Timeline
# ==============================

def monthly_timeline(selected_user, df):

    df = filter_user(selected_user, df)

    timeline = (
        df.groupby(["year", "month_num", "month"])
        .count()["message"]
        .reset_index()
    )

    timeline["time"] = (
        timeline["month"] + " " + timeline["year"].astype(str)
    )

    return timeline


# ==============================
# Daily Timeline
# ==============================

def daily_timeline(selected_user, df):

    df = filter_user(selected_user, df)

    return (
        df.groupby("only_date")
        .count()["message"]
        .reset_index()
    )


# ==============================
# Week Activity
# ==============================

def week_activity_map(selected_user, df):

    df = filter_user(selected_user, df)

    return df["day_name"].value_counts()


# ==============================
# Month Activity
# ==============================

def month_activity_map(selected_user, df):

    df = filter_user(selected_user, df)

    return df["month"].value_counts()


# ==============================
# Heatmap
# ==============================

def activity_heatmap(selected_user, df):

    df = filter_user(selected_user, df)

    heatmap = df.pivot_table(
        index="day_name",
        columns="period",
        values="message",
        aggfunc="count"
    ).fillna(0)

    return heatmap


# ==============================
# Word Cloud
# ==============================

def create_wordcloud(selected_user, df):

    df = filter_user(selected_user, df)

    temp = df[
        (~df["is_media"]) &
        (df["user"] != "group_notification")
    ]

    wc = WordCloud(
        width=800,
        height=400,
        background_color="white"
    )

    return wc.generate(temp["message"].str.cat(sep=" "))


# ==============================
# Common Words
# ==============================

def most_common_words(selected_user, df):

    df = filter_user(selected_user, df)

    temp = df[
        (~df["is_media"]) &
        (df["user"] != "group_notification")
    ]

    words = []

    for message in temp["message"]:
        words.extend(message.lower().split())

    common = pd.DataFrame(
        Counter(words).most_common(20),
        columns=["Word", "Count"]
    )

    return common


# ==============================
# Emoji Analysis
# ==============================

def emoji_analysis(selected_user, df):

    df = filter_user(selected_user, df)

    emojis = []

    for message in df["message"]:
        emojis.extend(
            [c for c in message if c in emoji.EMOJI_DATA]
        )

    emoji_df = pd.DataFrame(
        Counter(emojis).most_common(),
        columns=["Emoji", "Count"]
    )

    return emoji_df