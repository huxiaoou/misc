import pandas as pd
import argparse
from husfort.qplot import CPlotLinesWithBars

pd.set_option("display.float_format", "{:.6f}".format)


def load_nav(
    bgn: str,
    end: str,
    src_file: str = "data/rets_ALL.csim.main.csv",
    ret: str = "open",
) -> pd.DataFrame:
    ret_df = pd.read_csv(src_file)
    ret_df["nav"] = 1.0 + ret_df[ret].cumsum()
    return ret_df[["trade_date", "nav"]].set_index("trade_date").truncate(before=bgn, after=end)


def load_css(src_file: str = "data/css.csv") -> pd.DataFrame:
    css_df = pd.read_csv(src_file, parse_dates=["datetime"])
    css_df["trade_date"] = css_df["datetime"].map(lambda x: x.strftime("%Y-%m-%d"))
    css_df = css_df.pivot_table(index="trade_date", columns="code", values="val", aggfunc="mean")
    return css_df


def save(data: pd.DataFrame, filename: str):
    data.to_csv(filename, float_format="%.6f")
    return


def plot(data: pd.DataFrame, plot_indicator: str, sec_ylim: tuple[float, float], bgn: str, end: str):
    artist = CPlotLinesWithBars(
        plot_data=data,
        line_cols=["nav"],
        bar_cols=[plot_indicator],
        line_color=["#8B0000"],
        bar_alpha=0.5,
        bar_width=0.5,
        align="center",
        fig_name=f"nav_vs_{plot_indicator}_{bgn}_{end}",
        fig_save_dir="data",
    )
    artist.plot()
    artist.set_axis_x(xtick_count=min(20, len(data)), xtick_label_rotation=90, xgrid_visible=True)
    nav_min, nav_max = data["nav"].min(), data["nav"].max()
    d = nav_max - nav_min
    ylim = (nav_min - d * 0.05, nav_max + d * 0.05)
    artist.set_axis_y(ylim=ylim, ygrid_visible=True)
    artist.set_secondary_y_axis(ylim=sec_ylim)
    artist.set_legend(loc="upper left")
    artist.save_and_close()
    return


def parse_args():
    parser = argparse.ArgumentParser(description="Analyze CSS Epsilon")
    parser.add_argument("--indicator", type=str, required=True, help="Indicator to analyze")
    parser.add_argument("--window", type=int, default=1, help="Rolling window size for moving average")
    parser.add_argument("--yliml", type=float, default=0, help="Lower right y-axis limit")
    parser.add_argument("--ylimu", type=float, default=1, help="Upper right y-axis limit")
    parser.add_argument("--bgn", type=str, default="2018-01-02", help="bgn_date")
    parser.add_argument("--end", type=str, default="2026-06-09", help="end_date")
    return parser.parse_args()


def main():
    args = parse_args()
    indicator = args.indicator
    window = args.window
    sec_ylim = args.yliml, args.ylimu
    bgn, end = args.bgn, args.end

    plot_indicator = f"{indicator}_MA{window}"
    nav_df = load_nav(bgn, end)
    css_df = load_css()
    merged_df = pd.merge(nav_df, css_df, left_index=True, right_index=True, how="left")
    merged_df[plot_indicator] = merged_df[indicator].rolling(window=window).mean()
    print(merged_df)
    save(merged_df, f"data/merged_nav_css_{indicator}_MA{window}_{bgn}_{end}.csv")
    plot(merged_df, plot_indicator, sec_ylim=sec_ylim, bgn=bgn, end=end)


if __name__ == "__main__":
    main()
