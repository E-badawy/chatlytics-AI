import pandas as pd


def generate_insights(df, selected_user="Overall"):
    """
    Generate executive-level insights from a WhatsApp conversation.
    """

    # ----------------------------------------
    # Filter user
    # ----------------------------------------

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    if df.empty:
        return {
            "summary": "No data available.",
            "metrics": {}
        }

    # ----------------------------------------
    # Basic Metrics
    # ----------------------------------------

    total_messages = len(df)

    participants = (
        df["user"]
        .replace("group_notification", pd.NA)
        .dropna()
        .nunique()
    )

    start_date = df["date"].min().date()
    end_date = df["date"].max().date()

    total_days = max(
        (df["date"].max() - df["date"].min()).days,
        1
    )

    avg_daily = round(total_messages / total_days, 1)

    media = int(df["is_media"].sum())
    links = int(df["is_link"].sum())
    emojis = int(df["emoji_count"].sum())

    # ----------------------------------------
    # Activity
    # ----------------------------------------

    busiest_month = df["month"].mode()[0]
    busiest_day = df["day_name"].mode()[0]

    busiest_hour = (
        df["hour"]
        .value_counts()
        .idxmax()
    )

    # ----------------------------------------
    # Top User
    # ----------------------------------------

    top_user = (
        df["user"]
        .value_counts()
        .idxmax()
    )

    top_percentage = round(
        (
            df["user"]
            .value_counts()
            .max()
            / total_messages
        ) * 100,
        1,
    )

    # ----------------------------------------
    # Communication Style
    # ----------------------------------------

    if avg_daily > 40:
        engagement = "Very High"

    elif avg_daily > 20:
        engagement = "High"

    elif avg_daily > 10:
        engagement = "Moderate"

    else:
        engagement = "Low"

    # ----------------------------------------
    # Executive Summary
    # ----------------------------------------

    summary = f"""
This conversation contains **{total_messages:,} messages**
shared by **{participants} participant(s)** between
**{start_date}** and **{end_date}**.

Average activity was **{avg_daily} messages per day**,
indicating **{engagement.lower()} engagement**.

The busiest period occurred during **{busiest_month}**,
while **{busiest_day}** recorded the highest activity.

The conversation is most active around **{busiest_hour}:00**.

**{top_user}** contributed approximately
**{top_percentage}%** of all messages.

The chat contains **{media:,} media messages**,
**{links:,} shared links** and
**{emojis:,} emojis**,
suggesting a rich communication pattern.
"""

    metrics = {
        "Messages": total_messages,
        "Participants": participants,
        "Days": total_days,
        "Average Daily": avg_daily,
        "Media": media,
        "Links": links,
        "Emojis": emojis,
        "Top User": top_user,
        "Top %": top_percentage,
        "Peak Month": busiest_month,
        "Peak Day": busiest_day,
        "Peak Hour": busiest_hour,
        "Engagement": engagement,
    }

    return {
        "summary": summary,
        "metrics": metrics,
    }