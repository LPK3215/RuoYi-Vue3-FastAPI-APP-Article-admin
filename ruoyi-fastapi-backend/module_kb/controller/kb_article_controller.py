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
from module_kb.entity.vo.kb_article_vo import (
    DeleteToolKbArticleModel,
    ToolKbArticleModel,
    ToolKbArticlePageQueryModel,
    ToolKbArticlePublishStatusModel,
)
from module_kb.service.kb_article_service import ToolKbArticleService
from utils.log_util import logger
from utils.response_util import ResponseUtil

kb_article_controller = APIRouterPro(
    prefix='/tool/kb/article',
    order_num=18,
    tags=['系统工具-知识库-教程管理'],
    dependencies=[PreAuthDependency()],
)


@kb_article_controller.get(
    '/list',
    summary='获取教程文章分页列表接口',
    description='用于获取教程文章分页列表',
    response_model=PageResponseModel[ToolKbArticleModel],
    dependencies=[UserInterfaceAuthDependency('tool:kb:article:list')],
)
async def get_kb_article_list(
    request: Request,
    article_page_query: Annotated[ToolKbArticlePageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await ToolKbArticleService.get_article_list_services(query_db, article_page_query, is_page=True)
    logger.info('获取成功')
    return ResponseUtil.success(model_content=result)


@kb_article_controller.get(
    '/{article_id}',
    summary='获取教程文章详情接口',
    description='用于获取指定教程文章详情（含关联软件ID列表）',
    response_model=DataResponseModel[ToolKbArticleModel],
    dependencies=[UserInterfaceAuthDependency('tool:kb:article:query')],
)
async def get_kb_article_detail(
    request: Request,
    article_id: Annotated[int, Path(description='文章ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await ToolKbArticleService.article_detail_services(query_db, article_id)
    logger.info('获取成功')
    return ResponseUtil.success(data=result)


@kb_article_controller.post(
    '',
    summary='新增教程文章接口',
    description='用于新增教程文章',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:kb:article:add')],
)
@Log(title='教程管理', business_type=BusinessType.INSERT)
@ValidateFields(validate_model='add_kb_article')
async def add_kb_article(
    request: Request,
    add_article: ToolKbArticleModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    now = datetime.now()
    add_article.create_by = current_user.user.user_name
    add_article.create_time = now
    add_article.update_by = current_user.user.user_name
    add_article.update_time = now
    result = await ToolKbArticleService.add_article_services(query_db, add_article)
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message, data=result.result)


@kb_article_controller.put(
    '',
    summary='修改教程文章接口',
    description='用于修改教程文章',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:kb:article:edit')],
)
@Log(title='教程管理', business_type=BusinessType.UPDATE)
@ValidateFields(validate_model='edit_kb_article')
async def edit_kb_article(
    request: Request,
    edit_article: ToolKbArticleModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_article.update_by = current_user.user.user_name
    edit_article.update_time = datetime.now()
    result = await ToolKbArticleService.edit_article_services(query_db, edit_article)
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)


@kb_article_controller.delete(
    '/{article_ids}',
    summary='删除教程文章接口',
    description='用于删除教程文章（软删）',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:kb:article:remove')],
)
@Log(title='教程管理', business_type=BusinessType.DELETE)
async def delete_kb_article(
    request: Request,
    article_ids: Annotated[str, Path(description='需要删除的文章ID，多个用逗号分隔')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    page_object = DeleteToolKbArticleModel(articleIds=article_ids)
    result = await ToolKbArticleService.delete_article_services(query_db, page_object, update_by=current_user.user.user_name)
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)


@kb_article_controller.put(
    '/changePublishStatus',
    summary='修改教程文章发布状态接口',
    description='用于修改教程文章发布状态（草稿/发布/下线）',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:kb:article:publish')],
)
@Log(title='教程管理', business_type=BusinessType.UPDATE)
async def change_kb_article_publish_status(
    request: Request,
    change_model: ToolKbArticlePublishStatusModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await ToolKbArticleService.change_publish_status_services(
        query_db, change_model, update_by=current_user.user.user_name
    )
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)

