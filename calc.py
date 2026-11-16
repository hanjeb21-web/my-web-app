import pandas as pd


def load_readiness(path):
    return pd.read_csv(path)


def total_rate(df):
    planned = df["계획시간(h)"].sum()
    if planned == 0:
        return 0.0
    return round(float(df["가동시간(h)"].sum() / planned * 100), 1)


def rate_by_equipment(df):
    result = (
        df.groupby(["장비코드", "장비명"], as_index=False)[["계획시간(h)", "가동시간(h)"]]
        .sum()
        .rename(columns={"계획시간(h)": "계획시간", "가동시간(h)": "가동시간"})
    )
    result["가동률"] = (
        result["가동시간"].div(result["계획시간"].where(result["계획시간"] != 0, pd.NA))
        .mul(100)
        .fillna(0)
        .round(1)
    )
    return result[["장비코드", "장비명", "계획시간", "가동시간", "가동률"]]


def compare_weeks(prev, cur):
    previous = rate_by_equipment(prev)[["장비코드", "장비명", "가동률"]].rename(
        columns={"가동률": "가동률_이전"}
    )
    current = rate_by_equipment(cur)[["장비코드", "장비명", "가동률"]].rename(
        columns={"가동률": "가동률_이번"}
    )
    result = previous.merge(current, on=["장비코드", "장비명"], how="inner")
    result["증감"] = (result["가동률_이번"] - result["가동률_이전"]).round(1)
    return result[["장비코드", "장비명", "가동률_이전", "가동률_이번", "증감"]].sort_values(
        "증감", ascending=False, ignore_index=True
    )
