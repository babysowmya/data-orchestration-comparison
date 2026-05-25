import pandas as pd

def extract_data(input_path):
    df = pd.read_csv(input_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def transform_data(df, blocked_countries):
    df = df[~df["country"].isin(blocked_countries)].copy()  # .copy() fixes the warning
    session = df.groupby("user_id")["timestamp"].agg(["min", "max"])
    session["session_duration"] = (session["max"] - session["min"]).dt.total_seconds()
    df["date"] = df["timestamp"].dt.date
    events = df.groupby(["user_id", "date"]).size().reset_index(name="event_count")
    result = events.merge(
        session["session_duration"],
        left_on="user_id",
        right_index=True
    )
    return result

def load_data(df, output_path):
    df.to_parquet(output_path, engine="pyarrow", index=False)