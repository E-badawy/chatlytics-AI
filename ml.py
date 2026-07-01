from sklearn.cluster import KMeans


def message_clustering(df):

    features = df[
        [
            "word_count",
            "char_count",
            "emoji_count",
            "is_media",
            "is_link",
        ]
    ].copy()

    # Convert booleans to integers
    features["is_media"] = features["is_media"].astype(int)
    features["is_link"] = features["is_link"].astype(int)

    model = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10,
    )

    df = df.copy()
    df["cluster"] = model.fit_predict(features)

    return df