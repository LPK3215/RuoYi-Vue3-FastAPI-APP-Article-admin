import socket
import time

import pytest
import requests

from common.config import Config
from common.login_helper import LoginHelper

HTTP_OK = 200
API_OK_CODE = 200
DEFAULT_TIMEOUT_S = 10
SEEDED_PYTHON_ID = 20001


def _is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def _session() -> requests.Session:
    s = requests.Session()
    s.trust_env = False
    return s


def _assert_ok_json(resp: requests.Response) -> dict:
    assert resp.status_code == HTTP_OK, resp.text
    payload = resp.json()
    assert payload.get("code") == API_OK_CODE, payload
    return payload


@pytest.fixture(scope="session")
def http() -> requests.Session:
    return _session()


@pytest.fixture(scope="session")
def admin_token() -> str:
    token = LoginHelper().login(username="admin", password="admin123")
    assert token, "admin token should not be empty (captcha should be disabled in test env)"
    return token


def test_portal_article_list_ok(http: requests.Session) -> None:
    """
    Portal（公开）：文章分页列表接口可用（允许为空列表）
    """
    if not _is_port_open("127.0.0.1", 9099):
        pytest.skip("backend is not running on http://localhost:9099")

    resp = http.get(
        f"{Config.backend_url}/portal/article/list",
        params={"pageNum": 1, "pageSize": 10},
        timeout=DEFAULT_TIMEOUT_S,
    )
    data = _assert_ok_json(resp)
    assert data.get("pageNum") == 1
    assert data.get("pageSize") == 10
    assert isinstance(data.get("rows"), list)
    assert isinstance(data.get("total"), int)


def test_admin_create_article_and_portal_detail(http: requests.Session, admin_token: str) -> None:
    """
    管理端：创建一篇已发布文章，并验证 Portal 详情可访问且包含关联软件列表
    """
    if not _is_port_open("127.0.0.1", 9099):
        pytest.skip("backend is not running on http://localhost:9099")

    headers = {"Authorization": f"Bearer {admin_token}"}
    ts = int(time.time())
    title = f"自动化测试教程_{ts}"

    create_payload = {
        "title": title,
        "summary": "pytest seed article for portal",
        "coverUrl": "",
        "contentMd": f"# {title}\n\n- created by pytest\n- ts: {ts}\n",
        "tags": "pytest,portal,kb",
        "publishStatus": "1",
        "status": "0",
        "articleSort": 99,
        "softwareIds": [SEEDED_PYTHON_ID],
        "remark": "pytest",
    }

    resp_create = http.post(
        f"{Config.backend_url}/tool/kb/article",
        json=create_payload,
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    created = _assert_ok_json(resp_create)
    article_id = (created.get("data") or {}).get("articleId")
    assert isinstance(article_id, int)

    # Portal list should find it by keyword
    resp_list = http.get(
        f"{Config.backend_url}/portal/article/list",
        params={"pageNum": 1, "pageSize": 10, "keyword": title},
        timeout=DEFAULT_TIMEOUT_S,
    )
    listed = _assert_ok_json(resp_list)
    assert any(x.get("articleId") == article_id for x in (listed.get("rows") or [])), listed

    # Portal detail should include related softwares (only on-shelf)
    resp_detail = http.get(
        f"{Config.backend_url}/portal/article/{article_id}",
        timeout=DEFAULT_TIMEOUT_S,
    )
    detail = _assert_ok_json(resp_detail).get("data") or {}
    assert detail.get("articleId") == article_id
    assert detail.get("title") == title
    softwares = detail.get("softwares") or []
    assert isinstance(softwares, list)
    assert any(s.get("softwareId") == SEEDED_PYTHON_ID for s in softwares), softwares

