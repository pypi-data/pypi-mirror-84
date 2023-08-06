import datetime as dt
import logging
from itertools import chain
import typing as t
import uuid
import re
import requests

import pytz

from . import types as tp
from .helpers import to_ofx_date, clean_query
from .parse import parse_ofx
from .config import Config, DEFAULT_HEADERS


PROFILE_REQUEST = """
<PROFMSGSRQV1>
    <PROFTRNRQ>
        <TRNUID>{trn_uid}</TRNUID>
        <PROFRQ>
            <CLIENTROUTING>MSGSET</CLIENTROUTING>
            <DTPROFUP>{date}</DTPROFUP>
        </PROFRQ>
    </PROFTRNRQ>
</PROFMSGSRQV1>
"""


MESSAGE = """
<{msg_type}MSGSRQV1>
    <{trn_type}TRNRQ>
        <TRNUID>{trn_uid}</TRNUID>
        {request}
    </{trn_type}TRNRQ>
</{msg_type}MSGSRQV1>
"""


STATEMENT_REQUEST = """
<STMTRQ>
    <BANKACCTFROM>
        <BANKID>{bank_id}</BANKID>
        <ACCTID>{account_id}</ACCTID>
        <ACCTTYPE>{account_type}</ACCTTYPE>
    </BANKACCTFROM>
    <INCTRAN>
        <DTSTART>{start_date}</DTSTART>
        <DTEND>{end_date}</DTEND>
        <INCLUDE>Y</INCLUDE>
    </INCTRAN>
</STMTRQ>
"""


CC_STATEMENT_REQUEST = """
<CCSTMTRQ>
    <CCACCTFROM>
        <ACCTID>{account_id}</ACCTID>
    </CCACCTFROM>
    <INCTRAN>
        <DTSTART>{start_date}</DTSTART>
        <DTEND>{end_date}</DTEND>
        <INCLUDE>Y</INCLUDE>
    </INCTRAN>
</CCSTMTRQ>
"""

ACCOUNT_INFO_REQUEST = """
<ACCTINFORQ>
    <DTACCTUP>{start_date}</DTACCTUP>
</ACCTINFORQ>
"""


HEADER = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?OFX OFXHEADER="200"
    VERSION="{version}"
    SECURITY="NONE"
    OLDFILEUID="NONE"
    NEWFILEUID="{new_file_id}"
?>
"""

SIGNON = """
<SIGNONMSGSRQV1>
    <SONRQ>
        <DTCLIENT>{date}</DTCLIENT>
        <USERID>{username}</USERID>
        <USERPASS>{password}</USERPASS>
        <LANGUAGE>ENG</LANGUAGE>
        <FI>
            <ORG>{org}</ORG>
            <FID>{fid}</FID>
        </FI>
        <APPID>{app_id}</APPID>
        <APPVER>{app_version}</APPVER>
        <CLIENTUID>{client_id}</CLIENTUID>
    </SONRQ>
