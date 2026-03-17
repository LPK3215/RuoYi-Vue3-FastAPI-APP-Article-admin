from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from sqlalchemy import and_, func, select

from module_software.entity.do.software_do import ToolSoftware, ToolSoftwareDownload

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

FacetMode = Literal['tool', 'portal']


class SoftwareFacetsDao:
    """
    软件筛选项聚合 DAO

    - tool: 后台管理端（仅排除软删）
    - portal: 用户端（仅上架/正常/未删除）
    """

    @classmethod
    def _software_base_conditions(cls, mode: FacetMode) -> list[Any]:
        conditions: list[Any] = [ToolSoftware.del_flag == '0']
        if mode == 'portal':
            conditions.extend([ToolSoftware.status == '0', ToolSoftware.publish_status == '1'])
        return conditions

    @classmethod
    async def get_tag_strings(cls, db: AsyncSession, mode: FacetMode) -> list[str]:
        query = (
            select(ToolSoftware.tags)
            .select_from(ToolSoftware)
            .where(*cls._software_base_conditions(mode), ToolSoftware.tags.is_not(None))
        )
        rows = (await db.execute(query)).scalars().all()
        return [r for r in (rows or []) if isinstance(r, str) and r.strip()]

    @classmethod
    async def get_group_counts(
        cls, db: AsyncSession, mode: FacetMode, field_name: Literal['license', 'author', 'team'], limit: int
    ) -> list[dict[str, Any]]:
        field = getattr(ToolSoftware, field_name)
        value_expr = func.trim(field).label('value')
        query = (
            select(value_expr, func.count(ToolSoftware.software_id).label('count'))
            .select_from(ToolSoftware)
            .where(
                *cls._software_base_conditions(mode),
                field.is_not(None),
                func.trim(field) != '',
            )
            .group_by(value_expr)
            .order_by(func.count(ToolSoftware.software_id).desc(), value_expr.asc())
            .limit(limit)
        )
        rows = (await db.execute(query)).mappings().all()
        return [dict(r) for r in (rows or [])]

    @classmethod
    async def get_platform_counts(cls, db: AsyncSession, mode: FacetMode, limit: int) -> list[dict[str, Any]]:
        conditions = cls._software_base_conditions(mode)
        query = (
            select(
                func.trim(ToolSoftwareDownload.platform).label('value'),
                func.count(func.distinct(ToolSoftwareDownload.software_id)).label('count'),
            )
            .select_from(ToolSoftwareDownload)
            .join(
                ToolSoftware,
                and_(
                    ToolSoftwareDownload.software_id == ToolSoftware.software_id,
                    *conditions,
                ),
                isouter=False,
            )
            .where(ToolSoftwareDownload.platform.is_not(None), func.trim(ToolSoftwareDownload.platform) != '')
            .group_by(func.trim(ToolSoftwareDownload.platform))
            .order_by(func.count(func.distinct(ToolSoftwareDownload.software_id)).desc(), func.trim(ToolSoftwareDownload.platform).asc())
            .limit(limit)
        )
        rows = (await db.execute(query)).mappings().all()
        return [dict(r) for r in (rows or [])]

