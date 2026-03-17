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
from module_kb.entity.vo.kb_tag_vo import (
    DeleteToolKbTagModel,
    ToolKbTagModel,
    ToolKbTagOptionModel,
    ToolKbTagPageQueryModel,
)
from module_kb.service.kb_tag_service import ToolKbTagService
from utils.log_util import logger
from utils.response_util import ResponseUtil

kb_tag_controller = APIRouterPro(
    prefix='/tool/kb/tag',
    order_num=18,
    tags=['系统工具-知识库-教程标签'],
    dependencies=[PreAuthDependency()],
)


@kb_tag_controller.get(
    '/list',
    summary='获取教程标签分页列表接口',
    description='用于获取教程标签分页列表',
    response_model=PageResponseModel[ToolKbTagModel],
    dependencies=[UserInterfaceAuthDependency('tool:kb:tag:list')],
)
async def get_kb_tag_list(
    request: Request,
    tag_page_query: Annotated[ToolKbTagPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await ToolKbTagService.get_tag_list_services(query_db, tag_page_query, is_page=True)
    logger.info('获取成功')
    return ResponseUtil.success(model_content=result)


@kb_tag_controller.get(
    '/options',
    summary='获取教程标签下拉选项接口',
    description='用于获取教程标签下拉选项（仅正常且未删除）',
    response_model=DataResponseModel[list[ToolKbTagOptionModel]],
    dependencies=[UserInterfaceAuthDependency('tool:kb:tag:list')],
)
async def get_kb_tag_options(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    options = await ToolKbTagService.get_tag_options_services(query_db)
    logger.info('获取成功')
    return ResponseUtil.success(data=options)


@kb_tag_controller.get(
    '/{tag_id}',
    summary='获取教程标签详情接口',
    description='用于获取指定教程标签的详细信息',
    response_model=DataResponseModel[ToolKbTagModel],
    dependencies=[UserInterfaceAuthDependency('tool:kb:tag:query')],
)
async def query_kb_tag_detail(
    request: Request,
    tag_id: Annotated[int, Path(description='标签ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await ToolKbTagService.tag_detail_services(query_db, tag_id)
    logger.info(f'获取tag_id为{tag_id}的信息成功')
    return ResponseUtil.success(data=result)


@kb_tag_controller.post(
    '',
    summary='新增教程标签接口',
    description='用于新增教程标签',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:kb:tag:add')],
)
@ValidateFields(validate_model='add_kb_tag')
@Log(title='教程标签', business_type=BusinessType.INSERT)
async def add_kb_tag(
    request: Request,
    add_tag: ToolKbTagModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_tag.create_by = current_user.user.user_name
    add_tag.create_time = datetime.now()
    add_tag.update_by = current_user.user.user_name
    add_tag.update_time = datetime.now()
    result = await ToolKbTagService.add_tag_services(query_db, add_tag)
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)


@kb_tag_controller.put(
    '',
    summary='编辑教程标签接口',
    description='用于编辑教程标签',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:kb:tag:edit')],
)
@ValidateFields(validate_model='edit_kb_tag')
@Log(title='教程标签', business_type=BusinessType.UPDATE)
async def edit_kb_tag(
    request: Request,
    edit_tag: ToolKbTagModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_tag.update_by = current_user.user.user_name
    edit_tag.update_time = datetime.now()
    result = await ToolKbTagService.edit_tag_services(query_db, edit_tag)
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)


@kb_tag_controller.delete(
    '/{tag_ids}',
    summary='删除教程标签接口',
    description='用于删除教程标签（软删）',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:kb:tag:remove')],
)
@Log(title='教程标签', business_type=BusinessType.DELETE)
async def delete_kb_tag(
    request: Request,
    tag_ids: Annotated[str, Path(description='需要删除的标签ID，多个用逗号分隔')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    delete_tag = DeleteToolKbTagModel(tagIds=tag_ids)
    result = await ToolKbTagService.delete_tag_services(query_db, delete_tag, update_by=current_user.user.user_name)
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)

