# **********************************************************************************************************************
# Imports
# **********************************************************************************************************************
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# **********************************************************************************************************************
# Pipeline / Procedure: From data to plot
# **********************************************************************************************************************

'''
1. Get data and transform to a panda data frame
'''
file = os.getcwd() + "\\yahoo_info\\" + "total_annual_data.csv"
symbol = "GOOGL"

df = pd.read_csv(file, sep=';', decimal=",")

# reverse the rows - so that latest quarter is last element in the list. Goal: Improve plots
df = df[::-1]

# List of plot types
plot_list = [
    # PLOT TYPE 1
    ["TotalRevenue", "CostOfRevenue", "GrossProfit", "GrossMargin"],
    # PLOT TYPE 2
    ["OperatingExpenses", "OperatingIncome", "OperatingMargin"],  # ,"NetIncome"
    # PLOT TYPE 3
    ["CurrentAssets", "CashAndEquivalents", "CurrentLiabilities", "CashRatio", "CurrentRatio"],
    # PLOT TYPE 4
    ["TotalAssets", "StockholdersEquity", "TotalLiabilities", "EquityRatio"],
    # PLOT TYPE 5
    ["StockholdersEquity", "Goodwill", "IntangibleAssets", "GoodwillRatio"],
    # PLOT TYPE 6
    ["OperatingExpenses", "SellingGeneralAdministrative", "ResearchAndDevelopment"],
    # PLOT TYPE 7
    ["TotalOtherExpenses", "TaxProvision", "NetInterestExpenses"],  # TaxRate
    # PLOT TYPE 8
    ["OperatingCashflow", "CapitalExpenditures", "FreeCashflow"]  # "FCFRatio","OCFRatio"

]

color_list = ["blue", "green", "red", "cyan", "magenta", "yellow", "black"]

relative_indicator = ["GrossMargin", "OperatingMargin", "CashRatio", "CurrentRatio", "EquityRatio", "GoodwillRatio",
                      "ResearchRatio", "InterestRatio", "TaxRate", "FCFratio", "OCFRatio"]


def plot(plot_idx):
    # Create Figure Object
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    # Get Time Scale
    x_values = df["index"]

    ind = np.arange(len(x_values))

    # Bar Plotting
    w = 0
    width = 0.15

    # iterate over every plot list
    for i, item in enumerate(plot_list[plot_idx]):
        # show dates as x ticks in plot
        ax1.set_xticklabels(x_values)

        # if current parameter is a relative indicator
        if item in relative_indicator:
            ax2.plot(ind + w, df[item], label=item, color=color_list[i])
            ax2.scatter(ind + w, df[item], color=color_list[i])

            # annotate the values on the data points
            for i, j in zip(ind + w, df[item]):
                # multiply with 100 to plot in percentage
                ax2.annotate(str(round(j * 100, 2)), xy=(i, j))

            y_lim = max(df[item])
            if y_lim > 1:
                ax2.set_ylim([0, y_lim])
            else:
                ax2.set_ylim([0, 1])

        else:
            # plot indicator
            ax1.bar(ind + w, df[item], width=0.15, label=item, color=color_list[i])

            data = df[item]
            # calculate percentage change and store return values in change
            change = data.pct_change(periods=1)
            change = change.replace(np.nan, 0.0)

            # convert to list and multiply to 100 to plot relative data
            array = change.tolist()
            array = list(map(lambda x: x * 100, array))

            array = list(map(lambda x: round(x, 2), array))

            # annotate relative data
            counter = 0
            for i, j in zip(ind + w, data):
                rel_change = array[counter]
                ax1.annotate(str(rel_change), xy=(i, j))
                counter += 1

            w += width

    # show grid
    ax1.grid(visible=None, which='major', axis='both')
    plt.xticks(ind + width / 2, rotation="vertical")

    plt.title(f'{symbol} Data')

    ax1.set_ylabel('USD')
    ax2.set_ylabel('Ratio')
    # plot_full_screen()

    ax1.legend(loc='center left', bbox_to_anchor=(0, 0.5))
    ax2.legend(loc='center right', bbox_to_anchor=(1, 0.5))
    plt.show()


for idx in range(0, len(plot_list)):
    plot(idx)

# TODO error handling and check if all data has the same data length
# TODO what is to be done when adding indicator: 1. add to list if relative


# **********************************************************************************************************************
# TICKERS
# **********************************************************************************************************************
tech = ["INTC", "AMD", "NVDA", "AAPL", "MSFT", "QCOM", "MRVL", "ASML", "STM", "SNPS", "AMBA", "ZS"]

network = ["NOK", "VZ", "T"]

automotive = ["MBG.DE", "VWAGY", "TSLA", "P911.DE"]

consumer = ["PRG", "KO", "MCD", "NKE", "DIS"]

pharma_companies = ["JNJ", "PFE", "ABBV", "MRK", "GSK"]

energy = ["EQNR", "CVX", "COP", "XOM", "RDS-B", "BP", "RWE.DE", "ENEL.MI"]

chemestry = ["BASF", "WCH.DE"]
