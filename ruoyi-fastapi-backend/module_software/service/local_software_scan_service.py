import re
import sys
from dataclasses import dataclass
from typing import Any

try:
    import winreg as winreg_module
except ImportError:  # pragma: no cover
    winreg_module = None


winreg: Any = winreg_module


@dataclass
class InstalledSoftware:
    id: str
    name: str
    version: str | None = None
    publisher: str | None = None
    install_location: str | None = None
    icon_path: str | None = None
    url: str | None = None
    uninstall_string: str | None = None
    scope: str | None = None


_UNINSTALL_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"


def _safe_str(v: object) -> str | None:
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def _read_value(key: winreg.HKEYType, value_name: str) -> str | None:
    try:
        v, _t = winreg.QueryValueEx(key, value_name)
        return _safe_str(v)
    except FileNotFoundError:
        return None
    except OSError:
        return None


def _normalize_icon_path(raw: str | None) -> str | None:
    s = _safe_str(raw)
    if not s:
        return None
    # 去掉常见参数与引号，仅保留路径部分（尽量）
    s = s.strip().strip('"')
    # 形如 "C:\path\app.exe,0" 或 "C:\path\app.exe" / "C:\path\app.ico"
    s = re.split(r",\s*\d+$", s)[0]
    return s.strip().strip('"') or None


def _is_noise_name(name: str) -> bool:
    n = name.strip().lower()
    if not n:
        return True
    # 过滤明显的系统组件/更新项（保守一些）
    noise_prefix = (
        'security update',
        'update for',
        'hotfix for',
        'kb',
    )
    if n.startswith(noise_prefix):
        return True
    if n in {'microsoft visual c++', 'microsoft visual c++ redistributable'}:
        return False
    return False


def _normalize_limit(limit: int) -> int:
    safe_limit = int(limit or 0)
    if safe_limit <= 0:
        safe_limit = 500
    return min(3000, safe_limit)


def _match_keyword(keyword: str, display_name: str, display_version: str | None, publisher: str | None) -> bool:
    if not keyword:
        return True
    hay = ' '.join([display_name or '', display_version or '', publisher or '']).lower()
    return keyword in hay


def _append_registry_items(
    results: list[InstalledSoftware], keyword: str, safe_limit: int, root: int, view_flag: int, scope: str
) -> None:
    if winreg is None:
        return

    try:
        base = winreg.OpenKey(root, _UNINSTALL_PATH, 0, winreg.KEY_READ | view_flag)
    except OSError:
        return
    try:
        count, _sub, _mtime = winreg.QueryInfoKey(base)
    except OSError:
        return

    for idx in range(count):
        if len(results) >= safe_limit:
            return
        try:
            sub_name = winreg.EnumKey(base, idx)
            sub_key = winreg.OpenKey(base, sub_name)
        except OSError:
            continue

        try:
            display_name = _read_value(sub_key, 'DisplayName')
            if not display_name or _is_noise_name(display_name):
                continue

            display_version = _read_value(sub_key, 'DisplayVersion')
            publisher = _read_value(sub_key, 'Publisher')
            if not _match_keyword(keyword, display_name, display_version, publisher):
                continue

            results.append(
                InstalledSoftware(
                    id=f'{scope}:{_UNINSTALL_PATH}\\{sub_name}',
                    name=display_name,
                    version=display_version,
                    publisher=publisher,
                    install_location=_read_value(sub_key, 'InstallLocation'),
                    icon_path=_normalize_icon_path(_read_value(sub_key, 'DisplayIcon')),
                    url=_read_value(sub_key, 'URLInfoAbout') or _read_value(sub_key, 'HelpLink'),
                    uninstall_string=_read_value(sub_key, 'UninstallString'),
                    scope=scope,
                )
            )
        finally:
            try:
                winreg.CloseKey(sub_key)
            except OSError:
                pass


def _deduplicate_results(results: list[InstalledSoftware]) -> list[InstalledSoftware]:
    seen: set[tuple[str, str | None, str | None]] = set()
    uniq: list[InstalledSoftware] = []
    for item in results:
        key = (item.name.strip().lower(), (item.version or '').strip() or None, (item.publisher or '').strip() or None)
        if key in seen:
            continue
        seen.add(key)
        uniq.append(item)
    uniq.sort(key=lambda x: x.name.lower())
    return uniq


def scan_installed_software(keyword: str | None = None, limit: int = 500) -> list[InstalledSoftware]:
    if winreg is None or not sys.platform.startswith('win'):
        return []

    kw = (keyword or '').strip().lower()
    safe_limit = _normalize_limit(limit)
    results: list[InstalledSoftware] = []
    _append_registry_items(results, kw, safe_limit, winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY, 'HKLM')
    _append_registry_items(results, kw, safe_limit, winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY, 'WOW6432')
    _append_registry_items(results, kw, safe_limit, winreg.HKEY_CURRENT_USER, 0, 'HKCU')
    return _deduplicate_results(results)
