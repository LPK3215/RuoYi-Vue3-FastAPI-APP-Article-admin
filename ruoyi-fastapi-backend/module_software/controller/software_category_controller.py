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
from module_software.entity.vo.software_category_vo import (
    DeleteToolSoftwareCategoryModel,
    ToolSoftwareCategoryModel,
    ToolSoftwareCategoryOptionModel,
    ToolSoftwareCategoryPageQueryModel,
)
from module_software.service.software_category_service import ToolSoftwareCategoryService
from utils.log_util import logger
from utils.response_util import ResponseUtil

software_category_controller = APIRouterPro(
    prefix='/tool/software/category',
    order_num=18,
    tags=['系统工具-软件库-分类管理'],
    dependencies=[PreAuthDependency()],
)


@software_category_controller.get(
    '/list',
    summary='获取软件分类分页列表接口',
    description='用于获取软件分类分页列表',
    response_model=PageResponseModel[ToolSoftwareCategoryModel],
    dependencies=[UserInterfaceAuthDependency('tool:software:category:list')],
)
async def get_software_category_list(
    request: Request,
    category_page_query: Annotated[ToolSoftwareCategoryPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    category_page_query_result = await ToolSoftwareCategoryService.get_category_list_services(
        query_db, category_page_query, is_page=True
    )
    logger.info('获取成功')
    return ResponseUtil.success(model_content=category_page_query_result)


@software_category_controller.get(
    '/options',
    summary='获取软件分类下拉选项接口',
    description='用于获取软件分类下拉选项（仅正常且未删除）',
    response_model=DataResponseModel[list[ToolSoftwareCategoryOptionModel]],
    dependencies=[UserInterfaceAuthDependency('tool:software:category:list')],
)
async def get_software_category_options(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    options = await ToolSoftwareCategoryService.get_category_options_services(query_db)
    logger.info('获取成功')
    return ResponseUtil.success(data=options)


@software_category_controller.get(
    '/{category_id}',
    summary='获取软件分类详情接口',
    description='用于获取指定软件分类的详细信息',
    response_model=DataResponseModel[ToolSoftwareCategoryModel],
    dependencies=[UserInterfaceAuthDependency('tool:software:category:query')],
)
async def query_software_category_detail(
    request: Request,
    category_id: Annotated[int, Path(description='分类ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    category_detail_result = await ToolSoftwareCategoryService.category_detail_services(query_db, category_id)
    logger.info(f'获取category_id为{category_id}的信息成功')
    return ResponseUtil.success(data=category_detail_result)


@software_category_controller.post(
    '',
    summary='新增软件分类接口',
    description='用于新增软件分类',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:software:category:add')],
)
@ValidateFields(validate_model='add_category')
@Log(title='软件分类', business_type=BusinessType.INSERT)
async def add_software_category(
    request: Request,
    add_category: ToolSoftwareCategoryModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_category.create_by = current_user.user.user_name
    add_category.create_time = datetime.now()
    add_category.update_by = current_user.user.user_name
    add_category.update_time = datetime.now()
    add_category_result = await ToolSoftwareCategoryService.add_category_services(query_db, add_category)
    logger.info(add_category_result.message)
    return ResponseUtil.success(msg=add_category_result.message)


@software_category_controller.put(
    '',
    summary='编辑软件分类接口',
    description='用于编辑软件分类',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:software:category:edit')],
)
@ValidateFields(validate_model='edit_category')
@Log(title='软件分类', business_type=BusinessType.UPDATE)
async def edit_software_category(
    request: Request,
    edit_category: ToolSoftwareCategoryModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_category.update_by = current_user.user.user_name
    edit_category.update_time = datetime.now()
    edit_category_result = await ToolSoftwareCategoryService.edit_category_services(query_db, edit_category)
    logger.info(edit_category_result.message)
    return ResponseUtil.success(msg=edit_category_result.message)


@software_category_controller.delete(
    '/{category_ids}',
    summary='删除软件分类接口',
    description='用于删除软件分类（软删）',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:software:category:remove')],
)
@Log(title='软件分类', business_type=BusinessType.DELETE)
async def delete_software_category(
    request: Request,
    category_ids: Annotated[str, Path(description='需要删除的分类ID，多个用逗号分隔')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    delete_category = DeleteToolSoftwareCategoryModel(categoryIds=category_ids)
    delete_result = await ToolSoftwareCategoryService.delete_category_services(
        query_db, delete_category, update_by=current_user.user.user_name
    )
    logger.info(delete_result.message)
    return ResponseUtil.success(msg=delete_result.message)
