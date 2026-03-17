from datetime import datetime
from typing import Annotated

from fastapi import File, Form, Path, Query, Request, Response, UploadFile
from fastapi.responses import StreamingResponse
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
from module_software.entity.vo.software_dashboard_vo import SoftwareDashboardOverviewModel
from module_software.entity.vo.software_facets_vo import SoftwareFacetsModel
from module_software.entity.vo.software_item_vo import (
    DeleteToolSoftwareModel,
    ToolSoftwareBatchMoveCategoryModel,
    ToolSoftwareBatchPublishStatusModel,
    ToolSoftwareBatchTagsModel,
    ToolSoftwareModel,
    ToolSoftwarePageQueryModel,
    ToolSoftwarePublishStatusModel,
)
from module_software.service.software_item_service import ToolSoftwareService
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.response_util import ResponseUtil

software_item_controller = APIRouterPro(
    prefix='/tool/software/item',
    order_num=19,
    tags=['系统工具-软件库-软件管理'],
    dependencies=[PreAuthDependency()],
)


@software_item_controller.get(
    '/list',
    summary='获取软件分页列表接口',
    description='用于获取软件分页列表',
    response_model=PageResponseModel[ToolSoftwareModel],
    dependencies=[UserInterfaceAuthDependency('tool:software:item:list')],
)
async def get_software_item_list(
    request: Request,
    software_page_query: Annotated[ToolSoftwarePageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    software_page_query_result = await ToolSoftwareService.get_software_list_services(
        query_db, software_page_query, is_page=True
    )
    logger.info('获取成功')
    return ResponseUtil.success(model_content=software_page_query_result)


@software_item_controller.post(
    '/export',
    summary='导出软件列表接口',
    description='用于导出当前符合查询条件的软件列表数据',
    response_class=StreamingResponse,
    responses={
        200: {
            'description': '流式返回软件列表excel文件',
            'content': {
                'application/octet-stream': {},
            },
        }
    },
    dependencies=[UserInterfaceAuthDependency('tool:software:item:list')],
)
@Log(title='软件管理', business_type=BusinessType.EXPORT)
async def export_software_item_list(
    request: Request,
    software_page_query: Annotated[ToolSoftwarePageQueryModel, Form()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    software_list = await ToolSoftwareService.get_software_list_services(query_db, software_page_query, is_page=False)
    export_binary = await ToolSoftwareService.export_software_list_services(software_list)
    logger.info('导出成功')
    return ResponseUtil.streaming(data=bytes2file_response(export_binary), media_type='application/octet-stream')


@software_item_controller.post(
    '/importData',
    summary='批量导入软件接口',
    description='用于批量导入软件基础信息（Excel）',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:software:item:edit')],
)
@Log(title='软件管理', business_type=BusinessType.IMPORT)
async def batch_import_software_item(
    request: Request,
    file: Annotated[UploadFile, File(...)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
    update_support: Annotated[bool, Query(alias='updateSupport')] = False,
) -> Response:
    result = await ToolSoftwareService.batch_import_software_services(
        query_db,
        file,
        update_support,
        update_by=current_user.user.user_name,
    )
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)


@software_item_controller.post(
    '/importTemplate',
    summary='获取软件导入模板接口',
    description='用于获取软件导入模板excel文件',
    response_class=StreamingResponse,
    responses={
        200: {
            'description': '流式返回软件导入模板excel文件',
            'content': {
                'application/octet-stream': {},
            },
        }
    },
    dependencies=[UserInterfaceAuthDependency('tool:software:item:edit')],
)
async def export_software_item_template(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    template_binary = await ToolSoftwareService.get_software_import_template_services()
    logger.info('获取成功')
    return ResponseUtil.streaming(data=bytes2file_response(template_binary), media_type='application/octet-stream')


@software_item_controller.get(
    '/facets',
    summary='获取软件筛选项聚合接口（后台）',
    description='用于获取软件筛选项聚合数据（标签/许可证/作者/平台等），便于构建下拉/筛选 UI',
    response_model=DataResponseModel[SoftwareFacetsModel],
    dependencies=[UserInterfaceAuthDependency('tool:software:item:list')],
)
async def get_software_item_facets(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    limit: Annotated[int, Query(description='每类筛选项最多返回数量，默认50，最大200')] = 50,
) -> Response:
    result = await ToolSoftwareService.get_facets_services(query_db, limit=limit)
    logger.info('获取成功')
    return ResponseUtil.success(data=result)


@software_item_controller.get(
    '/overview',
    summary='获取软件库首页看板数据（后台）',
    description='聚合返回 KPI / 维度分布 / 数据质量 / 最近更新 / 草稿待处理，用于后台首页看板展示',
    response_model=DataResponseModel[SoftwareDashboardOverviewModel],
    dependencies=[UserInterfaceAuthDependency('tool:software:item:list')],
)
async def get_software_item_overview(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    limit: Annotated[int, Query(description='facets 每类最多返回数量，默认12，最大200')] = 12,
    recent_limit: Annotated[int, Query(alias='recentLimit', description='最近更新/草稿列表最多返回数量，默认6，最大50')] = 6,
) -> Response:
    result = await ToolSoftwareService.get_dashboard_overview_services(query_db, limit=limit, recent_limit=recent_limit)
    logger.info('获取成功')
    return ResponseUtil.success(data=result)


@software_item_controller.get(
    '/{software_id}',
    summary='获取软件详情接口',
    description='用于获取指定软件的详细信息（含下载配置）',
    response_model=DataResponseModel[ToolSoftwareModel],
    dependencies=[UserInterfaceAuthDependency('tool:software:item:query')],
)
async def query_software_item_detail(
    request: Request,
    software_id: Annotated[int, Path(description='软件ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    software_detail_result = await ToolSoftwareService.software_detail_services(query_db, software_id)
    logger.info(f'获取software_id为{software_id}的信息成功')
    return ResponseUtil.success(data=software_detail_result)


@software_item_controller.post(
    '',
    summary='新增软件接口',
    description='用于新增软件（含下载配置）',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:software:item:add')],
)
@ValidateFields(validate_model='add_software')
@Log(title='软件管理', business_type=BusinessType.INSERT)
async def add_software_item(
    request: Request,
    add_software: ToolSoftwareModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_software.create_by = current_user.user.user_name
    add_software.create_time = datetime.now()
    add_software.update_by = current_user.user.user_name
    add_software.update_time = datetime.now()
    add_software_result = await ToolSoftwareService.add_software_services(query_db, add_software)
    logger.info(add_software_result.message)
    return ResponseUtil.success(msg=add_software_result.message)


@software_item_controller.put(
    '',
    summary='编辑软件接口',
    description='用于编辑软件（含下载配置全量覆盖）',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:software:item:edit')],
)
@ValidateFields(validate_model='edit_software')
@Log(title='软件管理', business_type=BusinessType.UPDATE)
async def edit_software_item(
    request: Request,
    edit_software: ToolSoftwareModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_software.update_by = current_user.user.user_name
    edit_software.update_time = datetime.now()
    edit_software_result = await ToolSoftwareService.edit_software_services(query_db, edit_software)
    logger.info(edit_software_result.message)
    return ResponseUtil.success(msg=edit_software_result.message)


@software_item_controller.delete(
    '/{software_ids}',
    summary='删除软件接口',
    description='用于删除软件（软删）',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:software:item:remove')],
)
@Log(title='软件管理', business_type=BusinessType.DELETE)
async def delete_software_item(
    request: Request,
    software_ids: Annotated[str, Path(description='需要删除的软件ID，多个用逗号分隔')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    delete_software = DeleteToolSoftwareModel(softwareIds=software_ids)
    delete_result = await ToolSoftwareService.delete_software_services(
        query_db, delete_software, update_by=current_user.user.user_name
    )
    logger.info(delete_result.message)
    return ResponseUtil.success(msg=delete_result.message)


@software_item_controller.put(
    '/changePublishStatus',
    summary='修改软件发布状态接口',
    description='用于修改软件发布状态（草稿/上架/下架）',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:software:item:publish')],
)
@Log(title='软件管理', business_type=BusinessType.UPDATE)
async def change_software_publish_status(
    request: Request,
    change_model: ToolSoftwarePublishStatusModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await ToolSoftwareService.change_publish_status_services(
        query_db, change_model, update_by=current_user.user.user_name
    )
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)


@software_item_controller.put(
    '/batchChangePublishStatus',
    summary='批量修改软件发布状态接口',
    description='用于批量修改软件发布状态（草稿/上架/下架）',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:software:item:publish')],
)
@Log(title='软件管理', business_type=BusinessType.UPDATE)
async def batch_change_software_publish_status(
    request: Request,
    change_model: ToolSoftwareBatchPublishStatusModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await ToolSoftwareService.batch_change_publish_status_services(
        query_db, change_model, update_by=current_user.user.user_name
    )
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)


@software_item_controller.put(
    '/batchMoveCategory',
    summary='批量移动软件分类接口',
    description='用于批量将软件移动到指定分类',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:software:item:edit')],
)
@Log(title='软件管理', business_type=BusinessType.UPDATE)
async def batch_move_software_category(
    request: Request,
    change_model: ToolSoftwareBatchMoveCategoryModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await ToolSoftwareService.batch_move_category_services(
        query_db, change_model, update_by=current_user.user.user_name
    )
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)


@software_item_controller.put(
    '/batchManageTags',
    summary='批量标签治理接口',
    description='用于批量追加/移除/覆盖软件标签（逗号/换行分隔，自动去重与规范化）',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('tool:software:item:edit')],
)
@Log(title='软件管理', business_type=BusinessType.UPDATE)
async def batch_manage_software_tags(
    request: Request,
    change_model: ToolSoftwareBatchTagsModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await ToolSoftwareService.batch_manage_tags_services(
        query_db, change_model, update_by=current_user.user.user_name
    )
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)
