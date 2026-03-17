from typing import Any

from sqlalchemy import and_, exists, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from config.env import DataBaseConfig
from module_software.entity.do.software_do import (
    ToolSoftware,
    ToolSoftwareCategory,
    ToolSoftwareDownload,
    ToolSoftwareResource,
)
from module_software.entity.vo.portal_software_vo import PortalSoftwarePageQueryModel
from utils.common_util import CamelCaseUtil
from utils.page_util import PageUtil


class PortalSoftwareDao:
    """
    用户端：软件库数据库操作层（仅查询上架数据）
    """

    @classmethod
    async def get_category_list(cls, db: AsyncSession) -> list[dict[str, Any]]:
        """
        获取用户端软件分类列表（仅正常且未删除），并附带已上架软件数量

        仅返回“有上架软件”的分类，避免用户端出现空分类。
        """
        query = (
            select(
                ToolSoftwareCategory.category_id.label('category_id'),
                ToolSoftwareCategory.category_code.label('category_code'),
                ToolSoftwareCategory.category_name.label('category_name'),
                func.count(ToolSoftware.software_id).label('software_count'),
            )
            .select_from(ToolSoftwareCategory)
            .join(
                ToolSoftware,
                and_(
                    ToolSoftware.category_id == ToolSoftwareCategory.category_id,
                    ToolSoftware.del_flag == '0',
                    ToolSoftware.status == '0',
                    ToolSoftware.publish_status == '1',
                ),
                isouter=True,
            )
            .where(ToolSoftwareCategory.del_flag == '0', ToolSoftwareCategory.status == '0')
            .group_by(
                ToolSoftwareCategory.category_id,
                ToolSoftwareCategory.category_code,
                ToolSoftwareCategory.category_name,
                ToolSoftwareCategory.category_sort,
            )
            .having(func.count(ToolSoftware.software_id) > 0)
            .order_by(ToolSoftwareCategory.category_sort, ToolSoftwareCategory.category_id)
        )
        rows = (await db.execute(query)).mappings().all()
        # RowMapping 需要先转为 dict，才能被 CamelCaseUtil 正确转换
        return CamelCaseUtil.transform_result([dict(row) for row in (rows or [])])

    @classmethod
    async def get_software_list(
        cls, db: AsyncSession, query_object: PortalSoftwarePageQueryModel, is_page: bool = False
    ) -> PageModel | list[list[dict[str, Any]]]:
        """
        获取用户端软件列表（仅上架/正常/未删除），并包含分类名称
        """
        keyword = (query_object.keyword or '').strip()
        tag = (query_object.tag or '').strip()
        platform = (query_object.platform or '').strip()
        query = (
            select(ToolSoftware, ToolSoftwareCategory)
            .select_from(ToolSoftware)
            .where(
                ToolSoftware.del_flag == '0',
                ToolSoftware.status == '0',
                ToolSoftware.publish_status == '1',
                ToolSoftware.category_id == query_object.category_id if query_object.category_id else True,
                ToolSoftware.open_source == query_object.open_source if query_object.open_source is not None else True,
                ToolSoftware.license.like(f'%{query_object.license}%') if query_object.license else True,
                or_(
                    ToolSoftware.software_name.like(f'%{keyword}%'),
                    ToolSoftware.short_desc.like(f'%{keyword}%'),
                    ToolSoftware.author.like(f'%{keyword}%'),
                    ToolSoftware.team.like(f'%{keyword}%'),
                    ToolSoftware.license.like(f'%{keyword}%'),
                    ToolSoftware.tags.like(f'%{keyword}%'),
                )
                if keyword
                else True,
                func.find_in_set(tag, ToolSoftware.tags) > 0
                if (tag and DataBaseConfig.db_type == 'mysql')
                else (ToolSoftware.tags.like(f'%{tag}%') if tag else True),
                exists(
                    select(1)
                    .select_from(ToolSoftwareDownload)
                    .where(ToolSoftwareDownload.software_id == ToolSoftware.software_id, ToolSoftwareDownload.platform == platform)
                )
                if platform
                else True,
            )
            .join(
                ToolSoftwareCategory,
                and_(
                    ToolSoftware.category_id == ToolSoftwareCategory.category_id,
                    ToolSoftwareCategory.del_flag == '0',
                    ToolSoftwareCategory.status == '0',
                ),
                isouter=True,
            )
            .order_by(ToolSoftware.software_sort, ToolSoftware.software_id)
            .distinct()
        )
        software_list: PageModel | list[list[dict[str, Any]]] = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )
        return software_list

    @classmethod
    async def get_software_detail_by_id(cls, db: AsyncSession, software_id: int) -> list[dict[str, Any]] | None:
        """
        获取用户端软件详情（仅上架/正常/未删除），并包含分类信息
        """
        row = (
            await db.execute(
                select(ToolSoftware, ToolSoftwareCategory)
                .select_from(ToolSoftware)
                .where(
                    ToolSoftware.software_id == software_id,
                    ToolSoftware.del_flag == '0',
                    ToolSoftware.status == '0',
                    ToolSoftware.publish_status == '1',
                )
                .join(
                    ToolSoftwareCategory,
                    and_(
                        ToolSoftware.category_id == ToolSoftwareCategory.category_id,
                        ToolSoftwareCategory.del_flag == '0',
                        ToolSoftwareCategory.status == '0',
                    ),
                    isouter=True,
                )
            )
        ).first()
        if not row:
            return None
        return CamelCaseUtil.transform_result(row)


class PortalSoftwareDownloadDao:
    """
    用户端：软件下载配置数据库操作层
    """

    @classmethod
    async def get_download_list_by_software_id(cls, db: AsyncSession, software_id: int) -> list[dict[str, Any]]:
        downloads = (
            (
                await db.execute(
                    select(ToolSoftwareDownload)
                    .where(ToolSoftwareDownload.software_id == software_id)
                    .order_by(ToolSoftwareDownload.sort, ToolSoftwareDownload.download_id)
                    .distinct()
                )
            )
            .scalars()
            .all()
        )
        return CamelCaseUtil.transform_result(list(downloads or []))


class PortalSoftwareResourceDao:
    """
    用户端：软件资源数据库操作层（当前仅存 URL）
    """

    @classmethod
    async def get_resource_list_by_software_id(cls, db: AsyncSession, software_id: int) -> list[dict[str, Any]]:
        resources = (
            (
                await db.execute(
                    select(ToolSoftwareResource)
                    .where(ToolSoftwareResource.software_id == software_id)
                    .order_by(ToolSoftwareResource.sort, ToolSoftwareResource.resource_id)
                    .distinct()
                )
            )
            .scalars()
            .all()
        )
        return CamelCaseUtil.transform_result(list(resources or []))
