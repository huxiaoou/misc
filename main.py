from numpy import isin
import pandas as pd
import argparse
from husfort.qevaluation import CNAV
from husfort.qplot import CPlotLines
from pyparsing import col


def parse_args():
    args_parser = argparse.ArgumentParser(description="Entry point")
    args_parser.add_argument("func", type=str, choices=("nav", "md"))
    return args_parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.func == "nav":
        data_src: dict[str, str] = {
            "beta": "rets_ALL.main.beta.csv",
            "gamma": "rets_ALL.main.gamma.csv",
        }

        data_b = pd.read_csv(data_src["beta"]).set_index("trade_date")
        data_g = pd.read_csv(data_src["gamma"]).set_index("trade_date")
        w = 0.67
        rets = pd.DataFrame(
            {
                "beta": data_b["dual"],
                "gamma": data_g["dual"],
                "comb": data_b["dual"] * w + data_g["dual"] * (1 - w),
            }
        ).truncate(after="2025-09-30")
        print(rets)

        res: dict = {}
        for portfolio_id in rets.columns:
            portfolio_rets = rets[portfolio_id]
            nav = CNAV(input_srs=portfolio_rets, input_type="RET")
            nav.cal_all_indicators()
            res[portfolio_id] = nav.reformat_to_display()
        res_df = pd.DataFrame.from_dict(res, orient="index")
        print(res_df)

        nav = (1 + rets).cumprod()
        artist = CPlotLines(
            plot_data=nav,
            fig_name="nav_comb",
            fig_save_dir=".",
            line_width=1.0,
            line_style=["-.", "-.", "-"],
            line_color=["#696969", "#1E90FF", "#800000"],
        )
        artist.plot()
        artist.save_and_close()
    elif args.func == "md":
        pd.set_option("display.width", 0)

        bgn, end = "20230101", "20250930"
        w0, w1 = 240, 60
        instrument = "br"
        exchange_old, exchange_new = ".SHF", "_SHFE"

        n0, n1 = f"mtm{w0}", f"mtm{w1}"
        data_src: dict[str, str] = {
            "tq": f"md.{instrument}.tq.csv",
            "ts": f"md.{instrument}.ts.csv",
        }

        data_tq = pd.read_csv(data_src["tq"], parse_dates=["datetime"])
        data_tq["trade_date"] = data_tq["datetime"].map(lambda z: z.strftime("%Y%m%d"))
        data_tq["to"] = data_tq["volume"] / data_tq["open_interest"].rolling(window=2).mean()
        data_tq["ret_adj"] = data_tq["pre_close_ret"] * data_tq["to"]
        data_tq[n0] = data_tq["ret_adj"].rolling(window=w0).sum()
        data_tq[n1] = data_tq["ret_adj"].rolling(window=w1).sum()
        data_tq["mtm"] = data_tq[n0] * ((w1 / w0) ** 0.5) - data_tq[n1]
        data_tq = data_tq[["trade_date", "real_code", "close", "to", "ret_adj", n0, n1, "mtm"]].query(
            f"trade_date >= '{bgn}' and trade_date <= '{end}'"
        )
        print(data_tq)

        data_ts = pd.read_csv(data_src["ts"], dtype={"trade_date": str})
        data_ts = data_ts.rename(
            columns={
                "ticker_major": "real_code",
                "close_major": "close",
                "vol_major": "volume",
                "amount_major": "turnvoer",
                "oi_major": "open_interest",
                "return_c_major": "pre_close_ret",
            }
        )
        data_ts["real_code"] = data_ts["real_code"].map(
            lambda z: z.replace(exchange_old, exchange_new) if isinstance(z, str) else ""
        )
        data_ts["to"] = data_ts["volume"] / data_ts["open_interest"].rolling(window=2).mean()
        data_ts["ret_adj"] = data_ts["pre_close_ret"] * data_ts["to"]
        data_ts[n0] = data_ts["ret_adj"].rolling(window=w0).sum()
        data_ts[n1] = data_ts["ret_adj"].rolling(window=w1).sum()
        data_ts["mtm"] = data_ts[n0] * ((w1 / w0) ** 0.5) - data_ts[n1]
        data_ts = data_ts[["trade_date", "real_code", "close", "to", "ret_adj", n0, n1, "mtm"]].query(
            f"trade_date >= '{bgn}' and trade_date <= '{end}'"
        )
        print(data_ts)

        result = (
            pd.merge(left=data_tq, right=data_ts, on="trade_date", how="left", suffixes=("_tq", "_ts"))
            .set_index("trade_date")
            .sort_index(axis=1)
        )
        print(result)
        breakpoint()
        result.to_csv(f"md.{instrument}.ts_tq.{bgn}.{end}.csv", float_format="%.6f")

        diff_data = result.query("real_code_tq != real_code_ts")
        print(f"{'diff':-^60s}")
        print(diff_data)