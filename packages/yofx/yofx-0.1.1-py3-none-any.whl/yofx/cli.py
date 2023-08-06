import argparse
import logging
import os
import sys
import typing as t
import datetime as dt
from . import json
import csv

from .client import Client
from .config import (
    default_config,
    DEFAULT_OFX_VERSION,
    DEFAULT_DOWNLOAD_DAYS
)
from .parse import parse_ofx

DOWNLOAD_DAYS = 30


def environ_or_required(key):
    return (
        {'default': os.environ.get(key)} if os.environ.get(key)
        else {'required': True}
    )


def parse_test_args(subparsers) -> None:
    test = subparsers.add_parser('test', help='Test OFX parse')
    test.set_defaults(func=test_parse)


def parse_acctinfo_args(subparsers) -> None:
    accounts = subparsers.add_parser('accounts', help='List accounts')
    accounts.set_defaults(func=list_accounts)


def parse_tx_args(subparsers) -> None:
    tx_cmd = subparsers.add_parser('tx', help='Query transactions')
    tx_cmd.add_argument(
        "-a", "--account",
        help=(
            "Account ID to query. If not passed then program "
            "looks for OFX_ACCOUNT_ID in the environment."
        ),
        **environ_or_required("OFX_ACCOUNT_ID"),
    )
    tx_cmd.add_argument(
        "-r", "--routing-number",
        help=(
            "Routing number of bank. If not passed then program "
            "looks for OFX_ACCOUNT_ID in the environment."
        ),
        **environ_or_required("OFX_ROUTING_NUMBER"),
    )
    tx_cmd.add_argument(
        "-t", "--account-type",
        help=(
            "Account type (eg CHECKING, MONEYMRKT). If not "
            "passed then program looks for OFX_ACCOUNT_TYPE "
            "in the environment."
        ),
        **environ_or_required("OFX_ACCOUNT_TYPE"),
    )
    tx_cmd.add_argument(
        "--days",
        default=DEFAULT_DOWNLOAD_DAYS,
        type=int,
        help=(
            "number of days to download (default: %s)"
            "" % DEFAULT_DOWNLOAD_DAYS
        ),
    )
    tx_cmd.add_argument(
        "-s", "--start",
        type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d"),
        help="Start date",
    )
    tx_cmd.add_argument(
        "-e", "--end",
        type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d"),
        help="End date",
    )
    tx_cmd.add_argument(
        "-o", "--output-format",
        type=str,
        choices=("csv", "json"),
        default="json",
        help="Set verbosity level",
    )
    tx_cmd.set_defaults(func=list_transactions)


def parse_args() -> t.Dict[str, t.Any]:
    parser = argparse.ArgumentParser(prog="ofxclient")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Set verbosity level",
    )
    parser.add_argument(
        "--ofx-version",
        default=DEFAULT_OFX_VERSION,
        type=int,
        help="OFX version to use (default: %s)" % DEFAULT_OFX_VERSION,
    )
    subparsers = parser.add_subparsers()
    parse_test_args(subparsers)
    parse_acctinfo_args(subparsers)
    parse_tx_args(subparsers)
    return vars(parser.parse_args())


def test_parse(args: dict) -> None:
    input = sys.stdin.read()
    result = parse_ofx(input)
    print(json.dumps(result))


def list_accounts(args: dict) -> None:
    config = default_config()
    client = Client(config)
    result = client.query_accounts()
    print(json.dumps(result["accounts"]))


def list_transactions(args: dict) -> None:
    config = default_config()
    client = Client(config)

    end_date = args["end"]
    if end_date is None:
        end_date = dt.datetime.utcnow()

    start_date = args["start"]
    if start_date is None:
        start_date = end_date - dt.timedelta(days=args["days"])

    transactions = client.query_transactions(
        account_id=args["account"],
        routing_number=args["routing_number"],
        start_date=start_date,
        end_date=end_date,
        account_type=args["account_type"],
    )

    if args["output_format"] == "csv":
        if len(transactions) == 0:
            return
        keys = transactions[0].keys()
        writer = csv.DictWriter(sys.stdout, keys)
        writer.writeheader()
        writer.writerows(transactions)
    else:
        print(json.dumps(transactions))


def main():
    args = parse_args()
    if args["verbose"]:
        logging.basicConfig(level=logging.DEBUG)
    f = args["func"]
    f(args)


if __name__ == "__main__":
    main()
