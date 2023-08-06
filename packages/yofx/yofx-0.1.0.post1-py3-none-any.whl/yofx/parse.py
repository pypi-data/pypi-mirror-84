import decimal
import datetime
import typing as t
import xml.etree.ElementTree as ET
from itertools import chain

from . import types as tp
from .helpers import from_ofx_date, to_decimal


def noop(val: str) -> str:
    return val


def extract_contents(node: ET.Element, name: str) -> t.Optional[str]:
    child_node = node.find(name)
    if child_node is None or not child_node.text:
        return None
    return child_node.text.strip()


def parse_account(node: ET.Element) -> tp.Account:
    account = tp.defaults.account()
    description = extract_contents(node, "DESC")
    if description is not None:
        account["description"] = description

    try:
        account_info = next(chain(
            node.iter("BANKACCTFROM"),
            node.iter("CCACCTROM"),
            node.iter("INVACCTFROM"),
        ))
    except StopIteration as error:
        raise ValueError(
            "None of 'BANKACCTFROM', 'CCACCTFROM' "
            "or 'INVACCTFROM' was found"
        ) from error

    account_id = extract_contents(account_info, "ACCTID")
    if account_id is not None:
        account["account_id"] = account_id

    routing_number = extract_contents(account_info, "BANKID")
    if routing_number is not None:
        account["routing_number"] = routing_number

    branch_id = extract_contents(account_info, "BRANCHID")
    if branch_id is not None:
        account["branch_id"] = branch_id

    account_type = extract_contents(account_info, "ACCTTYPE")
    if account_type is not None:
        account["account_type"] = account_type

    broker_id = extract_contents(account_info, "BROKERID")
    if broker_id is not None:
        account["broker_id"] = broker_id

    return account


def parse_status(node: ET.Element) -> tp.Status:
    rv = tp.defaults.status()

    code = extract_contents(node, "CODE")
    if code is not None:
        rv["code"] = int(code)

    severity = extract_contents(node, "SEVERITY")
    if severity is not None:
        rv["severity"] = severity

    message = extract_contents(node, "MESSAGE")
    if message is not None:
        rv["message"] = message

    return rv


def parse_signon_response(node: ET.Element) -> tp.Signon:
    rv = tp.defaults.signon()

    status_node = node.find("STATUS")
    if status_node is not None:
        rv["status"] = parse_status(node)

    intu_bid = extract_contents(node, "INTU.BID")
    if intu_bid is not None:
        rv["intu_bid"] = intu_bid

    language = extract_contents(node, "LANGUAGE")
    if language is not None:
        rv["language"] = language

    dtserver = extract_contents(node, "DTSERVER")
    if dtserver is not None:
        rv["dtserver"] = dtserver

    dtprofup = extract_contents(node, "DTPROFUP")
    if dtprofup is not None:
        rv["dtprofup"] = dtprofup

    return rv


def parse_balance(
    node: ET.Element,
    bal_tag_name: str,
) -> t.Optional[t.Tuple[decimal.Decimal, datetime.datetime]]:

    balance = node.find(bal_tag_name)
    if not balance or not balance.text:
        return None

    amount_str = extract_contents(balance, "BALAMT")
    if amount_str is None:
        raise ValueError("Missing BALAMT tag")

    try:
        amount = to_decimal(amount_str)
    except (IndexError, decimal.InvalidOperation) as error:
        raise ValueError("Empty balance") from error

    date_str = extract_contents(balance, "DTASOF")
    if date_str is None:
        raise ValueError("Missing DTASOF tag.")

    date = from_ofx_date(date_str)

    return amount, date


def parse_statement(node: ET.Element) -> tp.Statement:
    rv = tp.defaults.statement()

    start_date = extract_contents(node, "DTSTART")
    if start_date is not None:
        rv["start_date"] = from_ofx_date(start_date)

    end_date = extract_contents(node, "DTEND")
    if end_date is not None:
        rv["end_date"] = from_ofx_date(end_date)

    currency = extract_contents(node, "CURDEF")
    if currency is not None:
        rv["currency"] = currency

    balance = parse_balance(node, "ledgerbal")
    if balance is not None:
        amount, date = balance
        rv["balance"] = amount
        rv["balance_date"] = date

    balance = parse_balance(node, "availbal")
    if balance is not None:
        amount, date = balance
        rv["available_balance"] = amount
        rv["available_balance_date"] = date

    for tx_node in node.findall("stmttrn"):
        rv["transactions"].append(parse_transaction(tx_node))

    return rv


def parse_transaction(node: ET.Element) -> tp.Transaction:
    rv = tp.defaults.transaction()

    type_ = extract_contents(node, "TRNTYPE")
    if type_ is not None:
        rv["type"] = type_.lower()

    payee = extract_contents(node, "NAME")
    if payee is not None:
        rv["payee"] = payee

    memo = extract_contents(node, "MEMO")
    if memo is not None:
        rv["memo"] = memo

    amount = extract_contents(node, "TRNAMT")
    if amount is not None:
        rv["amount"] = to_decimal(amount)

    date_posted = extract_contents(node, "DTPOSTED")
    if date_posted is not None:
        rv["date"] = from_ofx_date(date_posted)

    fitid = extract_contents(node, "ID")
    if fitid is not None:
        rv["id"] = fitid

    return rv


def parse_ofx(ofx_str: str) -> tp.ParseResult:
    rv = tp.defaults.parse_result()
    node = ET.fromstring(ofx_str)

    try:
        rv["signon"] = parse_signon_response(
            next(node.iter("SONRS")))
    except StopIteration as error:
        raise ValueError("Missing SONRS tag.") from error

    try:
        status_node = next(node.iter("STATUS"))
    except StopIteration as error:
        raise ValueError("Missing STATUS tag.") from error
    else:
        rv["status"] = parse_status(status_node)

    for child_node in node.iter("ACCTINFO"):
        account_ = parse_account(child_node)
        rv["accounts"].append(account_)

    for child_node in node.iter("STMTTRN"):
        transaction = parse_transaction(child_node)
        rv["transactions"].append(transaction)

    return rv
