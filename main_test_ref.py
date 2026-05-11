import pandas as pd


def test_df_ref(df: pd.DataFrame):
    print("In funciton, before operation df id:", id(df))
    df = df * 100
    print("In funciton, after operation df id:", id(df))
    return


if __name__ == "__main__":
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    print("Before function call df id:", id(df))
    test_df_ref(df)
    print("After function call df id:", id(df))
