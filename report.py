import time
import json
import datetime
import requests

from colorama import Fore, Back, Style

from utils import read_file_as_string, get_cookie

ENDPOINT = "https://console.zerodha.com/"


def get_equity_trade_records(from_date, to_date):
    current_page = 1

    def get_page(page):
        trade_report_uri = f"{ENDPOINT}/api/reports/tradebook?segment=EQ&from_date={from_date}&to_date={to_date}&page={page}"
        cookies = get_cookie("./console.cookie")
        headers = {
            "x-csrftoken": read_file_as_string("./console.x-csrftoken"),
        }
        response = requests.get(trade_report_uri, cookies=cookies, headers=headers)
        if response.status_code != 200:
            print(response.content)
            raise Exception(
                f"Failed to get the equity trade record: {from_date} to {to_date}"
            )
        response = json.loads(response.content)
        if response["status"] != "success":
            raise Exception(
                f"Failed to get the equity trade record: {from_date} to {to_date}"
            )
        if response["data"]["state"] == "PENDING":
            print(
                Fore.YELLOW + "Waiting 5 sec to get the pending status done",
                Style.RESET_ALL,
            )
            time.sleep(5)
            return get_page(page)

        trades = response["data"]["result"]
        pagination = response["data"]["pagination"]
        return trades, pagination["page"], pagination["per_page"], pagination["total"]

    trades = []

    total = 0
    max_total = 1e10
    current_page = 1
    while total < max_total:
        current_trades, page_no, page_size, max_total = get_page(current_page)
        print(
            Fore.GREEN
            + f"Page: {current_page}, From date: {from_date}, To date: {to_date}, Count: {len(current_trades)}",
            Style.RESET_ALL,
        )
        trades.extend(current_trades)
        current_page = current_page + 1
        total += page_size

    return trades


def trades_for_past(days, step_size_days=365):
    all_trades = []

    to_date = datetime.datetime.now()
    while days > 0:
        from_date = to_date - datetime.timedelta(
            days=step_size_days if days >= step_size_days else days
        )
        trades = get_equity_trade_records(
            from_date=from_date.date(), to_date=to_date.date()
        )
        all_trades.extend(trades)

        to_date = from_date - datetime.timedelta(days=1)
        days = days - step_size_days

    return all_trades