</SIGNONMSGSRQV1>
"""


def _format_headers(headers: t.Dict[str, str]) -> str:
    rv = ""
    for key, val in headers.items():
        rv = rv + "%s: %s\n" % (key, val)
    return rv


def _statement_request(
    account_id: str,
    start_date: dt.datetime,
    end_date: dt.datetime,
    account_type: str,
    bank_id: str,
) -> str:
    req = STATEMENT_REQUEST.format(
        bank_id=bank_id,
        account_id=account_id,
        account_type=account_type,
        start_date=to_ofx_date(start_date),
        end_date=to_ofx_date(end_date),
    )
    return MESSAGE.format(
        msg_type="BANK",
        trn_type="STMT",
        trn_uid=uuid.uuid4(),
        request=req,
    )


def _cc_statement_request(
    account_id: str,
    start_date: dt.datetime,
    end_date: dt.datetime,
) -> str:

    req = CC_STATEMENT_REQUEST.format(
        account_id=account_id,
        start_date=to_ofx_date(start_date),
        end_date=to_ofx_date(end_date),
    )

    return MESSAGE.format(
        msg_type="CREDITCARD",
        trn_type="CCSTMT",
        trn_uid=uuid.uuid4(),
        request=req,
    )


def _account_info_request(
    start_date: dt.datetime,
) -> str:
    req = ACCOUNT_INFO_REQUEST.format(
        start_date=to_ofx_date(start_date),
    )
    return MESSAGE.format(
        msg_type="SIGNUP",
        trn_type="ACCTINFO",
        trn_uid=uuid.uuid4(),
        request=req,
    )


def _log_request(body: str, headers: t.Dict[str, str]) -> None:
    logging.debug(
        "\n\n---- REQUEST HEADERS ----\n\n%s\n"
        "---- REQUEST BODY ----\n\n%sn",
        _format_headers(headers),
        body,
    )


def _log_response(response: requests.Response) -> None:
    logging.debug(
        "\n\n---- RESPONSE HEADERS ----\n\n%s\n"
        "---- RESPONSE BODY ----\n\n%s\n",
        _format_headers(dict(response.headers)),
        response.text,
    )


class Client:

    def __init__(self, config: Config) -> None:
        self.config = config

    def _make_header(self) -> str:
        header = HEADER.format(
            version=self.config["ofx_version"],
            new_file_id=uuid.uuid4()
        )
        return re.sub(
            r"\s+", " ", header.strip().replace("\n", ""))

    def _wrap(self, query: str):
        header = self._make_header()
        query = clean_query(query)
        return "{header}<OFX>{signon}{query}</OFX>".format(
            header=header,
            signon=self._sign_on(),
            query=query,
        )

    def _sign_on(self) -> str:
        """Generate signon message"""
        return SIGNON.format(
            date=to_ofx_date(dt.datetime.utcnow()),
            username=self.config["username"],
            password=self.config["password"],
            org=self.config["org"],
            fid=self.config["fid"],
            app_id=self.config["app_id"],
            app_version=self.config["app_version"],
            client_id=self.config["client_id"],
        )

    def _make_request(
        self,
        query: str,
        *extra_headers: t.Tuple[str, str],
        session: t.Optional[requests.Session] = None,
    ) -> t.Tuple[requests.Response, str]:
        post = session.post if session else requests.post
        headers = {}
        for key, val in chain(DEFAULT_HEADERS.items(), extra_headers):
            headers[key] = val
        body = self._wrap(query)
        _log_request(body, headers)
        response = post(self.config["url"], data=body, headers=headers)
        _log_response(response)
        response.raise_for_status()
        return response, response.text

    def query(self, query: str) -> tp.ParseResult:
        with requests.Session() as http_session:
            http_response, ofx_data = self._make_request(
                query, session=http_session)
            cookies = http_response.headers.get("Set-Cookie", None)
            if (
                len(ofx_data) == 0
                and cookies is not None
            ):
                logging.debug(
                    "Got 0-length 200 response with Set-Cookies header; "
                    "retrying request with cookies"
                )
                _, ofx_data = self._make_request(query, session=http_session)
        return parse_ofx(ofx_data)

    def query_profile(self) -> tp.ParseResult:
        query = PROFILE_REQUEST.format(
            trn_uid=uuid.uuid4(),
            date=to_ofx_date(dt.datetime.utcnow()),
        )
        return self.query(query)

    def query_accounts(
        self,
        date: t.Optional[dt.datetime] = None,
    ) -> tp.ParseResult:
        date = date or dt.datetime(
            1990, 12, 31, tzinfo=pytz.UTC)
        return self.query(_account_info_request(date))

    def query_transactions(
        self,
        account_id: str,
        routing_number: str,
        start_date: t.Optional[dt.datetime] = None,
        end_date: t.Optional[dt.datetime] = None,
        account_type: str = "CHECKING",
    ) -> t.List[tp.Transaction]:
        if end_date is None:
            end_date = dt.datetime.utcnow()
        if start_date is None:
            start_date = end_date - dt.timedelta(days=30)
        else:
            if start_date > end_date:
                raise ValueError(
                    f"Start date {start_date} is greater "
                    f"than end date '{end_date}'")
        account_req = _statement_request(
            account_id,
            start_date,
            end_date,
            account_type,
            routing_number
        )
        result = self.query(account_req)
        return result["transactions"]

    def query_cc_transactions(
        self,
        account_id: str,
        start_date: t.Optional[dt.datetime] = None,
        end_date: t.Optional[dt.datetime] = None,
    ) -> t.List[tp.Transaction]:
        if end_date is None:
            end_date = dt.datetime.utcnow()
        if start_date is None:
            start_date = end_date - dt.timedelta(days=30)
        else:
            if start_date > end_date:
                raise ValueError(
                    f"Start date {start_date} is greater "
                    f"than end date '{end_date}'")
        query = _cc_statement_request(account_id, start_date, end_date)
        result = self.query(query)
        return result["transactions"]
