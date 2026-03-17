from datetime import datetime
from typing import Annotated

from fastapi import Path, Query, Request, Response
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession

from common.annotation.log_annotation import Log
from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.enums import BusinessType
from common.router import APIRouterPro
from common.vo import DataResponseModel, PageResponseModel, ResponseBaseModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_kb.entity.vo.kb_category_vo import (
    DeleteToolKbCategoryModel,
    ToolKbCategoryModel,
    ToolKbCategoryOptionModel,
    ToolKbCategoryPageQueryModel,
)
from module_kb.service.kb_category_service import ToolKbCategoryService
from utils.log_util import logger
from utils.response_util import ResponseUtil

kb_category_controller = APIRouterPro(
    prefix='/tool/kb/category',
    order_num=18,
    tags=['系统工具-知识库-教程分类'],
    dependencies=[PreAuthDependency()],
)


@kb_category_controller.get(
    '/list',
    summary='获取教程分类分页列表接口',
    description='用于获取教程分类分页列表',
    response_model=PageResponseModel[ToolKbCategoryModel],
    dependencies=[UserInterfaceAuthDependency('tool:kb:category:list')],
)
async def get_kb_category_list(
    request: Request,
    category_page_query: Annotated[ToolKbCategoryPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await ToolKbCategoryService.get_category_list_services(query_db, category_page_query, is_page=True)
    logger.info('获取成功')
    return ResponseUtil.success(model_content=result)


@kb_category_controller.get(
    '/options',
    summary='获取教程分类下拉选项接口',
    description='用于获取教程分类下拉选项（仅正常且未删除）',
    response_model=DataResponseModel[list[ToolKbCategoryOptionModel]],
    dependencies=[UserInterfaceAuthDependency('tool:kb:category:list')],
)
async def get_kb_category_options(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    options = await ToolKbCategoryService.get_category_options_services(query_db)
    logger.info('获取成功')
    return ResponseUtil.success(data=options)


@kb_category_controller.get(
    '/{category_id}',
    summary='获取教程分类详情接口',
    description='用于获取指定教程分类的详细信息',
    response_model=DataResponseModel[ToolKbCategoryModel],
    dependencies=[UserInterfaceAuthDependency('tool:kb:category:query')],
)
async def query_kb_category_detail(
    request: Request,
    category_id: Annotated[int, Path(description='分类ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await ToolKbCategoryService.category_detail_services(query_db, category_id)
    logger.info(f'获取category_id为{category_id}的信息成功')
    return ResponseUtil.success(data=result)


@kb_category_controller.post(
    '',
    summary='新增教程分类接口',
    description='用于新增教程分类',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:kb:category:add')],
)
@ValidateFields(validate_model='add_kb_category')
@Log(title='教程分类', business_type=BusinessType.INSERT)
async def add_kb_category(
    request: Request,
    add_category: ToolKbCategoryModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_category.create_by = current_user.user.user_name
    add_category.create_time = datetime.now()
    add_category.update_by = current_user.user.user_name
    add_category.update_time = datetime.now()
    result = await ToolKbCategoryService.add_category_services(query_db, add_category)
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)


@kb_category_controller.put(
    '',
    summary='编辑教程分类接口',
    description='用于编辑教程分类',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:kb:category:edit')],
)
@ValidateFields(validate_model='edit_kb_category')
@Log(title='教程分类', business_type=BusinessType.UPDATE)
async def edit_kb_category(
    request: Request,
    edit_category: ToolKbCategoryModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_category.update_by = current_user.user.user_name
    edit_category.update_time = datetime.now()
    result = await ToolKbCategoryService.edit_category_services(query_db, edit_category)
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)


@kb_category_controller.delete(
    '/{category_ids}',
    summary='删除教程分类接口',
    description='用于删除教程分类（软删）',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:kb:category:remove')],
)
@Log(title='教程分类', business_type=BusinessType.DELETE)
async def delete_kb_category(
    request: Request,
    category_ids: Annotated[str, Path(description='需要删除的分类ID，多个用逗号分隔')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    delete_category = DeleteToolKbCategoryModel(categoryIds=category_ids)
    result = await ToolKbCategoryService.delete_category_services(
        query_db, delete_category, update_by=current_user.user.user_name
    )
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)

