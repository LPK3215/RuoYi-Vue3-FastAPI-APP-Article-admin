from typing import Any

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_software.entity.do.software_do import ToolSoftware, ToolSoftwareCategory
from module_software.entity.vo.software_category_vo import ToolSoftwareCategoryModel, ToolSoftwareCategoryPageQueryModel
from utils.page_util import PageUtil


class ToolSoftwareCategoryDao:
    """
    软件分类模块数据库操作层
    """

    @classmethod
    async def get_category_detail_by_id(cls, db: AsyncSession, category_id: int) -> ToolSoftwareCategory | None:
        """
        根据分类ID获取分类详细信息
        """
        category = (
            (await db.execute(select(ToolSoftwareCategory).where(ToolSoftwareCategory.category_id == category_id)))
            .scalars()
            .first()
        )
        return category

    @classmethod
    async def get_category_detail_by_info(cls, db: AsyncSession, category: ToolSoftwareCategoryModel) -> ToolSoftwareCategory | None:
        """
        根据分类参数获取分类信息
        """
        category_info = (
            (
                await db.execute(
                    select(ToolSoftwareCategory).where(
                        ToolSoftwareCategory.del_flag == '0',
                        ToolSoftwareCategory.category_name == category.category_name if category.category_name else True,
                        ToolSoftwareCategory.category_code == category.category_code if category.category_code else True,
                    )
                )
            )
            .scalars()
            .first()
        )
        return category_info

    @classmethod
    async def get_category_list(
        cls, db: AsyncSession, query_object: ToolSoftwareCategoryPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        根据查询参数获取分类列表信息
        """
        query = (
            select(ToolSoftwareCategory)
            .where(
                ToolSoftwareCategory.del_flag == '0',
                ToolSoftwareCategory.category_name.like(f'%{query_object.category_name}%')
                if query_object.category_name
                else True,
                ToolSoftwareCategory.category_code.like(f'%{query_object.category_code}%')
                if query_object.category_code
                else True,
                ToolSoftwareCategory.status == query_object.status if query_object.status else True,
            )
            .order_by(ToolSoftwareCategory.category_sort, ToolSoftwareCategory.category_id)
            .distinct()
        )
        category_list: PageModel | list[dict[str, Any]] = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )
        return category_list

    @classmethod
    async def add_category_dao(cls, db: AsyncSession, category: ToolSoftwareCategoryModel) -> ToolSoftwareCategory:
        """
        新增分类数据库操作
        """
        db_category = ToolSoftwareCategory(**category.model_dump())
        db.add(db_category)
        await db.flush()
        return db_category

    @classmethod
    async def edit_category_dao(cls, db: AsyncSession, category: dict) -> None:
        """
        编辑分类数据库操作
        """
        await db.execute(update(ToolSoftwareCategory), [category])

    @classmethod
    async def delete_category_dao(cls, db: AsyncSession, category_id: int, update_by: str, update_time: Any) -> None:
        """
        删除分类数据库操作（软删）
        """
        await db.execute(
            update(ToolSoftwareCategory)
            .where(ToolSoftwareCategory.category_id == category_id)
            .values(del_flag='2', update_by=update_by, update_time=update_time)
        )

    @classmethod
    async def count_software_by_category_id(cls, db: AsyncSession, category_id: int) -> int:
        """
        统计分类下的软件数量（未删除）
        """
        count = (
            await db.execute(
                select(func.count('*'))
                .select_from(ToolSoftware)
                .where(ToolSoftware.del_flag == '0', ToolSoftware.category_id == category_id)
            )
        ).scalar()
        return int(count or 0)
