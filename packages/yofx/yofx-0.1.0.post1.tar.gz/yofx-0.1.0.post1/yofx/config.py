import os
import typing_extensions as te
import uuid


DEFAULT_APP_ID = "QWIN"
DEFAULT_APP_VERSION = "2700"
DEFAULT_OFX_VERSION = "220"
DEFAULT_USER_AGENT = "httpclient"
DEFAULT_ACCEPT = "*/*, application/x-ofx"
DEFAULT_HEADERS = {
    "Accept": DEFAULT_ACCEPT,
    "User-Agent": DEFAULT_USER_AGENT,
    "Content-Type": "application/x-ofx",
    "Connection": "Keep-Alive",
}
DEFAULT_DOWNLOAD_DAYS = 30


class Config(te.TypedDict):
    org: str
    fid: str
    url: str
    username: str
    password: str
    client_id: str
    app_id: str
    app_version: str
    ofx_version: str
    user_agent: str
    accept: str


def default_config() -> Config:
    org = os.environ.get("OFX_ORG", "")
    fid = os.environ.get("OFX_FID", "")
    url = os.environ.get("OFX_URL", "")
    username = os.environ.get("OFX_USERNAME", "")
    password = os.environ.get("OFX_PASSWORD", "")
    client_id = os.environ.get("OFX_CLIENT_ID", str(uuid.uuid4()))
    app_id = os.environ.get("OFX_APP_ID", DEFAULT_APP_ID)
    app_version = os.environ.get("OFX_APP_VERSION", DEFAULT_APP_VERSION)
    ofx_version = os.environ.get("OFX_APP_VERSION", DEFAULT_OFX_VERSION)
    user_agent = os.environ.get("OFX_USER_AGENT", DEFAULT_USER_AGENT)
    accept = os.environ.get("OFX_ACCEPT", DEFAULT_ACCEPT)

    return {
        "org": org,
        "fid": fid,
        "url": url,
        "username": username,
        "password": password,
        "client_id": client_id,
        "app_id": app_id,
        "app_version": app_version,
        "ofx_version": ofx_version,
        "user_agent": user_agent,
        "accept": accept,
    }
