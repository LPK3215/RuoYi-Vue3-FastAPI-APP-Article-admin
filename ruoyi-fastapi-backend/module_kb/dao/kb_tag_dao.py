from typing import Any

from sqlalchemy import and_, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_kb.entity.do.kb_article_do import ToolKbArticle, ToolKbArticleTag, ToolKbTag
from module_kb.entity.vo.kb_tag_vo import ToolKbTagModel, ToolKbTagPageQueryModel
from utils.page_util import PageUtil


class ToolKbTagDao:
    """
    教程标签模块数据库操作层（管理端）
    """

    @classmethod
    async def get_tag_detail_by_id(cls, db: AsyncSession, tag_id: int) -> ToolKbTag | None:
        tag = (
            (await db.execute(select(ToolKbTag).where(ToolKbTag.tag_id == tag_id, ToolKbTag.del_flag == '0')))
            .scalars()
            .first()
        )
        return tag

    @classmethod
    async def get_tag_detail_by_info(cls, db: AsyncSession, tag: ToolKbTagModel) -> ToolKbTag | None:
        tag_info = (
            (
                await db.execute(
                    select(ToolKbTag).where(
                        ToolKbTag.del_flag == '0',
                        ToolKbTag.tag_name == tag.tag_name if tag.tag_name else True,
                        ToolKbTag.tag_code == tag.tag_code if tag.tag_code else True,
                    )
                )
            )
            .scalars()
            .first()
        )
        return tag_info

    @classmethod
    async def get_tag_list(
        cls, db: AsyncSession, query_object: ToolKbTagPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        query = (
            select(ToolKbTag)
            .where(
                ToolKbTag.del_flag == '0',
                ToolKbTag.tag_name.like(f'%{query_object.tag_name}%') if query_object.tag_name else True,
                ToolKbTag.tag_code.like(f'%{query_object.tag_code}%') if query_object.tag_code else True,
                ToolKbTag.status == query_object.status if query_object.status else True,
            )
            .order_by(ToolKbTag.tag_sort, ToolKbTag.tag_id)
            .distinct()
        )
        tag_list: PageModel | list[dict[str, Any]] = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )
        return tag_list

    @classmethod
    async def get_tag_list_by_ids(cls, db: AsyncSession, tag_ids: list[int]) -> list[ToolKbTag]:
        if not tag_ids:
            return []
        rows = (
            (
                await db.execute(
                    select(ToolKbTag)
                    .where(ToolKbTag.del_flag == '0', ToolKbTag.tag_id.in_(tag_ids))
                    .order_by(ToolKbTag.tag_sort, ToolKbTag.tag_id)
                )
            )
            .scalars()
            .all()
        )
        return list(rows or [])

    @classmethod
    async def get_tag_list_by_names(cls, db: AsyncSession, tag_names: list[str]) -> list[ToolKbTag]:
        if not tag_names:
            return []
        rows = (
            (
                await db.execute(
                    select(ToolKbTag)
                    .where(ToolKbTag.del_flag == '0', ToolKbTag.tag_name.in_(tag_names))
                    .order_by(ToolKbTag.tag_sort, ToolKbTag.tag_id)
                )
            )
            .scalars()
            .all()
        )
        return list(rows or [])

    @classmethod
    async def add_tag_dao(cls, db: AsyncSession, tag: ToolKbTagModel) -> ToolKbTag:
        db_tag = ToolKbTag(**tag.model_dump())
        db.add(db_tag)
        await db.flush()
        return db_tag

    @classmethod
    async def add_tag_list_dao(cls, db: AsyncSession, tags: list[ToolKbTag]) -> None:
        if not tags:
            return
        db.add_all(tags)
        await db.flush()

    @classmethod
    async def edit_tag_dao(cls, db: AsyncSession, tag: dict) -> None:
        await db.execute(update(ToolKbTag), [tag])

    @classmethod
    async def delete_tag_dao(cls, db: AsyncSession, tag_id: int, update_by: str, update_time: Any) -> None:
        await db.execute(
            update(ToolKbTag).where(ToolKbTag.tag_id == tag_id).values(
                del_flag='2',
                update_by=update_by,
                update_time=update_time,
            )
        )

    @classmethod
    async def count_articles_by_tag_id(cls, db: AsyncSession, tag_id: int) -> int:
        count = (
            await db.execute(
                select(func.count('*'))
                .select_from(ToolKbArticleTag)
                .join(
                    ToolKbArticle,
                    and_(
                        ToolKbArticle.article_id == ToolKbArticleTag.article_id,
                        ToolKbArticle.del_flag == '0',
                    ),
                )
                .where(ToolKbArticleTag.tag_id == tag_id)
            )
        ).scalar()
        return int(count or 0)

