from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank, Size


class ToolSoftwareDownloadModel(BaseModel):
    """
    软件多平台下载配置表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    download_id: int | None = Field(default=None, description='下载ID')
    software_id: int | None = Field(default=None, description='软件ID')
    platform: str | None = Field(default=None, description='平台标识')
    download_url: str | None = Field(default=None, description='下载地址')
    version: str | None = Field(default=None, description='版本')
    checksum: str | None = Field(default=None, description='校验值')
    sort: int | None = Field(default=None, description='显示顺序')
    remark: str | None = Field(default=None, description='备注')

    @NotBlank(field_name='platform', message='平台标识不能为空')
    @Size(field_name='platform', min_length=0, max_length=32, message='平台标识长度不能超过32个字符')
    def get_platform(self) -> str | None:
        return self.platform

    @NotBlank(field_name='download_url', message='下载地址不能为空')
    @Size(field_name='download_url', min_length=0, max_length=500, message='下载地址长度不能超过500个字符')
    def get_download_url(self) -> str | None:
        return self.download_url

    @Size(field_name='version', min_length=0, max_length=64, message='版本长度不能超过64个字符')
    def get_version(self) -> str | None:
        return self.version

    @Size(field_name='checksum', min_length=0, max_length=128, message='校验值长度不能超过128个字符')
    def get_checksum(self) -> str | None:
        return self.checksum

    def validate_fields(self) -> None:
        self.get_platform()
        self.get_download_url()
        self.get_version()
        self.get_checksum()


class ToolSoftwareResourceModel(BaseModel):
    """
    软件资源表对应pydantic模型（当前仅存 URL）
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    resource_id: int | None = Field(default=None, description='资源ID')
    software_id: int | None = Field(default=None, description='软件ID')
    resource_type: str | None = Field(default=None, description='资源类型')
    title: str | None = Field(default=None, description='标题')
    resource_url: str | None = Field(default=None, description='资源URL')
    sort: int | None = Field(default=None, description='显示顺序')
    remark: str | None = Field(default=None, description='备注')

    @NotBlank(field_name='resource_type', message='资源类型不能为空')
    @Size(field_name='resource_type', min_length=0, max_length=32, message='资源类型长度不能超过32个字符')
    def get_resource_type(self) -> str | None:
        return self.resource_type

    @Size(field_name='title', min_length=0, max_length=200, message='标题长度不能超过200个字符')
    def get_title(self) -> str | None:
        return self.title

    @NotBlank(field_name='resource_url', message='资源URL不能为空')
    @Size(field_name='resource_url', min_length=0, max_length=500, message='资源URL长度不能超过500个字符')
    def get_resource_url(self) -> str | None:
        return self.resource_url

    def validate_fields(self) -> None:
        self.get_resource_type()
        self.get_title()
        self.get_resource_url()


class ToolSoftwareModel(BaseModel):
    """
    软件信息表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    software_id: int | None = Field(default=None, description='软件ID')
    category_id: int | None = Field(default=None, description='分类ID')
    software_name: str | None = Field(default=None, description='软件名称')
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
    publish_status: Literal['0', '1', '2'] | None = Field(default=None, description='发布状态（0草稿 1上架 2下架）')
    software_sort: int | None = Field(default=None, description='显示顺序')
    status: Literal['0', '1'] | None = Field(default=None, description='状态（0正常 1停用）')
    del_flag: Literal['0', '2'] | None = Field(default=None, description='删除标志（0代表存在 2代表删除）')
    create_by: str | None = Field(default=None, description='创建者')
    create_time: datetime | None = Field(default=None, description='创建时间')
    update_by: str | None = Field(default=None, description='更新者')
    update_time: datetime | None = Field(default=None, description='更新时间')
    remark: str | None = Field(default=None, description='备注')

    downloads: list[ToolSoftwareDownloadModel] | None = Field(default=None, description='多平台下载配置列表')
    resources: list[ToolSoftwareResourceModel] | None = Field(default=None, description='资源URL列表')
    category_name: str | None = Field(default=None, description='分类名称（冗余字段，用于列表/详情展示）')

    @NotBlank(field_name='category_id', message='分类不能为空')
    def get_category_id(self) -> int | None:
        return self.category_id

    @NotBlank(field_name='software_name', message='软件名称不能为空')
    @Size(field_name='software_name', min_length=0, max_length=200, message='软件名称长度不能超过200个字符')
    def get_software_name(self) -> str | None:
        return self.software_name

    @NotBlank(field_name='software_sort', message='显示顺序不能为空')
    def get_software_sort(self) -> int | None:
        return self.software_sort

    def validate_fields(self) -> None:
        self.get_category_id()
        self.get_software_name()
        self.get_software_sort()
        if self.downloads:
            for download in self.downloads:
                download.validate_fields()
        if self.resources:
            for resource in self.resources:
                resource.validate_fields()


class ToolSoftwareQueryModel(ToolSoftwareModel):
    """
    软件信息不分页查询模型
    """


class ToolSoftwarePageQueryModel(ToolSoftwareQueryModel):
    """
    软件信息分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
    order_by_column: str | None = Field(default=None, description='排序的字段名称')
    is_asc: Literal['ascending', 'descending'] | None = Field(
        default=None, description='排序方式（ascending升序 descending降序）'
    )
    keyword: str | None = Field(default=None, description='关键字（名称/描述/作者/团队/许可证/标签）')
    tag: str | None = Field(default=None, description='标签（单个标签过滤）')
    platform: str | None = Field(default=None, description='平台标识（存在对应下载配置）')

    # 数据质量筛选（1=有，0=无）
    has_icon: Literal['0', '1'] | None = Field(default=None, description='是否有图标（1有 0无）')
    has_license: Literal['0', '1'] | None = Field(default=None, description='是否有许可证（1有 0无）')
    has_official_url: Literal['0', '1'] | None = Field(default=None, description='是否有官网地址（1有 0无）')
    has_short_desc: Literal['0', '1'] | None = Field(default=None, description='是否有简短描述（1有 0无）')
    has_tags: Literal['0', '1'] | None = Field(default=None, description='是否有标签（1有 0无）')
    has_downloads: Literal['0', '1'] | None = Field(default=None, description='是否配置下载（1有 0无）')
    has_resources: Literal['0', '1'] | None = Field(default=None, description='是否配置资源（1有 0无）')


class DeleteToolSoftwareModel(BaseModel):
    """
    删除软件模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    software_ids: str = Field(description='需要删除的软件ID')


class ToolSoftwarePublishStatusModel(BaseModel):
    """
    修改软件发布状态模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    software_id: int = Field(description='软件ID')
    publish_status: Literal['0', '1', '2'] = Field(description='发布状态（0草稿 1上架 2下架）')


class ToolSoftwareBatchPublishStatusModel(BaseModel):
    """
    批量修改软件发布状态模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    software_ids: list[int] = Field(description='软件ID列表')
    publish_status: Literal['0', '1', '2'] = Field(description='发布状态（0草稿 1上架 2下架）')


class ToolSoftwareBatchMoveCategoryModel(BaseModel):
    """
    批量移动软件分类模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    software_ids: list[int] = Field(description='软件ID列表')
    category_id: int = Field(description='目标分类ID')


class ToolSoftwareBatchTagsModel(BaseModel):
    """
    批量标签治理模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    software_ids: list[int] = Field(description='软件ID列表')
    action: Literal['append', 'remove', 'replace'] = Field(description='标签操作（append追加 remove移除 replace覆盖）')
    tags: str | None = Field(default=None, description='标签（逗号/换行分隔；replace 允许为空表示清空）')
