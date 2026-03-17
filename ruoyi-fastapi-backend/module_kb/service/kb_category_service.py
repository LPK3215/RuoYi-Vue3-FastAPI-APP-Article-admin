from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from common.constant import CommonConstant
from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_kb.dao.kb_category_dao import ToolKbCategoryDao
from module_kb.entity.vo.kb_category_vo import (
    DeleteToolKbCategoryModel,
    ToolKbCategoryModel,
    ToolKbCategoryOptionModel,
    ToolKbCategoryPageQueryModel,
)
from utils.common_util import CamelCaseUtil


class ToolKbCategoryService:
    """
    教程分类模块服务层（管理端）
    """

    @classmethod
    async def get_category_list_services(
        cls, query_db: AsyncSession, query_object: ToolKbCategoryPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        return await ToolKbCategoryDao.get_category_list(query_db, query_object, is_page)

    @classmethod
    async def check_category_name_unique_services(cls, query_db: AsyncSession, page_object: ToolKbCategoryModel) -> bool:
        category_id = -1 if page_object.category_id is None else page_object.category_id
        exists = await ToolKbCategoryDao.get_category_detail_by_info(
            query_db, ToolKbCategoryModel(categoryName=page_object.category_name)
        )
        if exists and exists.category_id != category_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

    @classmethod
    async def add_category_services(cls, query_db: AsyncSession, page_object: ToolKbCategoryModel) -> CrudResponseModel:
        page_object.validate_fields()
        if not await cls.check_category_name_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增分类{page_object.category_name}失败，分类名称已存在')
        page_object.parent_id = int(page_object.parent_id or 0)
        page_object.category_sort = int(page_object.category_sort or 0)
        try:
            await ToolKbCategoryDao.add_category_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def edit_category_services(cls, query_db: AsyncSession, page_object: ToolKbCategoryModel) -> CrudResponseModel:
        if page_object.category_id is None:
            raise ServiceException(message='分类ID不能为空')
        page_object.validate_fields()
        edit_category = page_object.model_dump(exclude_unset=True)
        current = await ToolKbCategoryDao.get_category_detail_by_id(query_db, page_object.category_id)
        if not current or current.del_flag != '0':
            raise ServiceException(message='分类不存在')
        if not await cls.check_category_name_unique_services(query_db, page_object):
            raise ServiceException(message=f'修改分类{page_object.category_name}失败，分类名称已存在')
        edit_category['parent_id'] = int(edit_category.get('parent_id') or 0)
        edit_category['category_sort'] = int(edit_category.get('category_sort') or 0)
        try:
            await ToolKbCategoryDao.edit_category_dao(query_db, edit_category)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='更新成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def delete_category_services(
        cls, query_db: AsyncSession, page_object: DeleteToolKbCategoryModel, update_by: str
    ) -> CrudResponseModel:
        if not page_object.category_ids:
            raise ServiceException(message='传入分类id为空')
        category_id_list = page_object.category_ids.split(',')
        try:
            for category_id_str in category_id_list:
                category_id = int(category_id_str)
                category = await ToolKbCategoryDao.get_category_detail_by_id(query_db, category_id)
                if not category or category.del_flag != '0':
                    raise ServiceException(message='分类不存在')
                used_count = await ToolKbCategoryDao.count_articles_by_category_id(query_db, category_id)
                if used_count > 0:
                    raise ServiceException(message=f'分类【{category.category_name}】已被教程使用，不能删除')
                await ToolKbCategoryDao.delete_category_dao(query_db, category_id, update_by, datetime.now())
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='删除成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def category_detail_services(cls, query_db: AsyncSession, category_id: int) -> ToolKbCategoryModel:
        category = await ToolKbCategoryDao.get_category_detail_by_id(query_db, category_id)
        if not category or category.del_flag != '0':
            return ToolKbCategoryModel()
        return ToolKbCategoryModel(**CamelCaseUtil.transform_result(category))

    @classmethod
    async def get_category_options_services(cls, query_db: AsyncSession) -> list[ToolKbCategoryOptionModel]:
        rows = await ToolKbCategoryDao.get_category_list(
            query_db, ToolKbCategoryPageQueryModel(status='0', pageNum=1, pageSize=1000), is_page=False
        )
        options: list[ToolKbCategoryOptionModel] = []
        for row in rows or []:
            if row.get('delFlag') != '0':
                continue
            options.append(ToolKbCategoryOptionModel(categoryId=row.get('categoryId'), categoryName=row.get('categoryName')))
        return options

