import datetime
import argparse

import pyxirr
from colorama import Fore, Back, Style
import pandas as pd

from report import trades_for_past

parser = argparse.ArgumentParser()
parser.add_argument("current_val", help="current value of the portfolio in Rs", type=float)


def main():
    args = parser.parse_args()
    current_val = args.current_val
    
    trades = trades_for_past(days=5 * 365)
    # trades = read_json_file("./trades.json")
    trades_df = pd.DataFrame(trades).sort_values(by="trade_date")
    trades_df.reset_index(drop=True, inplace=True)

    dates = []
    amounts = []

    def iter_trades():
        for i in range(len(trades_df)):
            date = datetime.datetime.fromisoformat(trades_df["order_execution_time"][i])
            # print(date)
            # date = trades_df["trade_date"][i]
            amount = (
                (-1 if trades_df["trade_type"][i] == "buy" else 1)
                * trades_df["price"][i]
                * trades_df["quantity"][i]
            )
            yield date, amount

    for date, amount in iter_trades():
        dates.append(date)
        amounts.append(amount)
    dates.append(datetime.datetime.now())
    amounts.append(current_val)

    print(
        Back.RED + Style.BRIGHT,
        "XIRR: ",
        pyxirr.xirr(dates, amounts) * 100,
        "%",
        Style.RESET_ALL,
    )


if __name__ == "__main__":
    main()
