def preprocess_heart(df):
    df["sex"] = df["sex"].map({"Male": 1, "Female": 0})

    df["exercise_induced_angina"] = df["exercise_induced_angina"].map({
        "Yes": 1,
        "No": 0
    })

    df["chest_pain_type"] = df["chest_pain_type"].map({
        "Typical angina": 0,
        "Atypical angina": 1,
        "Non-anginal pain": 2,
        "Asymptomatic": 3
    })

    return df