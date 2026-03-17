from typing import Any

from sqlalchemy import and_, asc, delete, desc, exists, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from config.env import DataBaseConfig
from module_software.entity.do.software_do import (
    ToolSoftware,
    ToolSoftwareCategory,
    ToolSoftwareDownload,
    ToolSoftwareResource,
)
from module_software.entity.vo.software_item_vo import (
    ToolSoftwareDownloadModel,
    ToolSoftwareModel,
    ToolSoftwarePageQueryModel,
    ToolSoftwareResourceModel,
)
from utils.common_util import SnakeCaseUtil
from utils.page_util import PageUtil


class ToolSoftwareDao:
    """
    软件信息模块数据库操作层
    """

    @classmethod
    async def get_software_detail_by_id(cls, db: AsyncSession, software_id: int) -> ToolSoftware | None:
        """
        根据软件ID获取软件详细信息
        """
        software = (
            (
                await db.execute(
                    select(ToolSoftware).where(ToolSoftware.software_id == software_id, ToolSoftware.del_flag == '0')
                )
            )
            .scalars()
            .first()
        )
        return software

    @classmethod
    async def get_software_list(
        cls, db: AsyncSession, query_object: ToolSoftwarePageQueryModel, is_page: bool = False
    ) -> PageModel | list[list[dict[str, Any]]]:
        """
        根据查询参数获取软件列表信息（包含分类信息）
        """
        keyword = (query_object.keyword or '').strip() or (query_object.software_name or '').strip()
        tag = (query_object.tag or '').strip()
        platform = (query_object.platform or '').strip()
        has_icon = (query_object.has_icon or '').strip()
        has_license = (query_object.has_license or '').strip()
        has_official_url = (query_object.has_official_url or '').strip()
        has_short_desc = (query_object.has_short_desc or '').strip()
        has_tags = (query_object.has_tags or '').strip()
        has_downloads = (query_object.has_downloads or '').strip()
        has_resources = (query_object.has_resources or '').strip()

        def is_blank(col: Any) -> Any:
            return or_(col.is_(None), func.trim(col) == '')

        download_exists = exists(
            select(1)
            .select_from(ToolSoftwareDownload)
            .where(ToolSoftwareDownload.software_id == ToolSoftware.software_id)
        )
        resource_exists = exists(
            select(1)
            .select_from(ToolSoftwareResource)
            .where(ToolSoftwareResource.software_id == ToolSoftware.software_id)
        )

        order_by: list[Any] = []
        if query_object.order_by_column:
            field_name = SnakeCaseUtil.camel_to_snake(query_object.order_by_column)
            col = getattr(ToolSoftware, field_name, None)
            if col is not None:
                if query_object.is_asc == 'descending':
                    order_by.append(desc(col))
                    order_by.append(desc(ToolSoftware.software_id))
                else:
                    order_by.append(asc(col))
                    order_by.append(asc(ToolSoftware.software_id))

        if not order_by:
            order_by = [ToolSoftware.software_sort, ToolSoftware.software_id]
        query = (
            select(ToolSoftware, ToolSoftwareCategory)
            .select_from(ToolSoftware)
            .where(
                ToolSoftware.del_flag == '0',
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
                ToolSoftware.category_id == query_object.category_id if query_object.category_id else True,
                ToolSoftware.publish_status == query_object.publish_status if query_object.publish_status else True,
                ToolSoftware.status == query_object.status if query_object.status else True,
                ToolSoftware.open_source == query_object.open_source if query_object.open_source is not None else True,
                ToolSoftware.license.like(f'%{query_object.license}%') if query_object.license else True,
                ToolSoftware.official_url.like(f'%{query_object.official_url}%') if query_object.official_url else True,
                ToolSoftware.repo_url.like(f'%{query_object.repo_url}%') if query_object.repo_url else True,
                or_(
                    ToolSoftware.author.like(f'%{query_object.author}%'),
                    ToolSoftware.team.like(f'%{query_object.author}%'),
                )
                if query_object.author
                else True,
                ToolSoftware.team.like(f'%{query_object.team}%') if query_object.team else True,
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
                (~is_blank(ToolSoftware.icon_url)) if has_icon == '1' else (is_blank(ToolSoftware.icon_url) if has_icon == '0' else True),
                (~is_blank(ToolSoftware.license)) if has_license == '1' else (is_blank(ToolSoftware.license) if has_license == '0' else True),
                (~is_blank(ToolSoftware.official_url))
                if has_official_url == '1'
                else (is_blank(ToolSoftware.official_url) if has_official_url == '0' else True),
                (~is_blank(ToolSoftware.short_desc))
                if has_short_desc == '1'
                else (is_blank(ToolSoftware.short_desc) if has_short_desc == '0' else True),
                (~is_blank(ToolSoftware.tags)) if has_tags == '1' else (is_blank(ToolSoftware.tags) if has_tags == '0' else True),
                (download_exists) if has_downloads == '1' else ((~download_exists) if has_downloads == '0' else True),
                (resource_exists) if has_resources == '1' else ((~resource_exists) if has_resources == '0' else True),
            )
            .join(
                ToolSoftwareCategory,
                and_(
                    ToolSoftware.category_id == ToolSoftwareCategory.category_id,
                    ToolSoftwareCategory.del_flag == '0',
                ),
                isouter=True,
            )
            .order_by(*order_by)
            .distinct()
        )
        software_list: PageModel | list[list[dict[str, Any]]] = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )
        return software_list

    @classmethod
    async def add_software_dao(cls, db: AsyncSession, software: ToolSoftwareModel) -> ToolSoftware:
        """
        新增软件数据库操作
        """
        db_software = ToolSoftware(**software.model_dump(exclude={'downloads', 'resources', 'category_name'}, exclude_none=True))
        db.add(db_software)
        await db.flush()
        return db_software

    @classmethod
    async def edit_software_dao(cls, db: AsyncSession, software: dict) -> None:
        """
        编辑软件数据库操作
        """
        await db.execute(update(ToolSoftware), [software])

    @classmethod
    async def batch_edit_software_dao(cls, db: AsyncSession, softwares: list[dict]) -> None:
        """
        批量编辑软件数据库操作
        """
        if not softwares:
            return
        await db.execute(update(ToolSoftware), softwares)

    @classmethod
    async def get_existing_software_ids(cls, db: AsyncSession, software_ids: list[int]) -> list[int]:
        """
        查询存在的软件ID列表（排除软删）
        """
        if not software_ids:
            return []
        rows = (
            (
                await db.execute(
                    select(ToolSoftware.software_id).where(
                        ToolSoftware.software_id.in_(software_ids), ToolSoftware.del_flag == '0'
                    )
                )
            )
            .scalars()
            .all()
        )
        return list(rows or [])

    @classmethod
    async def get_software_tags_map_by_ids(cls, db: AsyncSession, software_ids: list[int]) -> dict[int, str | None]:
        """
        批量查询软件 tags 字段（排除软删）
        """
        if not software_ids:
            return {}
        rows = (
            (
                await db.execute(
                    select(ToolSoftware.software_id, ToolSoftware.tags).where(
                        ToolSoftware.software_id.in_(software_ids), ToolSoftware.del_flag == '0'
                    )
                )
            )
            .all()
        )
        return {int(software_id): tags for software_id, tags in (rows or [])}

    @classmethod
    async def delete_software_dao(cls, db: AsyncSession, software_id: int, update_by: str, update_time: Any) -> None:
        """
        删除软件数据库操作（软删）
        """
        await db.execute(
            update(ToolSoftware)
            .where(ToolSoftware.software_id == software_id)
            .values(del_flag='2', update_by=update_by, update_time=update_time)
        )


