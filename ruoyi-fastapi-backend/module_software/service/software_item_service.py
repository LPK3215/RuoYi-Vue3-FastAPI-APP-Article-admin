import io
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import pandas as pd
from fastapi import UploadFile
from sqlalchemy import exists, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_software.dao.software_category_dao import ToolSoftwareCategoryDao
from module_software.dao.software_facets_dao import SoftwareFacetsDao
from module_software.dao.software_item_dao import ToolSoftwareDao, ToolSoftwareDownloadDao, ToolSoftwareResourceDao
from module_software.entity.do.software_do import (
    ToolSoftware,
    ToolSoftwareCategory,
    ToolSoftwareDownload,
    ToolSoftwareResource,
)
from module_software.entity.vo.software_dashboard_vo import (
    SoftwareDashboardKpiModel,
    SoftwareDashboardListItemModel,
    SoftwareDashboardOverviewModel,
    SoftwareDashboardQualityModel,
)
from module_software.entity.vo.software_facets_vo import SoftwareFacetItemModel, SoftwareFacetsModel
from module_software.entity.vo.software_item_vo import (
    DeleteToolSoftwareModel,
    ToolSoftwareBatchMoveCategoryModel,
    ToolSoftwareBatchPublishStatusModel,
    ToolSoftwareBatchTagsModel,
    ToolSoftwareDownloadModel,
    ToolSoftwareModel,
    ToolSoftwarePageQueryModel,
    ToolSoftwarePublishStatusModel,
    ToolSoftwareResourceModel,
)
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil

MAX_SOFTWARE_TAGS_LENGTH = 500


@dataclass(frozen=True, slots=True)
class SoftwareImportCategoryCache:
    by_id: dict[int, int]
    by_code: dict[str, int]
    by_name: dict[str, int]


