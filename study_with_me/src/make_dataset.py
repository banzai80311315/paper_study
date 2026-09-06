import numpy as np
import pandas as pd
import jpholiday


def get_slot(df):
    return df["時刻コード"].rename("slot")


def get_area_price(df, area="エリアプライス東京(円/kWh)"):
    return df[area].rename("price")


def get_holiday_flag(df):
    return pd.Series(
        df.index.map(lambda x: jpholiday.is_holiday(x) or x.weekday() >= 5),
        index=df.index,
        name="is_holiday",
    )


def get_scaled_price(price, is_holiday):
    temp = pd.DataFrame({
        "price": price,
        "is_holiday": is_holiday,
        "date": price.index.date,
    })

    temp["price_weekday"] = np.where(~temp["is_holiday"], temp["price"], np.nan)
    temp["price_holiday"] = np.where(temp["is_holiday"], temp["price"], np.nan)

    daily = temp.groupby("date").agg({"price_weekday": "mean", "price_holiday": "mean"})

    daily["weekday_cummean"] = daily["price_weekday"].expanding().mean()
    daily["holiday_cummean"] = daily["price_holiday"].expanding().mean()
    daily["k"] = daily["weekday_cummean"] / daily["holiday_cummean"]

    temp = temp.merge(daily["k"], left_on="date", right_index=True, how="left")

    price_scaled = temp["price"].copy()
    price_scaled.loc[temp["is_holiday"]] = (
        temp.loc[temp["is_holiday"], "price"] * temp.loc[temp["is_holiday"], "k"]
    )

    price_scaled.name = "price_scaled"
    return price_scaled


def get_spike_indicator(price_scaled, threshold=25):
    return (price_scaled > threshold).astype(int).rename("u")


def get_spike_excess(price_scaled, threshold=25):
    return pd.Series(
        np.where(price_scaled > threshold, price_scaled - threshold, 0.0),
        index=price_scaled.index,
        name="x",
    )


def make_dataset(df, area="エリアプライス東京(円/kWh)", threshold=25):
    slot = get_slot(df)
    price = get_area_price(df, area)
    is_holiday = get_holiday_flag(df)
    price_scaled = get_scaled_price(price, is_holiday)
    u = get_spike_indicator(price_scaled, threshold)
    x = get_spike_excess(price_scaled, threshold)

    return pd.DataFrame({
        "slot": slot,
        "is_holiday": is_holiday,
        "price": price,
        "price_scaled": price_scaled,
        "u": u,
        "x": x,
    })
