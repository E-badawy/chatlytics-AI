def generate_recommendations(metrics):
    """
    Generate simple business recommendations from chat metrics.
    """

    recs = []

    # Engagement
    if metrics["Average Daily"] < 10:
        recs.append(
            "Increase communication frequency to improve engagement."
        )
    else:
        recs.append(
            "Conversation activity is healthy and consistently maintained."
        )

    # Emoji
    if metrics["Emojis"] < 100:
        recs.append(
            "Emoji usage is relatively low. Richer emotional expression may improve engagement."
        )

    # Links
    if metrics["Links"] < 5:
        recs.append(
            "Very few links were shared. Consider sharing more resources or references."
        )

    # Media
    if metrics["Media"] > 1000:
        recs.append(
            "High media sharing indicates visually rich communication."
        )

    # Participation
    if metrics["Top %"] > 70:
        recs.append(
            "One participant dominates the conversation. More balanced participation may improve interaction."
        )
    else:
        recs.append(
            "Participation appears well balanced across users."
        )

    return recs