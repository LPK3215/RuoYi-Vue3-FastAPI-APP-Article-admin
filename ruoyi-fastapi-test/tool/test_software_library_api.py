import time

import pytest
import requests

from common.config import Config
from common.login_helper import LoginHelper

HTTP_OK = 200
API_OK_CODE = 200
DEFAULT_TIMEOUT_S = 10
DEFAULT_PAGE_SIZE = 10
SEEDED_PYTHON_ID = 20001
EXPECTED_DOWNLOAD_COUNT = 2
EXPECTED_RESOURCE_COUNT = 2


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


def test_portal_categories(http: requests.Session) -> None:
    resp = http.get(f"{Config.backend_url}/portal/software/categories", timeout=DEFAULT_TIMEOUT_S)
    data = _assert_ok_json(resp)
    assert isinstance(data.get("data"), list)
    assert len(data["data"]) > 0

    names = {x.get("categoryName") for x in data["data"]}
    assert "开发工具" in names


def test_portal_list_pagination_and_keyword(http: requests.Session) -> None:
    resp = http.get(
        f"{Config.backend_url}/portal/software/list",
        params={"pageNum": 1, "pageSize": DEFAULT_PAGE_SIZE},
        timeout=DEFAULT_TIMEOUT_S,
    )
    data = _assert_ok_json(resp)
    assert data.get("pageNum") == 1
    assert data.get("pageSize") == DEFAULT_PAGE_SIZE
    assert isinstance(data.get("rows"), list)
    assert data.get("total", 0) >= len(data["rows"])
    assert isinstance(data.get("hasNext"), bool)

    resp_kw = http.get(
        f"{Config.backend_url}/portal/software/list",
        params={"pageNum": 1, "pageSize": DEFAULT_PAGE_SIZE, "keyword": "Python"},
        timeout=DEFAULT_TIMEOUT_S,
    )
    kw = _assert_ok_json(resp_kw)
    assert any("Python" in (x.get("softwareName") or "") for x in kw.get("rows", [])), kw

    # V2 filters: openSource / tag
    resp_os = http.get(
        f"{Config.backend_url}/portal/software/list",
        params={"pageNum": 1, "pageSize": DEFAULT_PAGE_SIZE, "openSource": "1"},
        timeout=DEFAULT_TIMEOUT_S,
    )
    os_data = _assert_ok_json(resp_os)
    assert os_data.get("total", 0) > 0
    assert all((x.get("openSource") == "1") for x in os_data.get("rows", [])), os_data

    resp_tag = http.get(
        f"{Config.backend_url}/portal/software/list",
        params={"pageNum": 1, "pageSize": DEFAULT_PAGE_SIZE, "tag": "python"},
        timeout=DEFAULT_TIMEOUT_S,
    )
    tag_data = _assert_ok_json(resp_tag)
    assert any(x.get("softwareId") == SEEDED_PYTHON_ID for x in tag_data.get("rows", [])), tag_data


def test_portal_facets(http: requests.Session) -> None:
    resp = http.get(f"{Config.backend_url}/portal/software/facets", timeout=DEFAULT_TIMEOUT_S)
    data = _assert_ok_json(resp)
    facets = data.get("data") or {}

    assert isinstance(facets.get("tags"), list)
    assert any(x.get("value") == "python" for x in facets.get("tags", [])), facets

    assert isinstance(facets.get("licenses"), list)
    assert any("PSF-2.0" in (x.get("value") or "") for x in facets.get("licenses", [])), facets

    assert isinstance(facets.get("platforms"), list)
    assert any(x.get("value") == "windows" for x in facets.get("platforms", [])), facets


def test_portal_detail_contains_downloads(http: requests.Session) -> None:
    # Use seeded softwareId=20001 (Python)
    resp = http.get(f"{Config.backend_url}/portal/software/{SEEDED_PYTHON_ID}", timeout=DEFAULT_TIMEOUT_S)
    data = _assert_ok_json(resp)
    detail = data.get("data") or {}
    assert detail.get("softwareId") == SEEDED_PYTHON_ID
    assert detail.get("softwareName") == "Python"
    assert isinstance(detail.get("downloads"), list)
    assert len(detail["downloads"]) >= 1
    assert any(x.get("platform") == "windows" for x in detail["downloads"])
    assert isinstance(detail.get("resources"), list)
    assert len(detail["resources"]) >= 1
    assert any("docs.python.org" in (x.get("resourceUrl") or "") for x in detail["resources"])


