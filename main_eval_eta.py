import pandas as pd


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


if __name__ == "__main__":
    css_file = "data/css.csv"
    css_data = load_css(css_file)
    print(css_data)

    eta_ret_file = "data/rets_ALL.csim.main.eta.csv"
    eta_ret_data = load_eta_ret(eta_ret_file)
    print(eta_ret_data)

    main_data = pd.merge(css_data, eta_ret_data, left_index=True, right_index=True, how="right")
    print(main_data)