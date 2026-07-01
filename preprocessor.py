import re
import pandas as pd
import emoji
from urlextract import URLExtract

extractor = URLExtract()


def preprocess(data):
    """
    Convert exported WhatsApp chat into a clean DataFrame.
    """

    # Replace WhatsApp's invisible Unicode spaces
    data = data.replace("\u202f", " ")

    # Pattern for exported chats (12-hour format)
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM|am|pm)\s-\s)'

    split_chat = re.split(pattern, data)

    if len(split_chat) < 3:
        raise ValueError("Unsupported WhatsApp export format.")

    dates = split_chat[1::2]
    messages = split_chat[2::2]

    df = pd.DataFrame({
        "message_date": dates,
        "user_message": messages
    })

    # Convert to datetime
    df["date"] = pd.to_datetime(
        df["message_date"],
        format="%m/%d/%y, %I:%M %p - ",
        errors="coerce"
    )

    df.drop(columns="message_date", inplace=True)

    users = []
    msgs = []

    for message in df["user_message"]:

        entry = re.split(r'^([^:]+):\s', message, maxsplit=1)

        if len(entry) >= 3:
            users.append(entry[1].strip())
            msgs.append(entry[2].strip())
        else:
            users.append("group_notification")
            msgs.append(entry[0].strip())

    df["user"] = users
    df["message"] = msgs

    df.drop(columns="user_message", inplace=True)

    # ==========================
    # Date Features
    # ==========================

    df["only_date"] = df["date"].dt.date
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month_name()
    df["month_num"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["day_name"] = df["date"].dt.day_name()
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    df["period"] = (
        df["hour"].astype(str).str.zfill(2)
        + "-"
        + ((df["hour"] + 1) % 24).astype(str).str.zfill(2)
    )

    # ==========================
    # Feature Engineering
    # ==========================

    df["word_count"] = df["message"].apply(lambda x: len(x.split()))
    df["char_count"] = df["message"].apply(len)

    df["emoji_count"] = df["message"].apply(
        lambda x: len([c for c in x if c in emoji.EMOJI_DATA])
    )

    df["is_media"] = df["message"].str.contains(
        "<Media omitted>",
        case=False,
        na=False
    )

    df["is_deleted"] = df["message"].str.contains(
        "deleted",
        case=False,
        na=False
    )

    df["is_link"] = df["message"].apply(
        lambda x: len(extractor.find_urls(x)) > 0
    )

    # Arrange columns in a consistent order
    df = df[
    [
        "date",
        "user",
        "message",
        "only_date",
        "year",
        "month_num",
        "month",
        "day",
        "day_name",
        "hour",
        "minute",
        "period",
        "word_count",
        "char_count",
        "emoji_count",
        "is_media",
        "is_deleted",
        "is_link",
        ]
    ]

    return df

