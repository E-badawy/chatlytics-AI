def conversation_health(metrics):
    """
    Calculates a simple conversation health score (0–100).
    """

    score = 0

    # Activity
    avg = metrics["Average Daily"]

    if avg >= 40:
        score += 30
    elif avg >= 20:
        score += 25
    elif avg >= 10:
        score += 20
    elif avg >= 5:
        score += 15
    else:
        score += 10

    # Emoji usage
    if metrics["Emojis"] >= 500:
        score += 20
    elif metrics["Emojis"] >= 200:
        score += 15
    elif metrics["Emojis"] >= 100:
        score += 10
    else:
        score += 5

    # Media usage
    if metrics["Media"] >= 1000:
        score += 20
    elif metrics["Media"] >= 500:
        score += 15
    else:
        score += 10

    # Links shared
    if metrics["Links"] >= 20:
        score += 10
    else:
        score += 5

    # Participant balance
    if metrics["Top %"] < 60:
        score += 20
    elif metrics["Top %"] < 75:
        score += 15
    else:
        score += 10

    score = min(score, 100)

    if score >= 85:
        status = "Excellent 🟢"
    elif score >= 70:
        status = "Good 🟡"
    elif score >= 50:
        status = "Moderate 🟠"
    else:
        status = "Low 🔴"

    return score, status