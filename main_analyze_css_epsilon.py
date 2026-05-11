from ast import arg
from curses import window

from matplotlib.pylab import f
import pandas as pd
import argparse
from husfort.qplot import CPlotLinesWithBars

pd.set_option("display.float_format", "{:.6f}".format)


def load_nav(src_file: str = "rets_ALL.main.epsilon.csv", ret: str = "open") -> pd.DataFrame:
    ret_df = pd.read_csv(src_file)
    ret_df["nav"] = ret_df[ret].cumsum()
    return ret_df[["trade_date", "nav"]].set_index("trade_date")


def load_css(src_file: str = "css.csv") -> pd.DataFrame:
    css_df = pd.read_csv(src_file, parse_dates=["datetime"])
    css_df["trade_date"] = css_df["datetime"].map(lambda x: x.strftime("%Y-%m-%d"))
    css_df = css_df.pivot_table(index="trade_date", columns="code", values="val", aggfunc="mean")
    return css_df


def save(data: pd.DataFrame, filename: str):
    data.to_csv(filename, float_format="%.6f")
    return


def plot(data: pd.DataFrame, plot_indicator: str, ylim: tuple[float, float]):
    artist = CPlotLinesWithBars(
        plot_data=data,
        line_cols=["nav"],
        bar_cols=[plot_indicator],
        line_color=["#8B0000"],
        bar_alpha=0.5,
        fig_name=f"sector_timing_vs_{plot_indicator}",
        fig_save_dir="data",
    )
    artist.plot()
    artist.set_axis_x(xtick_spread=42, xtick_label_rotation=90, xgrid_visible=True)
    artist.set_axis_y(ylim=(-0.1, 0.6), ygrid_visible=True)
    artist.set_secondary_y_axis(ylim=ylim)
    artist.set_legend(loc="upper left")
    artist.save_and_close()
    return


def parse_args():
    parser = argparse.ArgumentParser(description="Analyze CSS Epsilon")
    parser.add_argument("--indicator", type=str, required=True, help="Indicator to analyze")
    parser.add_argument("--window", type=int, default=5, help="Rolling window size for moving average")
    parser.add_argument("--rylim", type=float, default=5, help="Right y-axis limit")
    parser.add_argument("--lylim", type=float, default=0, help="Left y-axis limit")
    return parser.parse_args()


def main():
    args = parse_args()
    indicator = args.indicator
    window = args.window
    lylim = args.lylim
    rylim = args.rylim

    plot_indicator = f"{indicator}_MA{window}"
    nav_df = load_nav()
    css_df = load_css()
    merged_df = pd.merge(nav_df, css_df, left_index=True, right_index=True, how="left")
    merged_df[plot_indicator] = merged_df[indicator].rolling(window=window).mean()
    print(merged_df.head(20))
    save(merged_df, f"merged_nav_css_{indicator}_MA{window}.csv")
    plot(merged_df, plot_indicator, ylim=(lylim, rylim))


if __name__ == "__main__":
    main()
