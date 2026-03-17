from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import CrudResponseModel
from exceptions.exception import ServiceException
from module_software.dao.software_category_dao import ToolSoftwareCategoryDao
from module_software.dao.software_item_dao import ToolSoftwareDao
from module_software.entity.vo.software_category_vo import ToolSoftwareCategoryModel
from module_software.entity.vo.software_item_vo import ToolSoftwareModel
from module_software.entity.vo.software_scan_vo import (
    LocalInstalledSoftwareModel,
    LocalSoftwareScanImportRequestModel,
    LocalSoftwareScanImportResultModel,
    LocalSoftwareScanQueryModel,
)
from module_software.service.local_software_scan_service import scan_installed_software


DEFAULT_IMPORTED_CATEGORY_CODE = 'local-import'
DEFAULT_IMPORTED_CATEGORY_NAME = '本机导入'


def _trim(s: str | None) -> str | None:
    if s is None:
        return None
    t = str(s).strip()
    return t or None


class ToolSoftwareScanService:
    """本机软件扫描/导入（后台）。"""

    @classmethod
    async def scan_services(cls, query: LocalSoftwareScanQueryModel) -> list[LocalInstalledSoftwareModel]:
        items = scan_installed_software(keyword=query.keyword, limit=query.limit)
        return [
            LocalInstalledSoftwareModel(
                id=i.id,
                name=i.name,
                version=i.version,
                publisher=i.publisher,
                installLocation=i.install_location,
                iconPath=i.icon_path,
                url=i.url,
                uninstallString=i.uninstall_string,
                scope=i.scope,
            )
            for i in items
        ]

    @classmethod
    async def _ensure_default_category(cls, query_db: AsyncSession, operator_name: str) -> int:
        # 沿用现有的分类模型/dao：按 category_code 查，若不存在则创建
        exists = await ToolSoftwareCategoryDao.get_category_detail_by_info(
            query_db,
            ToolSoftwareCategoryModel(categoryCode=DEFAULT_IMPORTED_CATEGORY_CODE),
        )
        if exists and getattr(exists, 'del_flag', '0') == '0':
            return int(exists.category_id)

        now = datetime.now()
        model = ToolSoftwareCategoryModel(
            categoryId=None,
            categoryCode=DEFAULT_IMPORTED_CATEGORY_CODE,
            categoryName=DEFAULT_IMPORTED_CATEGORY_NAME,
            categorySort=999,
            status='0',
            delFlag='0',
            createBy=operator_name,
            createTime=now,
            updateBy=operator_name,
            updateTime=now,
            remark='本机软件扫描导入默认分类',
        )
        db_category = await ToolSoftwareCategoryDao.add_category_dao(query_db, model)
        await query_db.flush()
        return int(db_category.category_id)

    @classmethod
    async def import_services(
        cls,
        query_db: AsyncSession,
        request: LocalSoftwareScanImportRequestModel,
        operator_name: str,
    ) -> CrudResponseModel:
        scanned = scan_installed_software(keyword=None, limit=3000)
        scanned_map = {i.id: i for i in scanned}

        selected_ids = request.ids or []
        if selected_ids:
            selected = [scanned_map.get(i) for i in selected_ids]
            selected = [x for x in selected if x is not None]
        else:
            selected = list(scanned)

        category_id = request.category_id
        if category_id is None or int(category_id or 0) <= 0:
            category_id = await cls._ensure_default_category(query_db, operator_name)

        created = updated = skipped = errors = 0
        error_samples: list[str] = []

        # 通过“同名”判断是否存在（简单且符合你需求）
        for item in selected:
            try:
                name = _trim(item.name)
                if not name:
                    skipped += 1
                    continue

                # 查询同名软件（精确匹配，未删除）
                existing = await ToolSoftwareDao.get_software_detail_by_name(query_db, name)
                existing_id: int | None = int(existing.software_id) if existing else None

                now = datetime.now()
                payload = {
                    'category_id': int(category_id),
                    'software_name': name,
                    'short_desc': _trim(item.publisher),
                    'official_url': _trim(item.url),
                    'tags': None,
                    'status': '0',
                    'del_flag': '0',
                    'publish_status': '0',
                    'software_sort': 0,
                    'update_by': operator_name,
                    'update_time': now,
                }

                # iconPath：如果是本机路径，先不直接暴露，转成备注提示
                icon_path = _trim(item.icon_path)
                install_location = _trim(item.install_location)
                version = _trim(item.version)

                remark_parts: list[str] = []
                if version:
                    remark_parts.append(f'本机版本：{version}')
                if install_location:
                    remark_parts.append(f'安装路径：{install_location}')
                if icon_path:
                    remark_parts.append(f'图标路径：{icon_path}')
                if item.uninstall_string:
                    remark_parts.append('已记录卸载信息')
                if remark_parts:
                    payload['remark'] = '；'.join(remark_parts)[:500]

                if existing_id is None:
                    payload['create_by'] = operator_name
                    payload['create_time'] = now
                    db_software = await ToolSoftwareDao.add_software_dao(query_db, ToolSoftwareModel(**payload))
                    await query_db.flush()
                    created += 1
                else:
                    if not request.update_support:
                        skipped += 1
                        continue

                    # 默认只补齐空字段；overwrite=true 才覆盖
                    current = await ToolSoftwareDao.get_software_detail_by_id(query_db, existing_id)
                    if not current:
                        skipped += 1
                        continue

                    edit_payload = {'software_id': existing_id, **payload}
                    if not request.overwrite:
                        # 不覆盖已有的 short_desc / official_url / remark
                        if getattr(current, 'short_desc', None):
                            edit_payload.pop('short_desc', None)
                        if getattr(current, 'official_url', None):
                            edit_payload.pop('official_url', None)
                        if getattr(current, 'remark', None):
                            edit_payload.pop('remark', None)
                    await ToolSoftwareDao.edit_software_dao(query_db, edit_payload)
                    updated += 1
            except Exception as exc:
                errors += 1
                if len(error_samples) < 10:
                    error_samples.append(f'{getattr(item, "name", "<unknown>")}: {exc}')

        try:
            await query_db.commit()
        except Exception as exc:
            await query_db.rollback()
            raise ServiceException(message=str(exc))

        result = LocalSoftwareScanImportResultModel(
            scanned=len(scanned),
            selected=len(selected),
            created=created,
            updated=updated,
            skipped=skipped,
            errors=errors,
            errorSamples=error_samples,
        )
        return CrudResponseModel(is_success=True, message='导入完成', result=result)