def test_admin_category_and_software_crud(http: requests.Session, admin_token: str) -> None:  # noqa: PLR0915
    headers = {"Authorization": f"Bearer {admin_token}"}
    ts = int(time.time())

    # 1) create category
    cat_name = f"自动化测试分类_{ts}"
    cat_payload = {
        "categoryName": cat_name,
        "categoryCode": f"test_{ts}",
        "categorySort": 99,
        "status": "0",
        "remark": "pytest seed",
    }
    resp = http.post(
        f"{Config.backend_url}/tool/software/category",
        json=cat_payload,
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    _assert_ok_json(resp)

    # 2) find category id
    resp = http.get(
        f"{Config.backend_url}/tool/software/category/list",
        params={"pageNum": 1, "pageSize": DEFAULT_PAGE_SIZE, "categoryName": cat_name},
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    data = _assert_ok_json(resp)
    rows = data.get("rows") or []
    assert len(rows) == 1
    category_id = rows[0].get("categoryId")
    assert isinstance(category_id, int)

    # 3) create software (with downloads)
    sw_name = f"自动化测试软件_{ts}"
    sw_payload = {
        "categoryId": category_id,
        "softwareName": sw_name,
        "softwareSort": 99,
        "shortDesc": "pytest create/edit/delete",
        "iconUrl": "",
        "officialUrl": "https://example.com",
        "repoUrl": "https://github.com/example/repo",
        "author": "pytest",
        "team": "pytest-team",
        "license": "MIT",
        "openSource": "1",
        "tags": "test,dev",
        "descriptionMd": f"# {sw_name}\n\n- 自动化测试插入\n- 用于验证 CRUD",
        "usageMd": "## 使用\n\n- 这是一条自动化测试数据",
        "publishStatus": "1",
        "status": "0",
        "downloads": [
            {"platform": "windows", "downloadUrl": "https://example.com/windows", "version": "1.0.0", "sort": 1},
            {"platform": "web", "downloadUrl": "https://example.com", "version": "1.0.0", "sort": 2},
        ],
        "resources": [
            {"resourceType": "doc", "title": "Docs", "resourceUrl": "https://example.com/docs", "sort": 1},
            {"resourceType": "link", "title": "Home", "resourceUrl": "https://example.com", "sort": 2},
        ],
        "remark": "pytest",
    }
    resp = http.post(
        f"{Config.backend_url}/tool/software/item",
        json=sw_payload,
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    _assert_ok_json(resp)

    # 4) category should not be deletable while used
    resp = http.delete(
        f"{Config.backend_url}/tool/software/category/{category_id}",
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    assert resp.status_code == HTTP_OK
    deny = resp.json()
    assert deny.get("code") != API_OK_CODE, deny

    # 5) find software id and detail
    resp = http.get(
        f"{Config.backend_url}/tool/software/item/list",
        params={"pageNum": 1, "pageSize": DEFAULT_PAGE_SIZE, "softwareName": sw_name},
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    data = _assert_ok_json(resp)
    sw_rows = data.get("rows") or []
    assert len(sw_rows) == 1
    software_id = sw_rows[0].get("softwareId")
    assert isinstance(software_id, int)

    resp = http.get(
        f"{Config.backend_url}/tool/software/item/{software_id}",
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    detail = _assert_ok_json(resp).get("data") or {}
    assert detail.get("softwareName") == sw_name
    assert isinstance(detail.get("downloads"), list)
    assert len(detail["downloads"]) == EXPECTED_DOWNLOAD_COUNT
    assert detail.get("openSource") == "1"
    assert detail.get("license") == "MIT"
    assert isinstance(detail.get("resources"), list)
    assert len(detail["resources"]) == EXPECTED_RESOURCE_COUNT

    # 5.2) facets should include tag/license/platform for this new software (admin endpoint)
    resp = http.get(
        f"{Config.backend_url}/tool/software/item/facets",
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    facets = _assert_ok_json(resp).get("data") or {}
    assert any((x.get("value") == "MIT") for x in facets.get("licenses", [])), facets
    assert any((x.get("value") == "test") for x in facets.get("tags", [])), facets
    assert any((x.get("value") == "web") for x in facets.get("platforms", [])), facets

    # 5.1) list filter by tag/platform should include it
    resp = http.get(
        f"{Config.backend_url}/tool/software/item/list",
        params={"pageNum": 1, "pageSize": DEFAULT_PAGE_SIZE, "tag": "test", "platform": "web"},
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    flt = _assert_ok_json(resp)
    assert any(x.get("softwareId") == software_id for x in flt.get("rows", [])), flt

    # 5.1.1) list filter by officialUrl/repoUrl should include it
    resp = http.get(
        f"{Config.backend_url}/tool/software/item/list",
        params={
            "pageNum": 1,
            "pageSize": DEFAULT_PAGE_SIZE,
            "officialUrl": "example.com",
            "repoUrl": "github.com/example/repo",
        },
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    flt = _assert_ok_json(resp)
    assert any(x.get("softwareId") == software_id for x in flt.get("rows", [])), flt

    # 5.3) overview (dashboard) should be available for admin
    resp = http.get(
        f"{Config.backend_url}/tool/software/item/overview",
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    overview = _assert_ok_json(resp).get("data") or {}
    assert isinstance(overview.get("kpi"), dict)
    assert "softwareTotal" in (overview.get("kpi") or {})
    assert isinstance(overview.get("facets"), dict)
    assert isinstance(overview.get("quality"), dict)
    assert isinstance(overview.get("recent"), list)
    assert isinstance(overview.get("drafts"), list)
    if overview.get("recent"):
        first = overview["recent"][0]
        assert "softwareId" in first and "softwareName" in first, first
    if overview.get("drafts"):
        first = overview["drafts"][0]
        assert "softwareId" in first and "softwareName" in first, first

    # 5.4) export should return xlsx binary (zip header 'PK')
    resp = http.post(
        f"{Config.backend_url}/tool/software/item/export",
        data={"pageNum": 1, "pageSize": DEFAULT_PAGE_SIZE, "tag": "test"},
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    assert resp.status_code == HTTP_OK
    assert resp.content[:2] == b"PK", resp.content[:32]

    # 5.5) import template should be available and importData should accept it (no rows)
    resp = http.post(
        f"{Config.backend_url}/tool/software/item/importTemplate",
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    assert resp.status_code == HTTP_OK
    template_bytes = resp.content
    assert template_bytes[:2] == b"PK", template_bytes[:32]

    resp = http.post(
        f"{Config.backend_url}/tool/software/item/importData",
        params={"updateSupport": 0},
        files={
            "file": (
                "software_import_template.xlsx",
                template_bytes,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    msg = _assert_ok_json(resp).get("msg") or ""
    assert "无数据" in msg or "导入完成" in msg, msg

    # 5.6) batch governance: move category + manage tags
    cat_name_to = f"自动化测试分类_目标_{ts}"
    resp = http.post(
        f"{Config.backend_url}/tool/software/category",
        json={
            "categoryName": cat_name_to,
            "categoryCode": f"test_to_{ts}",
            "categorySort": 100,
            "status": "0",
            "remark": "pytest seed (target)",
        },
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    _assert_ok_json(resp)

    resp = http.get(
        f"{Config.backend_url}/tool/software/category/list",
        params={"pageNum": 1, "pageSize": DEFAULT_PAGE_SIZE, "categoryName": cat_name_to},
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    data = _assert_ok_json(resp)
    rows = data.get("rows") or []
    assert len(rows) == 1
    category_id_to = rows[0].get("categoryId")
    assert isinstance(category_id_to, int)

    resp = http.put(
        f"{Config.backend_url}/tool/software/item/batchMoveCategory",
        json={"softwareIds": [software_id], "categoryId": category_id_to},
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    _assert_ok_json(resp)

    resp = http.get(
        f"{Config.backend_url}/tool/software/item/{software_id}",
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    detail = _assert_ok_json(resp).get("data") or {}
    assert detail.get("categoryId") == category_id_to
    assert detail.get("categoryName") == cat_name_to

    resp = http.put(
        f"{Config.backend_url}/tool/software/item/batchManageTags",
        json={"softwareIds": [software_id], "action": "append", "tags": "ops,cli"},
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    _assert_ok_json(resp)

    resp = http.put(
        f"{Config.backend_url}/tool/software/item/batchManageTags",
        json={"softwareIds": [software_id], "action": "remove", "tags": "dev"},
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    _assert_ok_json(resp)

    resp = http.put(
        f"{Config.backend_url}/tool/software/item/batchManageTags",
        json={"softwareIds": [software_id], "action": "replace", "tags": "prod;stable\n"},
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    _assert_ok_json(resp)

    resp = http.get(
        f"{Config.backend_url}/tool/software/item/{software_id}",
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    detail = _assert_ok_json(resp).get("data") or {}
    tags = [x.strip() for x in (detail.get("tags") or "").split(",") if x.strip()]
    assert set(tags) == {"prod", "stable"}, tags

    # 6) batch change publish status -> draft
    resp = http.put(
        f"{Config.backend_url}/tool/software/item/batchChangePublishStatus",
        json={"softwareIds": [software_id], "publishStatus": "0"},
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    _assert_ok_json(resp)

    resp = http.get(
        f"{Config.backend_url}/tool/software/item/{software_id}",
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    detail = _assert_ok_json(resp).get("data") or {}
    assert detail.get("publishStatus") == "0"

    # 6.1) change publish status -> off shelf and portal should not find it via keyword
    resp = http.put(
        f"{Config.backend_url}/tool/software/item/changePublishStatus",
        json={"softwareId": software_id, "publishStatus": "2"},
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    _assert_ok_json(resp)

    resp = http.get(
        f"{Config.backend_url}/portal/software/list",
        params={"pageNum": 1, "pageSize": DEFAULT_PAGE_SIZE, "keyword": sw_name},
        timeout=DEFAULT_TIMEOUT_S,
    )
    portal = _assert_ok_json(resp)
    assert portal.get("total") == 0

    # 7) delete software, then delete category
    resp = http.delete(
        f"{Config.backend_url}/tool/software/item/{software_id}",
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    _assert_ok_json(resp)

    resp = http.delete(
        f"{Config.backend_url}/tool/software/category/{category_id}",
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    _assert_ok_json(resp)

    resp = http.delete(
        f"{Config.backend_url}/tool/software/category/{category_id_to}",
        headers=headers,
        timeout=DEFAULT_TIMEOUT_S,
    )
    _assert_ok_json(resp)
