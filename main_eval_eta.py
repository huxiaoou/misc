import pandas as pd
import argparse
from husfort.qplot import CPlotLinesWithBars


def load_css(css_file: str) -> pd.DataFrame:
    css_data = pd.read_csv(css_file, parse_dates=["datetime"])
    css_data["trade_date"] = css_data["datetime"].dt.strftime("%Y%m%d")
    pivot_css_data = pd.pivot_table(css_data, index="trade_date", columns="code", values="val")
    return pivot_css_data


def load_eta_ret(eta_ret_file: str) -> pd.DataFrame:
    eta_ret_data = pd.read_csv(eta_ret_file, parse_dates=["trade_date"])
    eta_ret_data["trade_date"] = eta_ret_data["trade_date"].dt.strftime("%Y%m%d")
    eta_ret_data = eta_ret_data.set_index("trade_date").rename(columns={"open": "ret"})
    eta_ret_data["nav"] = (1 + eta_ret_data["ret"]).cumprod()
    return eta_ret_data


def plot_indicator(data: pd.DataFrame, indicator: str, nav: str = "nav"):
    indicator_ylim = {
        "VOL": (0.0, 0.10),
        "VMA": (0.0, 0.08),
        "VAR_WITHIN": (0.0, 20),
        "VAR_BETWEEN": (0.0, 20),
        "VAR_TOT": (0.0, 20),
        "VAR_WITHIN_RATIO": (0.0, 2.0),
        "CORR_ABS_AVER": (0.0, 1.0),
    }.get(indicator, (0.0, 1.0))
    artist = CPlotLinesWithBars(
        plot_data=data,
        line_cols=[nav],
        bar_cols=[indicator],
        line_color=["#FF6347"],
        bar_color=["#6495ED"],
        fig_name=f"eta.{nav}-vs-{indicator}",
        fig_save_dir="data",
    )
    artist.plot()
    artist.set_axis_x(xtick_spread=21, xtick_label_rotation=90, xgrid_visible=True)
    artist.set_axis_y(ylim=(1.00, 1.60), ygrid_visible=True)
    artist.set_secondary_y_axis(ylim=indicator_ylim)
    artist.set_legend(loc="upper left")
    artist.save_and_close()
    return


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate ETA indicators")
    parser.add_argument(
        "--indicator",
        type=str,
        default="CORR_ABS_AVER",
        choices=(
            "VOL",
            "VMA",
            "VAR_WITHIN",
            "VAR_BETWEEN",
            "VAR_TOT",
            "VAR_WITHIN_RATIO",
            "CORR_ABS_AVER",
        ),
        help="Indicator to plot",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    css_file = "data/css.csv"
    css_data = load_css(css_file)
    print(css_data)

    eta_ret_file = "data/rets_ALL.csim.main.eta.csv"
    eta_ret_data = load_eta_ret(eta_ret_file)
    print(eta_ret_data)

    main_data = pd.merge(css_data, eta_ret_data, left_index=True, right_index=True, how="right")
    print(main_data)
    print(main_data.max())

    plot_indicator(main_data, indicator=args.indicator)