class ToolSoftwareService:
    """
    软件信息模块服务层
    """

    @staticmethod
    def _split_tags(tags: str) -> list[str]:
        # 支持中文逗号/分号、换行等输入
        raw = tags or ''
        raw = raw.replace('，', ',').replace('；', ',').replace(';', ',')
        raw = raw.replace('\r\n', ',').replace('\n', ',').replace('\r', ',').replace('\t', ',')
        parts = [p.strip() for p in raw.split(',')]
        # 同一软件内的 tag 去重，避免重复计数
        seen: set[str] = set()
        result: list[str] = []
        for p in parts:
            if not p or p in seen:
                continue
            seen.add(p)
            result.append(p)
        return result

    @classmethod
    async def get_facets_services(cls, query_db: AsyncSession, limit: int = 50) -> SoftwareFacetsModel:
        """
        获取后台“软件筛选项”聚合数据（用于构建筛选 UI/下拉选项）。

        仅排除软删数据。
        """
        safe_limit = max(1, min(int(limit or 50), 200))

        # tags: 逗号分隔字段，使用 Python 统计
        tag_strings = await SoftwareFacetsDao.get_tag_strings(query_db, mode='tool')
        tag_counter: Counter[str] = Counter()
        for s in tag_strings:
            for tag in cls._split_tags(s):
                tag_counter[tag] += 1
        tag_items = [
            SoftwareFacetItemModel(value=v, count=c)
            for v, c in sorted(tag_counter.items(), key=lambda x: (-x[1], x[0]))[:safe_limit]
        ]

        license_rows = await SoftwareFacetsDao.get_group_counts(query_db, mode='tool', field_name='license', limit=safe_limit)
        author_rows = await SoftwareFacetsDao.get_group_counts(query_db, mode='tool', field_name='author', limit=safe_limit)
        team_rows = await SoftwareFacetsDao.get_group_counts(query_db, mode='tool', field_name='team', limit=safe_limit)
        platform_rows = await SoftwareFacetsDao.get_platform_counts(query_db, mode='tool', limit=safe_limit)

        return SoftwareFacetsModel(
            tags=tag_items,
            licenses=[SoftwareFacetItemModel(**r) for r in license_rows],
            authors=[SoftwareFacetItemModel(**r) for r in author_rows],
            teams=[SoftwareFacetItemModel(**r) for r in team_rows],
            platforms=[SoftwareFacetItemModel(**r) for r in platform_rows],
        )

    @classmethod
    async def get_dashboard_overview_services(
        cls, query_db: AsyncSession, limit: int = 12, recent_limit: int = 6
    ) -> SoftwareDashboardOverviewModel:
        """
        获取后台“软件库首页看板”数据（聚合接口）。

        目标：
        - 减少前端多次分页请求带来的开销
        - 提供维度分布（facets）与数据质量（quality）用于产品化看板展示
        """
        safe_limit = max(1, min(int(limit or 12), 200))
        safe_recent = max(1, min(int(recent_limit or 6), 50))

        base = ToolSoftware.del_flag == '0'

        def is_blank(col: Any) -> Any:
            return or_(col.is_(None), func.trim(col) == '')

        async def count_software(*conds: Any) -> int:
            stmt = select(func.count()).select_from(ToolSoftware).where(base, *conds)
            return int((await query_db.execute(stmt)).scalar_one())

        async def count_category(*conds: Any) -> int:
            stmt = select(func.count()).select_from(ToolSoftwareCategory).where(ToolSoftwareCategory.del_flag == '0', *conds)
            return int((await query_db.execute(stmt)).scalar_one())

        # KPI
        total = await count_software()
        published = await count_software(ToolSoftware.publish_status == '1')
        draft = await count_software(ToolSoftware.publish_status == '0')
        offline = await count_software(ToolSoftware.publish_status == '2')
        categories = await count_category()

        kpi = SoftwareDashboardKpiModel(
            software_total=total,
            published=published,
            draft=draft,
            offline=offline,
            categories=categories,
        )

        # Facets
        facets = await cls.get_facets_services(query_db, limit=safe_limit)

        # Quality
        download_exists = exists(
            select(1).select_from(ToolSoftwareDownload).where(ToolSoftwareDownload.software_id == ToolSoftware.software_id)
        )
        resource_exists = exists(
            select(1).select_from(ToolSoftwareResource).where(ToolSoftwareResource.software_id == ToolSoftware.software_id)
        )

        quality = SoftwareDashboardQualityModel(
            missing_icon=await count_software(is_blank(ToolSoftware.icon_url)),
            missing_license=await count_software(is_blank(ToolSoftware.license)),
            missing_official_url=await count_software(is_blank(ToolSoftware.official_url)),
            missing_short_desc=await count_software(is_blank(ToolSoftware.short_desc)),
            missing_tags=await count_software(is_blank(ToolSoftware.tags)),
            missing_downloads=await count_software(~download_exists),
            missing_resources=await count_software(~resource_exists),
        )

        # Lists
        recent_stmt = (
            select(
                ToolSoftware.software_id,
                ToolSoftware.software_name,
                ToolSoftware.short_desc,
                ToolSoftware.publish_status,
                ToolSoftware.update_time,
            )
            .select_from(ToolSoftware)
            .where(base)
            .order_by(ToolSoftware.update_time.desc(), ToolSoftware.software_id.desc())
            .limit(safe_recent)
        )
        recent_rows = (await query_db.execute(recent_stmt)).mappings().all()
        recent = [
            SoftwareDashboardListItemModel(**CamelCaseUtil.transform_result(dict(r))) for r in (recent_rows or [])
        ]

        drafts_stmt = (
            select(
                ToolSoftware.software_id,
                ToolSoftware.software_name,
                ToolSoftware.short_desc,
                ToolSoftware.publish_status,
                ToolSoftware.update_time,
            )
            .select_from(ToolSoftware)
            .where(base, ToolSoftware.publish_status == '0')
            .order_by(ToolSoftware.update_time.desc(), ToolSoftware.software_id.desc())
            .limit(safe_recent)
        )
        drafts_rows = (await query_db.execute(drafts_stmt)).mappings().all()
        drafts = [
            SoftwareDashboardListItemModel(**CamelCaseUtil.transform_result(dict(r))) for r in (drafts_rows or [])
        ]

        return SoftwareDashboardOverviewModel(kpi=kpi, facets=facets, quality=quality, recent=recent, drafts=drafts)

    @classmethod
    async def get_software_list_services(
        cls, query_db: AsyncSession, query_object: ToolSoftwarePageQueryModel, is_page: bool = False
    ) -> PageModel[ToolSoftwareModel] | list[dict[str, Any]]:
        """
        获取软件分页列表信息service
        """
        query_result = await ToolSoftwareDao.get_software_list(query_db, query_object, is_page)
        if is_page:
            software_list_result = PageModel[ToolSoftwareModel](
                **{
                    **query_result.model_dump(by_alias=True),
                    'rows': [
                        {
                            **(row[0] or {}),
                            'categoryName': (row[1] or {}).get('categoryName') if isinstance(row[1], dict) else None,
                        }
                        for row in query_result.rows
                    ],
                }
            )
            return software_list_result
        if not query_result:
            return []
        return [
            {**(row[0] or {}), 'categoryName': (row[1] or {}).get('categoryName') if isinstance(row[1], dict) else None}
            for row in query_result
        ]

    @staticmethod
    async def export_software_list_services(software_list: list[dict[str, Any]]) -> bytes:
        """
        导出软件信息列表（Excel）。

        说明：仅导出列表页常用字段，避免把 Markdown 大字段一并导出导致文件过大。
        """
        mapping_dict = {
            'softwareId': '软件ID',
            'softwareName': '软件名称',
            'categoryName': '分类',
            'publishStatus': '发布状态',
            'status': '状态',
            'openSource': '是否开源',
            'license': '许可证',
            'tags': '标签',
            'author': '作者',
            'team': '团队/组织',
            'officialUrl': '官网地址',
            'repoUrl': '仓库地址',
            'shortDesc': '简短描述',
            'updateTime': '更新时间',
            'createTime': '创建时间',
            'remark': '备注',
        }

        publish_map = {'0': '草稿', '1': '上架', '2': '下架'}
        status_map = {'0': '正常', '1': '停用'}

        for item in software_list:
            publish = item.get('publishStatus')
            if publish is not None:
                item['publishStatus'] = publish_map.get(str(publish), str(publish))

            status = item.get('status')
            if status is not None:
                item['status'] = status_map.get(str(status), str(status))

            open_source = item.get('openSource')
            item['openSource'] = '是' if str(open_source) == '1' else '否'

        return ExcelUtil.export_list2excel(software_list, mapping_dict)

    @staticmethod
    async def get_software_import_template_services() -> bytes:
        """
        获取软件导入模板service

        说明：当前模板仅覆盖“软件基础信息”，下载/资源等明细建议导入后在详情页维护。
        """
        header_list = [
            '软件ID（可选）',
            '分类ID（可选）',
            '分类编码（可选）',
            '分类名称（必填）',
            '软件名称（必填）',
            '简短描述',
            '图标URL',
            '官网地址',
            '仓库地址',
            '作者',
            '团队/组织',
            '许可证',
            '是否开源',
            '标签（逗号分隔）',
            '发布状态',
            '状态',
            '排序',
            '备注',
        ]
        selector_header_list = ['是否开源', '发布状态', '状态']
        option_list = [
            {'是否开源': ['是', '否']},
            {'发布状态': ['草稿', '上架', '下架']},
            {'状态': ['正常', '停用']},
        ]
        return ExcelUtil.get_excel_template(
            header_list=header_list, selector_header_list=selector_header_list, option_list=option_list
        )

    @staticmethod
    def _software_import_header_map() -> dict[str, str]:
        return {
            '软件ID（可选）': 'softwareId',
            '软件ID': 'softwareId',
            '分类ID（可选）': 'categoryId',
            '分类ID': 'categoryId',
            '分类编码（可选）': 'categoryCode',
            '分类编码': 'categoryCode',
            '分类名称（必填）': 'categoryName',
            '分类名称': 'categoryName',
            '软件名称（必填）': 'softwareName',
            '软件名称': 'softwareName',
            '简短描述': 'shortDesc',
            '图标URL': 'iconUrl',
            '官网地址': 'officialUrl',
            '仓库地址': 'repoUrl',
            '作者': 'author',
            '团队/组织': 'team',
            '许可证': 'license',
            '是否开源': 'openSource',
            '标签（逗号分隔）': 'tags',
            '标签': 'tags',
            '发布状态': 'publishStatus',
            '状态': 'status',
            '排序': 'softwareSort',
            '备注': 'remark',
        }

    @staticmethod
    def _import_cell_str(value: Any) -> str:
        if value is None or pd.isna(value):
            return ''
        return str(value).strip()

    @classmethod
    def _import_cell_int(cls, value: Any) -> int | None:
        if value is None or pd.isna(value) or isinstance(value, bool):
            return None
        if isinstance(value, int):
            return int(value)
        if isinstance(value, float):
            return int(value) if value.is_integer() else None
        s = str(value).strip()
        if not s:
            return None
        try:
            if '.' in s:
                f = float(s)
                return int(f) if f.is_integer() else None
            return int(s)
        except Exception:
            return None

    @classmethod
    def _parse_open_source(cls, value: Any, default: str | None) -> str | None:
        s = cls._import_cell_str(value)
        if not s:
            return default
        s = s.lower()
        if s in {'1', '是', 'y', 'yes', 'true', '开源'}:
            return '1'
        if s in {'0', '否', 'n', 'no', 'false', '闭源'}:
            return '0'
        return default

    @classmethod
    def _parse_publish_status(cls, value: Any, default: str | None) -> str | None:
        s = cls._import_cell_str(value)
        if not s:
            return default
        m = {'草稿': '0', '上架': '1', '下架': '2'}
        if s in m:
            return m[s]
        if s in {'0', '1', '2'}:
            return s
        return default

    @classmethod
    def _parse_status(cls, value: Any, default: str | None) -> str | None:
        s = cls._import_cell_str(value)
        if not s:
            return default
        m = {'正常': '0', '停用': '1'}
        if s in m:
            return m[s]
        if s in {'0', '1'}:
            return s
        return default

    @classmethod
    def _should_skip_import_row(cls, row: Mapping[str, Any]) -> bool:
        if cls._import_cell_int(row.get('softwareId')):
            return False
        if cls._import_cell_str(row.get('softwareName')):
            return False
        return not any(cls._import_cell_str(row.get(k)) for k in ('categoryId', 'categoryCode', 'categoryName'))

    @classmethod
    def _resolve_import_category_id(cls, row: Mapping[str, Any], cache: SoftwareImportCategoryCache) -> int | None:
        cid = cls._import_cell_int(row.get('categoryId'))
        if cid is not None:
            return cache.by_id.get(cid)
        code = cls._import_cell_str(row.get('categoryCode')).lower()
        if code:
            return cache.by_code.get(code)
        name = cls._import_cell_str(row.get('categoryName'))
        if name:
            return cache.by_name.get(name)
        return None

    @staticmethod
    async def _build_import_category_cache(query_db: AsyncSession) -> SoftwareImportCategoryCache:
        rows = (
            (
                await query_db.execute(
                    select(
                        ToolSoftwareCategory.category_id,
                        ToolSoftwareCategory.category_code,
                        ToolSoftwareCategory.category_name,
                    ).where(ToolSoftwareCategory.del_flag == '0')
                )
            )
            .all()
            or []
        )
        by_id: dict[int, int] = {int(r[0]): int(r[0]) for r in rows if r and r[0] is not None}
        by_code: dict[str, int] = {}
        by_name: dict[str, int] = {}
        for r in rows:
            if not r or r[0] is None:
                continue
            cid = int(r[0])
            code = ToolSoftwareService._import_cell_str(r[1]).lower()
            if code:
                by_code[code] = cid
            name = ToolSoftwareService._import_cell_str(r[2])
            if name:
                by_name[name] = cid
        return SoftwareImportCategoryCache(by_id=by_id, by_code=by_code, by_name=by_name)

    @classmethod
    async def _get_existing_ids_for_import(cls, query_db: AsyncSession, df: pd.DataFrame) -> set[int]:
        if 'softwareId' not in df.columns:
            return set()
        ids: list[int] = []
        for v in df['softwareId'].tolist():
            sid = cls._import_cell_int(v)
            if sid:
                ids.append(sid)
        if not ids:
            return set()
        return set(await ToolSoftwareDao.get_existing_software_ids(query_db, sorted(set(ids))))

    @classmethod
    def _maybe_set_text(
        cls,
        payload: dict[str, Any],
        row: Mapping[str, Any],
        key: str,
        *,
        normalize_tags: bool = False,
    ) -> None:
        value = cls._import_cell_str(row.get(key))
        if not value:
            return
        payload[key] = value.replace('，', ',') if normalize_tags else value

    @classmethod
    def _build_import_update_payload(
        cls,
        *,
        row: Mapping[str, Any],
        software_id: int,
        update_by: str,
        now: datetime,
        cache: SoftwareImportCategoryCache,
    ) -> tuple[dict[str, Any] | None, str | None]:
        payload: dict[str, Any] = {'softwareId': software_id, 'updateBy': update_by, 'updateTime': now}

        has_category_input = any(cls._import_cell_str(row.get(k)) for k in ('categoryId', 'categoryCode', 'categoryName'))
        if has_category_input:
            category_id = cls._resolve_import_category_id(row, cache)
            if category_id is None:
                return None, '分类不存在或为空（请填写正确的分类ID/分类编码/分类名称）'
            payload['categoryId'] = category_id

        for key in (
            'softwareName',
            'shortDesc',
            'iconUrl',
            'officialUrl',
            'repoUrl',
            'author',
            'team',
            'license',
            'remark',
        ):
            cls._maybe_set_text(payload, row, key)
        cls._maybe_set_text(payload, row, 'tags', normalize_tags=True)

        open_source = cls._parse_open_source(row.get('openSource'), default=None)
        if open_source is not None:
            payload['openSource'] = open_source

        publish_status = cls._parse_publish_status(row.get('publishStatus'), default=None)
        if publish_status is not None:
            payload['publishStatus'] = publish_status

        status = cls._parse_status(row.get('status'), default=None)
        if status is not None:
            payload['status'] = status

        software_sort = cls._import_cell_int(row.get('softwareSort'))
        if software_sort is not None:
            payload['softwareSort'] = software_sort

        return payload, None

    @classmethod
    def _build_import_insert_model(
        cls,
        *,
        row: Mapping[str, Any],
        update_by: str,
        now: datetime,
        cache: SoftwareImportCategoryCache,
    ) -> tuple[ToolSoftwareModel | None, str | None]:
        category_id = cls._resolve_import_category_id(row, cache)
        if category_id is None:
            return None, '分类不存在或为空（请填写正确的分类ID/分类编码/分类名称）'

        name = cls._import_cell_str(row.get('softwareName'))
        if not name:
            return None, '软件名称不能为空'

        payload: dict[str, Any] = {
            'categoryId': category_id,
            'softwareName': name,
            'softwareSort': cls._import_cell_int(row.get('softwareSort')) or 0,
            'openSource': cls._parse_open_source(row.get('openSource'), default='0') or '0',
            'publishStatus': cls._parse_publish_status(row.get('publishStatus'), default='0') or '0',
            'status': cls._parse_status(row.get('status'), default='0') or '0',
            'createBy': update_by,
            'createTime': now,
            'updateBy': update_by,
            'updateTime': now,
        }
        for key in (
            'shortDesc',
            'iconUrl',
            'officialUrl',
            'repoUrl',
            'author',
            'team',
            'license',
            'remark',
        ):
            value = cls._import_cell_str(row.get(key))
            if value:
                payload[key] = value
        tags = cls._import_cell_str(row.get('tags')).replace('，', ',')
        if tags:
            payload['tags'] = tags

        model = ToolSoftwareModel(**payload)
        model.validate_fields()
        return model, None

    @staticmethod
    def _assert_import_df_valid(df: pd.DataFrame) -> None:
        if df.empty:
            return
        if 'softwareName' not in df.columns:
            raise ServiceException(message='导入文件缺少“软件名称”列，请使用模板下载后填写')
        if not any(c in df.columns for c in ('categoryId', 'categoryCode', 'categoryName')):
            raise ServiceException(message='导入文件缺少“分类”列（分类ID/分类编码/分类名称），请使用模板下载后填写')

    @staticmethod
    def _format_import_result_message(*, inserted: int, updated: int, skipped: int, errors: list[str]) -> str:
        summary = f'导入完成：新增 {inserted} 条，更新 {updated} 条，跳过 {skipped} 条，失败 {len(errors)} 条。'
        if not errors:
            return summary

        max_lines = 100
        detail = '\n'.join(errors[:max_lines])
        if len(errors) > max_lines:
            detail = f'{detail}\n……（共 {len(errors)} 条失败，仅展示前 {max_lines} 条）'
        return f'{summary}\n\n失败明细：\n{detail}'

    @classmethod
    async def batch_import_software_services(
        cls,
        query_db: AsyncSession,
        file: UploadFile,
        update_support: bool,
        update_by: str,
    ) -> CrudResponseModel:
        """
        批量导入软件基础信息（Excel）

        规则：
        - 若填写“软件ID”，则按软件ID更新（需 updateSupport=true）
        - 未填写“软件ID”，按新增处理
        - 空单元格默认不更新（更新场景）
        """
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        await file.close()
        df.rename(columns=cls._software_import_header_map(), inplace=True)

        if df.empty:
            return CrudResponseModel(is_success=True, message='导入文件无数据')

        cls._assert_import_df_valid(df)
        cache = await cls._build_import_category_cache(query_db)
        existing_ids = await cls._get_existing_ids_for_import(query_db, df)

        try:
            errors: list[str] = []
            inserted = 0
            updated = 0
            skipped = 0
            now = datetime.now()

            for i, row in df.iterrows():
                line_no = int(i) + 2  # 1=表头
                if cls._should_skip_import_row(row):
                    skipped += 1
                    continue

                software_id = cls._import_cell_int(row.get('softwareId'))
                if software_id:
                    if software_id not in existing_ids:
                        errors.append(f'{line_no}. 软件ID={software_id} 不存在，无法更新（请留空软件ID按新增导入）')
                        continue
                    if not update_support:
                        errors.append(f'{line_no}. 软件ID={software_id} 已存在（未勾选“更新已存在数据”）')
                        continue

                    payload, err = cls._build_import_update_payload(
                        row=row,
                        software_id=software_id,
                        update_by=update_by,
                        now=now,
                        cache=cache,
                    )
                    if err or not payload:
                        errors.append(f'{line_no}. {err or "更新数据不合法"}')
                        continue

                    edit_software = ToolSoftwareModel(**payload).model_dump(
                        exclude_unset=True, exclude={'downloads', 'resources', 'category_name'}
                    )
                    await ToolSoftwareDao.edit_software_dao(query_db, edit_software)
                    updated += 1
                    continue

                model, err = cls._build_import_insert_model(row=row, update_by=update_by, now=now, cache=cache)
                if err or not model:
                    errors.append(f'{line_no}. {err or "新增数据不合法"}')
                    continue

                await ToolSoftwareDao.add_software_dao(query_db, model)
                inserted += 1

            await query_db.commit()
            message = cls._format_import_result_message(
                inserted=inserted,
                updated=updated,
                skipped=skipped,
                errors=errors,
            )
            return CrudResponseModel(is_success=True, message=message)
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def software_detail_services(cls, query_db: AsyncSession, software_id: int) -> ToolSoftwareModel:
        """
        获取软件详细信息service（含下载配置/资源URL）
        """
        software = await ToolSoftwareDao.get_software_detail_by_id(query_db, software_id)
        if not software:
            return ToolSoftwareModel()
        software_dict = CamelCaseUtil.transform_result(software)
        category_name = None
        if software.category_id:
            category = await ToolSoftwareCategoryDao.get_category_detail_by_id(query_db, software.category_id)
            if category and category.del_flag == '0':
                category_name = category.category_name
        downloads_do = await ToolSoftwareDownloadDao.get_download_list_by_software_id(query_db, software_id)
        downloads: list[ToolSoftwareDownloadModel] = [
            ToolSoftwareDownloadModel(**CamelCaseUtil.transform_result(item)) for item in downloads_do
        ]

        resources_do = await ToolSoftwareResourceDao.get_resource_list_by_software_id(query_db, software_id)
        resources: list[ToolSoftwareResourceModel] = [
            ToolSoftwareResourceModel(**CamelCaseUtil.transform_result(item)) for item in resources_do
        ]

        return ToolSoftwareModel(
            **{
                **software_dict,
                'categoryName': category_name,
                'downloads': downloads,
                'resources': resources,
            }
        )

    @classmethod
    async def add_software_services(cls, query_db: AsyncSession, page_object: ToolSoftwareModel) -> CrudResponseModel:
        """
        新增软件信息service
        """
        if page_object.category_id is None:
            raise ServiceException(message='分类不能为空')
        category = await ToolSoftwareCategoryDao.get_category_detail_by_id(query_db, page_object.category_id)
        if not category or category.del_flag != '0':
            raise ServiceException(message='分类不存在')
        try:
            db_software = await ToolSoftwareDao.add_software_dao(query_db, page_object)
            await ToolSoftwareDownloadDao.add_downloads_dao(
                query_db, db_software.software_id, page_object.downloads or []
            )
            await ToolSoftwareResourceDao.add_resources_dao(
                query_db, db_software.software_id, page_object.resources or []
            )
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def edit_software_services(cls, query_db: AsyncSession, page_object: ToolSoftwareModel) -> CrudResponseModel:
        """
        编辑软件信息service（下载配置/资源URL支持全量覆盖）
        """
        if page_object.software_id is None:
            raise ServiceException(message='软件ID不能为空')
        current = await ToolSoftwareDao.get_software_detail_by_id(query_db, page_object.software_id)
        if not current:
            raise ServiceException(message='软件不存在')
        if page_object.category_id is None:
            raise ServiceException(message='分类不能为空')
        category = await ToolSoftwareCategoryDao.get_category_detail_by_id(query_db, page_object.category_id)
        if not category or category.del_flag != '0':
            raise ServiceException(message='分类不存在')
        fields_set = getattr(page_object, 'model_fields_set', set())
        replace_downloads = 'downloads' in fields_set
        replace_resources = 'resources' in fields_set
        edit_software = page_object.model_dump(exclude_unset=True, exclude={'downloads', 'resources', 'category_name'})
        try:
            await ToolSoftwareDao.edit_software_dao(query_db, edit_software)
            if replace_downloads:
                await ToolSoftwareDownloadDao.delete_downloads_by_software_id(query_db, page_object.software_id)
                await ToolSoftwareDownloadDao.add_downloads_dao(
                    query_db, page_object.software_id, page_object.downloads or []
                )
            if replace_resources:
                await ToolSoftwareResourceDao.delete_resources_by_software_id(query_db, page_object.software_id)
                await ToolSoftwareResourceDao.add_resources_dao(
                    query_db, page_object.software_id, page_object.resources or []
                )
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='更新成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def delete_software_services(
        cls, query_db: AsyncSession, page_object: DeleteToolSoftwareModel, update_by: str
    ) -> CrudResponseModel:
        """
        删除软件信息service（软删）
        """
        if not page_object.software_ids:
            raise ServiceException(message='传入软件id为空')
        software_id_list = page_object.software_ids.split(',')
        try:
            for software_id_str in software_id_list:
                software_id = int(software_id_str)
                current = await ToolSoftwareDao.get_software_detail_by_id(query_db, software_id)
                if not current:
                    raise ServiceException(message='软件不存在')
                await ToolSoftwareDao.delete_software_dao(query_db, software_id, update_by, datetime.now())
                await ToolSoftwareDownloadDao.delete_downloads_by_software_id(query_db, software_id)
                await ToolSoftwareResourceDao.delete_resources_by_software_id(query_db, software_id)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='删除成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def change_publish_status_services(
        cls, query_db: AsyncSession, page_object: ToolSoftwarePublishStatusModel, update_by: str
    ) -> CrudResponseModel:
        """
        修改软件发布状态service
        """
        current = await ToolSoftwareDao.get_software_detail_by_id(query_db, page_object.software_id)
        if not current:
            raise ServiceException(message='软件不存在')
        edit_software = ToolSoftwareModel(
            softwareId=page_object.software_id,
            publishStatus=page_object.publish_status,
            updateBy=update_by,
            updateTime=datetime.now(),
        ).model_dump(exclude_unset=True, exclude={'downloads', 'resources', 'category_name'})
        try:
            await ToolSoftwareDao.edit_software_dao(query_db, edit_software)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='更新成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def batch_change_publish_status_services(
        cls, query_db: AsyncSession, page_object: ToolSoftwareBatchPublishStatusModel, update_by: str
    ) -> CrudResponseModel:
        """
        批量修改软件发布状态service
        """
        software_ids = [int(x) for x in (page_object.software_ids or []) if str(x).strip()]
        software_ids = sorted(set(software_ids))
        if not software_ids:
            raise ServiceException(message='软件ID不能为空')

        existing_ids = await ToolSoftwareDao.get_existing_software_ids(query_db, software_ids)
        missing = sorted(set(software_ids) - set(existing_ids))
        if missing:
            raise ServiceException(message=f'以下软件不存在或已删除：{",".join(map(str, missing))}')

        now = datetime.now()
        payloads = [
            ToolSoftwareModel(
                softwareId=software_id,
                publishStatus=page_object.publish_status,
                updateBy=update_by,
                updateTime=now,
            ).model_dump(exclude_unset=True, exclude={'downloads', 'resources', 'category_name'})
            for software_id in software_ids
        ]
        try:
            await ToolSoftwareDao.batch_edit_software_dao(query_db, payloads)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='批量更新成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def batch_move_category_services(
        cls, query_db: AsyncSession, page_object: ToolSoftwareBatchMoveCategoryModel, update_by: str
    ) -> CrudResponseModel:
        """
        批量移动软件分类 service
        """
        software_ids = [int(x) for x in (page_object.software_ids or []) if str(x).strip()]
        software_ids = sorted(set(software_ids))
        if not software_ids:
            raise ServiceException(message='软件ID不能为空')

        category_id = int(page_object.category_id)
        category = await ToolSoftwareCategoryDao.get_category_detail_by_id(query_db, category_id)
        if not category or category.del_flag != '0':
            raise ServiceException(message='分类不存在')
        if getattr(category, 'status', '0') != '0':
            raise ServiceException(message='分类已停用')

        existing_ids = await ToolSoftwareDao.get_existing_software_ids(query_db, software_ids)
        missing = sorted(set(software_ids) - set(existing_ids))
        if missing:
            raise ServiceException(message=f'以下软件不存在或已删除：{",".join(map(str, missing))}')

        now = datetime.now()
        payloads = [
            ToolSoftwareModel(
                softwareId=software_id,
                categoryId=category_id,
                updateBy=update_by,
                updateTime=now,
            ).model_dump(exclude_unset=True, exclude={'downloads', 'resources', 'category_name'})
            for software_id in software_ids
        ]
        try:
            await ToolSoftwareDao.batch_edit_software_dao(query_db, payloads)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='批量移动分类成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def batch_manage_tags_services(
        cls, query_db: AsyncSession, page_object: ToolSoftwareBatchTagsModel, update_by: str
    ) -> CrudResponseModel:
        """
        批量标签治理 service

        action:
        - append: 追加标签（去重）
        - remove: 移除标签（不存在则忽略）
        - replace: 覆盖标签（允许为空表示清空）
        """
        software_ids = [int(x) for x in (page_object.software_ids or []) if str(x).strip()]
        software_ids = sorted(set(software_ids))
        if not software_ids:
            raise ServiceException(message='软件ID不能为空')

        action = (page_object.action or '').strip()
        raw_tags = page_object.tags or ''
        input_tags = cls._split_tags(raw_tags)

        if action in {'append', 'remove'} and not input_tags:
            raise ServiceException(message='标签不能为空')
        if action not in {'append', 'remove', 'replace'}:
            raise ServiceException(message='action 参数不合法')

        existing_ids = await ToolSoftwareDao.get_existing_software_ids(query_db, software_ids)
        missing = sorted(set(software_ids) - set(existing_ids))
        if missing:
            raise ServiceException(message=f'以下软件不存在或已删除：{",".join(map(str, missing))}')

        tags_map = await ToolSoftwareDao.get_software_tags_map_by_ids(query_db, software_ids)
        input_set = set(input_tags)
        now = datetime.now()

        payloads: list[dict[str, Any]] = []
        changed = 0
        unchanged = 0

        for software_id in software_ids:
            current_tags = tags_map.get(software_id)
            current_list = cls._split_tags(current_tags or '')
            current_norm = ','.join(current_list) if current_list else None

            if action == 'replace':
                new_list = input_tags
            elif action == 'append':
                seen = set(current_list)
                new_list = current_list + [t for t in input_tags if t not in seen]
            else:  # remove
                new_list = [t for t in current_list if t not in input_set]

            new_norm = ','.join(new_list) if new_list else None

            if new_norm and len(new_norm) > MAX_SOFTWARE_TAGS_LENGTH:
                raise ServiceException(
                    message=(
                        f'软件ID={software_id} 标签过长（{len(new_norm)} > {MAX_SOFTWARE_TAGS_LENGTH}）'
                    )
                )

            if new_norm == current_norm:
                unchanged += 1
                continue

            changed += 1
            payloads.append(
                ToolSoftwareModel(
                    softwareId=software_id,
                    tags=new_norm,
                    updateBy=update_by,
                    updateTime=now,
                ).model_dump(exclude_unset=True, exclude={'downloads', 'resources', 'category_name'})
            )

        if not payloads:
            return CrudResponseModel(is_success=True, message=f'无需更新（保持不变 {unchanged} 条）')

        try:
            await ToolSoftwareDao.batch_edit_software_dao(query_db, payloads)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message=f'批量标签治理成功（更新 {changed} 条，保持不变 {unchanged} 条）')
        except Exception as exc:
            await query_db.rollback()
            raise exc
