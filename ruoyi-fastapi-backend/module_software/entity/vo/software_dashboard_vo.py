from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from module_software.entity.vo.software_facets_vo import SoftwareFacetsModel


class SoftwareDashboardKpiModel(BaseModel):
    """
    软件库看板 KPI（后台管理端）
    """

    model_config = ConfigDict(alias_generator=to_camel)

    software_total: int = Field(default=0, description='软件总数（仅排除软删）')
    published: int = Field(default=0, description='上架数量')
    draft: int = Field(default=0, description='草稿数量')
    offline: int = Field(default=0, description='下架数量')
    categories: int = Field(default=0, description='分类数量（仅排除软删）')


class SoftwareDashboardQualityModel(BaseModel):
    """
    数据质量统计（用于提示“缺字段/缺配置”的数据）
    """

    model_config = ConfigDict(alias_generator=to_camel)

    missing_icon: int = Field(default=0, description='缺少图标（iconUrl 为空）')
    missing_license: int = Field(default=0, description='缺少许可证（license 为空）')
    missing_official_url: int = Field(default=0, description='缺少官网地址（officialUrl 为空）')
    missing_short_desc: int = Field(default=0, description='缺少简短描述（shortDesc 为空）')
    missing_tags: int = Field(default=0, description='缺少标签（tags 为空）')
    missing_downloads: int = Field(default=0, description='缺少下载配置（downloads 为空）')
    missing_resources: int = Field(default=0, description='缺少资源配置（resources 为空）')


class SoftwareDashboardListItemModel(BaseModel):
    """
    看板列表项（最近更新/草稿待处理）
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    software_id: int = Field(description='软件ID')
    software_name: str = Field(description='软件名称')
    short_desc: str | None = Field(default=None, description='简短描述')
    publish_status: Literal['0', '1', '2'] | None = Field(default=None, description='发布状态（0草稿 1上架 2下架）')
    update_time: datetime | None = Field(default=None, description='更新时间')


class SoftwareDashboardOverviewModel(BaseModel):
    """
    软件库首页看板数据（聚合接口）
    """

    model_config = ConfigDict(alias_generator=to_camel)

    kpi: SoftwareDashboardKpiModel = Field(description='核心 KPI')
    facets: SoftwareFacetsModel = Field(description='筛选维度聚合（标签/许可证/平台等）')
    quality: SoftwareDashboardQualityModel = Field(description='数据质量统计')
    recent: list[SoftwareDashboardListItemModel] = Field(default_factory=list, description='最近更新')
    drafts: list[SoftwareDashboardListItemModel] = Field(default_factory=list, description='草稿待处理')

