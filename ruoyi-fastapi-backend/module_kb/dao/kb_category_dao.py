from typing import Any

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_kb.entity.do.kb_article_do import ToolKbArticle, ToolKbCategory
from module_kb.entity.vo.kb_category_vo import ToolKbCategoryModel, ToolKbCategoryPageQueryModel
from utils.page_util import PageUtil


class ToolKbCategoryDao:
    """
    教程分类模块数据库操作层（管理端）
    """

    @classmethod
    async def get_category_detail_by_id(cls, db: AsyncSession, category_id: int) -> ToolKbCategory | None:
        category = (
            (
                await db.execute(
                    select(ToolKbCategory).where(ToolKbCategory.category_id == category_id, ToolKbCategory.del_flag == '0')
                )
            )
            .scalars()
            .first()
        )
        return category

    @classmethod
    async def get_category_detail_by_info(cls, db: AsyncSession, category: ToolKbCategoryModel) -> ToolKbCategory | None:
        category_info = (
            (
                await db.execute(
                    select(ToolKbCategory).where(
                        ToolKbCategory.del_flag == '0',
                        ToolKbCategory.category_name == category.category_name if category.category_name else True,
                        ToolKbCategory.category_code == category.category_code if category.category_code else True,
                    )
                )
            )
            .scalars()
            .first()
        )
        return category_info

    @classmethod
    async def get_category_list(
        cls, db: AsyncSession, query_object: ToolKbCategoryPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        query = (
            select(ToolKbCategory)
            .where(
                ToolKbCategory.del_flag == '0',
                ToolKbCategory.category_name.like(f'%{query_object.category_name}%') if query_object.category_name else True,
                ToolKbCategory.category_code.like(f'%{query_object.category_code}%') if query_object.category_code else True,
                ToolKbCategory.status == query_object.status if query_object.status else True,
            )
            .order_by(ToolKbCategory.category_sort, ToolKbCategory.category_id)
            .distinct()
        )
        category_list: PageModel | list[dict[str, Any]] = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )
        return category_list

    @classmethod
    async def add_category_dao(cls, db: AsyncSession, category: ToolKbCategoryModel) -> ToolKbCategory:
        db_category = ToolKbCategory(**category.model_dump())
        db.add(db_category)
        await db.flush()
        return db_category

    @classmethod
    async def edit_category_dao(cls, db: AsyncSession, category: dict) -> None:
        await db.execute(update(ToolKbCategory), [category])

    @classmethod
    async def delete_category_dao(cls, db: AsyncSession, category_id: int, update_by: str, update_time: Any) -> None:
        await db.execute(
            update(ToolKbCategory)
            .where(ToolKbCategory.category_id == category_id)
            .values(del_flag='2', update_by=update_by, update_time=update_time)
        )

    @classmethod
    async def count_articles_by_category_id(cls, db: AsyncSession, category_id: int) -> int:
        count = (
            await db.execute(
                select(func.count('*')).select_from(ToolKbArticle).where(
                    ToolKbArticle.del_flag == '0', ToolKbArticle.category_id == category_id
                )
            )
        ).scalar()
        return int(count or 0)