class ToolSoftwareDownloadDao:
    """
    软件多平台下载配置数据库操作层
    """

    @classmethod
    async def get_download_list_by_software_id(cls, db: AsyncSession, software_id: int) -> list[ToolSoftwareDownload]:
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
        return list(downloads or [])

    @classmethod
    async def delete_downloads_by_software_id(cls, db: AsyncSession, software_id: int) -> None:
        await db.execute(delete(ToolSoftwareDownload).where(ToolSoftwareDownload.software_id == software_id))

    @classmethod
    async def add_downloads_dao(
        cls, db: AsyncSession, software_id: int, downloads: list[ToolSoftwareDownloadModel]
    ) -> None:
        if not downloads:
            return
        db_downloads = [
            ToolSoftwareDownload(**{**download.model_dump(exclude={'download_id'}), 'software_id': software_id})
            for download in downloads
        ]
        db.add_all(db_downloads)
        await db.flush()


class ToolSoftwareResourceDao:
    """
    软件资源数据库操作层（当前仅存 URL）
    """

    @classmethod
    async def get_resource_list_by_software_id(cls, db: AsyncSession, software_id: int) -> list[ToolSoftwareResource]:
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
        return list(resources or [])

    @classmethod
    async def delete_resources_by_software_id(cls, db: AsyncSession, software_id: int) -> None:
        await db.execute(delete(ToolSoftwareResource).where(ToolSoftwareResource.software_id == software_id))

    @classmethod
    async def add_resources_dao(
        cls, db: AsyncSession, software_id: int, resources: list[ToolSoftwareResourceModel]
    ) -> None:
        if not resources:
            return
        db_resources = [
            ToolSoftwareResource(**{**resource.model_dump(exclude={'resource_id'}), 'software_id': software_id})
            for resource in resources
        ]
        db.add_all(db_resources)
        await db.flush()
