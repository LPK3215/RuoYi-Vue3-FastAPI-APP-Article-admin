from typing import Annotated

from fastapi import Path, Query, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.router import APIRouterPro
from common.vo import DataResponseModel, PageResponseModel
from module_kb.entity.vo.portal_article_vo import (
    PortalArticleCategoryModel,
    PortalArticleDetailModel,
    PortalArticleListItemModel,
    PortalArticlePageQueryModel,
)
from module_kb.entity.vo.portal_tag_vo import PortalTagItemModel
from module_kb.service.portal_article_service import PortalArticleService
from utils.log_util import logger
from utils.response_util import ResponseUtil

portal_article_controller = APIRouterPro(
    prefix='/portal/article',
    order_num=21,
    tags=['用户端-教程'],
)


@portal_article_controller.get(
    '/categories',
    summary='获取教程分类列表接口（用户端）',
    description='用于获取教程分类列表（仅正常且未删除），并附带已发布文章数量',
    response_model=DataResponseModel[list[PortalArticleCategoryModel]],
)
async def get_portal_article_categories(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    categories = await PortalArticleService.get_category_list_services(query_db)
    logger.info('获取成功')
    return ResponseUtil.success(data=categories)


@portal_article_controller.get(
    '/tags',
    summary='获取教程热门标签列表接口（用户端）',
    description='用于获取用户端可用的热门标签（仅正常且未删除），并附带已发布文章数量',
    response_model=DataResponseModel[list[PortalTagItemModel]],
)
async def get_portal_article_tags(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    limit: Annotated[int, Query(description='最多返回数量，默认50，最大200')] = 50,
) -> Response:
    tags = await PortalArticleService.get_tag_list_services(query_db, limit=limit)
    logger.info('获取成功')
    return ResponseUtil.success(data=tags)


@portal_article_controller.get(
    '/list',
    summary='获取教程文章分页列表接口（用户端）',
    description='用于获取教程文章分页列表（仅发布/正常/未删除）',
    response_model=PageResponseModel[PortalArticleListItemModel],
)
async def get_portal_article_list(
    request: Request,
    query_object: Annotated[PortalArticlePageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await PortalArticleService.get_article_list_services(query_db, query_object, is_page=True)
    logger.info('获取成功')
    return ResponseUtil.success(model_content=result)


@portal_article_controller.get(
    '/{article_id}',
    summary='获取教程文章详情接口（用户端）',
    description='用于获取指定教程文章详情（仅发布/正常/未删除，含关联软件列表）',
    response_model=DataResponseModel[PortalArticleDetailModel],
)
async def get_portal_article_detail(
    request: Request,
    article_id: Annotated[int, Path(description='文章ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await PortalArticleService.article_detail_services(query_db, article_id)
    logger.info('获取成功')
    return ResponseUtil.success(data=result)
