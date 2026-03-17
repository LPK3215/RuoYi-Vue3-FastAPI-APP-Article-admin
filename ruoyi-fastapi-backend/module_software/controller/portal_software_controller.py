from typing import Annotated

from fastapi import Path, Query, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.router import APIRouterPro
from common.vo import DataResponseModel, PageResponseModel
from module_software.entity.vo.portal_software_vo import (
    PortalSoftwareCategoryModel,
    PortalSoftwareDetailModel,
    PortalSoftwareListItemModel,
    PortalSoftwarePageQueryModel,
)
from module_software.entity.vo.software_facets_vo import SoftwareFacetsModel
from module_software.service.portal_software_service import PortalSoftwareService
from utils.log_util import logger
from utils.response_util import ResponseUtil

portal_software_controller = APIRouterPro(
    prefix='/portal/software',
    order_num=20,
    tags=['用户端-软件库'],
)


@portal_software_controller.get(
    '/categories',
    summary='获取软件分类列表接口（用户端）',
    description='用于获取软件分类列表（仅正常且未删除），并附带已上架软件数量',
    response_model=DataResponseModel[list[PortalSoftwareCategoryModel]],
)
async def get_portal_software_categories(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    categories = await PortalSoftwareService.get_category_list_services(query_db)
    logger.info('获取成功')
    return ResponseUtil.success(data=categories)


@portal_software_controller.get(
    '/facets',
    summary='获取软件筛选项聚合接口（用户端）',
    description='用于获取用户端可用的筛选项聚合数据（仅上架/正常/未删除）',
    response_model=DataResponseModel[SoftwareFacetsModel],
)
async def get_portal_software_facets(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    limit: Annotated[int, Query(description='每类筛选项最多返回数量，默认50，最大200')] = 50,
) -> Response:
    result = await PortalSoftwareService.get_facets_services(query_db, limit=limit)
    logger.info('获取成功')
    return ResponseUtil.success(data=result)


@portal_software_controller.get(
    '/list',
    summary='获取软件分页列表接口（用户端）',
    description='用于获取软件分页列表（仅上架/正常/未删除）',
    response_model=PageResponseModel[PortalSoftwareListItemModel],
)
async def get_portal_software_list(
    request: Request,
    query_object: Annotated[PortalSoftwarePageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await PortalSoftwareService.get_software_list_services(query_db, query_object, is_page=True)
    logger.info('获取成功')
    return ResponseUtil.success(model_content=result)


@portal_software_controller.get(
    '/{software_id}',
    summary='获取软件详情接口（用户端）',
    description='用于获取指定软件的详细信息（仅上架/正常/未删除，含下载配置）',
    response_model=DataResponseModel[PortalSoftwareDetailModel],
)
async def get_portal_software_detail(
    request: Request,
    software_id: Annotated[int, Path(description='软件ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await PortalSoftwareService.software_detail_services(query_db, software_id)
    logger.info('获取成功')
    return ResponseUtil.success(data=result)
