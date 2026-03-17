from typing import Annotated

from fastapi import Body, Query, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.router import APIRouterPro
from common.vo import DataResponseModel, ResponseBaseModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_software.entity.vo.software_scan_vo import (
    LocalInstalledSoftwareModel,
    LocalSoftwareScanImportRequestModel,
    LocalSoftwareScanImportResultModel,
    LocalSoftwareScanQueryModel,
)
from module_software.service.software_scan_service import ToolSoftwareScanService
from utils.log_util import logger
from utils.response_util import ResponseUtil

software_scan_controller = APIRouterPro(
    prefix='/tool/software/scan',
    order_num=19,
    tags=['系统工具-软件库-本机扫描导入'],
    dependencies=[PreAuthDependency()],
)


@software_scan_controller.get(
    '/list',
    summary='扫描本机已安装软件（Windows）',
    description='读取注册表 Uninstall 项，返回可导入的软件列表（仅名称/版本/发布者等基础信息）',
    response_model=DataResponseModel[list[LocalInstalledSoftwareModel]],
    dependencies=[UserInterfaceAuthDependency('tool:software:item:edit')],
)
async def scan_local_installed_softwares(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    keyword: Annotated[str | None, Query(description='关键字（名称/发布者/版本）')] = None,
    limit: Annotated[int, Query(description='最多返回数量（默认500，最大3000）')] = 500,
) -> Response:
    q = LocalSoftwareScanQueryModel(keyword=keyword, limit=limit)
    items = await ToolSoftwareScanService.scan_services(q)
    logger.info('扫描成功')
    return ResponseUtil.success(data=items)


@software_scan_controller.post(
    '/import',
    summary='导入本机扫描结果到软件库（按同名匹配）',
    description='支持选择部分导入；遇到同名软件可选择跳过/更新；默认导入到“本机导入”分类',
    response_model=DataResponseModel[LocalSoftwareScanImportResultModel],
    dependencies=[UserInterfaceAuthDependency('tool:software:item:edit')],
)
async def import_local_installed_softwares(
    request: Request,
    body: Annotated[LocalSoftwareScanImportRequestModel, Body()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await ToolSoftwareScanService.import_services(query_db, body, operator_name=current_user.user.user_name)
    logger.info(result.message)
    return ResponseUtil.success(data=result.result)
