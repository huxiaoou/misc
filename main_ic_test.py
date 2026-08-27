if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator
    import pandas as pd

    src_file = "data/pre_opn_ret.csv"
    src_data = pd.read_csv(src_file, index_col=0).fillna(0)

    ret_data = pd.pivot_table(src_data, index="datetime", columns="code", values="pre_opn_ret_major")

    fac = ret_data.rolling(250).sum().dropna(axis=0, how="all")
    ret = ret_data.loc[fac.index]
    print(fac)
    print(ret)

    res = {}
    for h in [1,2,5,10,20]:
        test_ret = ret.rolling(h).sum().shift(-h-1).dropna(axis=0, how="all")
        test_fac = fac.loc[test_ret.index]
        print(test_ret.shape, test_fac.shape)
        ic = test_fac.corrwith(test_ret, axis=1, method="spearman")
        res[h] = ic
    res = pd.DataFrame(res)
    res_cumsum = res.cumsum().dropna(axis=0, how="any")
    print(res_cumsum)

    plt.figure(figsize=(16, 9))
    plt.plot(res_cumsum)
    plt.legend(res_cumsum.columns)
    plt.tick_params(axis='x', rotation=45)
    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(nbins=60))
    plt.show()
    plt.close()

