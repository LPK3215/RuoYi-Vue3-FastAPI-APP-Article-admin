from collections import Counter
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from exceptions.exception import ServiceException
from module_software.dao.portal_software_dao import (
    PortalSoftwareDao,
    PortalSoftwareDownloadDao,
    PortalSoftwareResourceDao,
)
from module_software.dao.software_facets_dao import SoftwareFacetsDao
from module_software.entity.vo.portal_software_vo import (
    PortalSoftwareCategoryModel,
    PortalSoftwareDetailModel,
    PortalSoftwareDownloadModel,
    PortalSoftwareListItemModel,
    PortalSoftwarePageQueryModel,
    PortalSoftwareResourceModel,
)
from module_software.entity.vo.software_facets_vo import SoftwareFacetItemModel, SoftwareFacetsModel


class PortalSoftwareService:
    """
    用户端：软件库服务层（仅查询上架数据）
    """

    @staticmethod
    def _split_tags(tags: str) -> list[str]:
        raw = (tags or '').replace('，', ',')
        parts = [p.strip() for p in raw.split(',')]
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
        获取用户端“软件筛选项”聚合数据（仅上架/正常/未删除）。

        用于用户端构建筛选 UI（标签/许可证/作者/平台等）。
        """
        safe_limit = max(1, min(int(limit or 50), 200))

        tag_strings = await SoftwareFacetsDao.get_tag_strings(query_db, mode='portal')
        tag_counter: Counter[str] = Counter()
        for s in tag_strings:
            for tag in cls._split_tags(s):
                tag_counter[tag] += 1
        tag_items = [
            SoftwareFacetItemModel(value=v, count=c)
            for v, c in sorted(tag_counter.items(), key=lambda x: (-x[1], x[0]))[:safe_limit]
        ]

        license_rows = await SoftwareFacetsDao.get_group_counts(query_db, mode='portal', field_name='license', limit=safe_limit)
        author_rows = await SoftwareFacetsDao.get_group_counts(query_db, mode='portal', field_name='author', limit=safe_limit)
        team_rows = await SoftwareFacetsDao.get_group_counts(query_db, mode='portal', field_name='team', limit=safe_limit)
        platform_rows = await SoftwareFacetsDao.get_platform_counts(query_db, mode='portal', limit=safe_limit)

        return SoftwareFacetsModel(
            tags=tag_items,
            licenses=[SoftwareFacetItemModel(**r) for r in license_rows],
            authors=[SoftwareFacetItemModel(**r) for r in author_rows],
            teams=[SoftwareFacetItemModel(**r) for r in team_rows],
            platforms=[SoftwareFacetItemModel(**r) for r in platform_rows],
        )

    @classmethod
    async def get_category_list_services(cls, query_db: AsyncSession) -> list[PortalSoftwareCategoryModel]:
        rows = await PortalSoftwareDao.get_category_list(query_db)
        if not rows:
            return []
        return [PortalSoftwareCategoryModel(**row) for row in rows]

    @classmethod
    async def get_software_list_services(
        cls, query_db: AsyncSession, query_object: PortalSoftwarePageQueryModel, is_page: bool = False
    ) -> PageModel[PortalSoftwareListItemModel] | list[dict[str, Any]]:
        query_result = await PortalSoftwareDao.get_software_list(query_db, query_object, is_page)
        if is_page:
            software_list_result = PageModel[PortalSoftwareListItemModel](
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

    @classmethod
    async def software_detail_services(cls, query_db: AsyncSession, software_id: int) -> PortalSoftwareDetailModel:
        """
        获取用户端软件详情（含下载配置）
        """
        row = await PortalSoftwareDao.get_software_detail_by_id(query_db, software_id)
        if not row:
            raise ServiceException(message='软件不存在或未上架')

        software = row[0] if isinstance(row, list) and len(row) > 0 else {}
        category = row[1] if isinstance(row, list) and len(row) > 1 else {}
        downloads = await PortalSoftwareDownloadDao.get_download_list_by_software_id(query_db, software_id)
        resources = await PortalSoftwareResourceDao.get_resource_list_by_software_id(query_db, software_id)

        download_models = [PortalSoftwareDownloadModel(**d) for d in downloads]
        resource_models = [PortalSoftwareResourceModel(**r) for r in resources]
        return PortalSoftwareDetailModel(
            **{
                **(software or {}),
                'categoryName': (category or {}).get('categoryName'),
                'downloads': download_models,
                'resources': resource_models,
            }
        )
