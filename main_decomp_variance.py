import pandas as pd


def weighted_average_and_variance(values: pd.Series, weights: pd.Series) -> tuple[float, float]:
    average: float = values @ weights  # type:ignore
    variance: float = values**2 @ weights - average**2  # type:ignore
    return average, variance


def calculate_decomposition_variance(df: pd.DataFrame) -> tuple[float, float, float]:
    """_summary_

    Args:
        df (pd.DataFrame): has columns "return"(float), "weight"(float), and "sector"(str)

    Returns:
        tuple[float, float, float]: (total_variance, within_sector_variance, between_sector_variance)
    """

    total_average_return, total_variance = weighted_average_and_variance(df["return"], df["weight"])
    result = []
    for sector, group in df.groupby("sector"):
        sector_weight = group["weight"].sum()
        wgt_h = group["weight"] / sector_weight
        sector_average_return, within = weighted_average_and_variance(group["return"], wgt_h)
        between = (sector_average_return - total_average_return) ** 2
        result.append(
            {
                "sector": sector,
                "sector_weight": sector_weight,
                "within": within,
                "between": between,
            }
        )
    group_result = pd.DataFrame(result)
    within_sector_variance: float = group_result["within"] @ group_result["sector_weight"]  # type:ignore
    between_sector_variance: float = group_result["between"] @ group_result["sector_weight"]  # type:ignore
    if abs(total_variance - (within_sector_variance + between_sector_variance)) > 1e-6:
        raise ValueError(
            f"Warning: Total variance {total_variance:.6f} does not equal the sum of within and between variances {within_sector_variance + between_sector_variance:.6f}"
        )
    return total_variance, within_sector_variance, between_sector_variance


def main():
    test_data = pd.DataFrame(
        {
            "return": [0.1, 0.2, -0.3, 0.05],
            "weight": [0.20, 0.40, 0.15, 0.25],
            "sector": ["Tech", "Tech", "Finance", "Finance"],
        }
    )

    tot, within, between = calculate_decomposition_variance(test_data)
    print(f"Total Variance         : {tot:.6f}")
    print(f"Within Sector Variance : {within:.6f}")
    print(f"Between Sector Variance: {between:.6f}")


if __name__ == "__main__":
    main()
