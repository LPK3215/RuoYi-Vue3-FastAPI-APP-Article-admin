from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class PortalSoftwareCategoryModel(BaseModel):
    """
    用户端：软件分类展示模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    category_id: int = Field(description='分类ID')
    category_code: str | None = Field(default=None, description='分类编码')
    category_name: str = Field(description='分类名称')
    software_count: int = Field(default=0, description='已上架软件数量')


class PortalSoftwareDownloadModel(BaseModel):
    """
    用户端：软件多平台下载配置展示模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    platform: str = Field(description='平台标识')
    download_url: str = Field(description='下载地址')
    version: str | None = Field(default=None, description='版本')
    checksum: str | None = Field(default=None, description='校验值')
    sort: int | None = Field(default=None, description='显示顺序')
    remark: str | None = Field(default=None, description='备注')


class PortalSoftwareResourceModel(BaseModel):
    """
    用户端：软件资源展示模型（当前仅存 URL）
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    resource_type: str = Field(description='资源类型')
    title: str | None = Field(default=None, description='标题')
    resource_url: str = Field(description='资源URL')
    sort: int | None = Field(default=None, description='显示顺序')
    remark: str | None = Field(default=None, description='备注')


class PortalSoftwareListItemModel(BaseModel):
    """
    用户端：软件列表展示模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    software_id: int = Field(description='软件ID')
    category_id: int | None = Field(default=None, description='分类ID')
    category_name: str | None = Field(default=None, description='分类名称')
    software_name: str = Field(description='软件名称')
    short_desc: str | None = Field(default=None, description='简短描述')
    icon_url: str | None = Field(default=None, description='图标URL')
    official_url: str | None = Field(default=None, description='官网地址')
    repo_url: str | None = Field(default=None, description='开源地址/仓库地址')
    author: str | None = Field(default=None, description='作者')
    team: str | None = Field(default=None, description='团队/组织')
    license: str | None = Field(default=None, description='许可证')
    open_source: Literal['0', '1'] | None = Field(default=None, description='是否开源（0否 1是）')
    tags: str | None = Field(default=None, description='标签（逗号分隔）')
    publish_status: Literal['1'] = Field(default='1', description='发布状态（固定为上架）')
    update_time: datetime | None = Field(default=None, description='更新时间')


class PortalSoftwareDetailModel(BaseModel):
    """
    用户端：软件详情展示模型（含下载配置）
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    software_id: int = Field(description='软件ID')
    category_id: int | None = Field(default=None, description='分类ID')
    category_name: str | None = Field(default=None, description='分类名称')
    software_name: str = Field(description='软件名称')
    short_desc: str | None = Field(default=None, description='简短描述')
    icon_url: str | None = Field(default=None, description='图标URL')
    official_url: str | None = Field(default=None, description='官网地址')
    repo_url: str | None = Field(default=None, description='开源地址/仓库地址')
    author: str | None = Field(default=None, description='作者')
    team: str | None = Field(default=None, description='团队/组织')
    license: str | None = Field(default=None, description='许可证')
    open_source: Literal['0', '1'] | None = Field(default=None, description='是否开源（0否 1是）')
    tags: str | None = Field(default=None, description='标签（逗号分隔）')
    description_md: str | None = Field(default=None, description='介绍（Markdown）')
    usage_md: str | None = Field(default=None, description='使用说明（Markdown）')
    update_time: datetime | None = Field(default=None, description='更新时间')

    downloads: list[PortalSoftwareDownloadModel] = Field(default_factory=list, description='多平台下载配置列表')
    resources: list[PortalSoftwareResourceModel] = Field(default_factory=list, description='资源URL列表')


class PortalSoftwarePageQueryModel(BaseModel):
    """
    用户端：软件列表查询模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
    category_id: int | None = Field(default=None, description='分类ID')
    keyword: str | None = Field(default=None, description='关键字（软件名称/描述）')
    open_source: Literal['0', '1'] | None = Field(default=None, description='是否开源（0否 1是）')
    license: str | None = Field(default=None, description='许可证')
    tag: str | None = Field(default=None, description='标签（单个标签过滤）')
    platform: str | None = Field(default=None, description='平台标识（存在对应下载配置）')
