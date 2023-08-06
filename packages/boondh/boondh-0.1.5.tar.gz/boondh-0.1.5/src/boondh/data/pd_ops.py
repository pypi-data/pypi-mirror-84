from pandas import DataFrame, Series
from numpy import nan
from string import ascii_uppercase
from random import randint


def series_most_freq(series: Series) -> object:
    """Returns most feq value in the series. Good as agg function.

    Args:
        series (Series): Pandas series

    Returns:
        object: Either the series value or numpy.nan
    """
    series = series.dropna().values.tolist()
    if series:
        return max(series, key=series.count)
    return nan


def df_filter_values_above_freq(
    df: DataFrame, column_name: str, freq: int
) -> DataFrame:
    """Filters data frame on a column's value counts.

    Args:
        df (DataFrame): DataFrame to be filtered
        column_name (str): target column
        freq (int): minimum freq (inclusive) of values in that column to be accepted in new dataframe

    Returns:
        DataFrame: DataFrame with only those rows which have values that occur in that column more than `freq` times
    """
    assert_column_in_dataframe(column_name, df)
    value_counts = df[column_name].value_counts()
    values_with_freq_above = value_counts.loc[value_counts >= freq].index.values
    return df.loc[df[column_name].isin(values_with_freq_above)]


def df_get_dummy() -> DataFrame:
    """Create a dummy dataframe for experiments..

    Returns:
        DataFrame: DataFrame of shape (26, 3)
    """
    sales = [randint(0, 100) for _ in range(len(ascii_uppercase))]
    category = [sale // 10 for sale in sales]
    data = DataFrame(
        {"name": list(ascii_uppercase), "sales": sales, "category": category,}
    )
    return data.sample(data.shape[0]).reset_index(drop=True)


def assert_column_in_dataframe(column_name: str, df: DataFrame):
    """Assert column in a dataframe

    Args:
        column_name (str): desired column
        df (DataFrame): target dataframe
    """
    assert (
        column_name in df.columns.values
    ), f"{column_name} not in DataFrame\nColumns={df.columns.values.tolist()}"


if __name__ == "__main__":
    df = df_get_dummy()
    print(df_filter_values_above_freq(df, "category", 5))
    print(series_most_freq(Series([1,2,3,4,1,2,3,2,3,2])))
