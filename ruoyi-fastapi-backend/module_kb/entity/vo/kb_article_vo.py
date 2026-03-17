from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank, Size


class ToolKbArticleTagItemModel(BaseModel):
    """
    教程文章标签项模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    tag_id: int = Field(description='标签ID')
    tag_name: str = Field(description='标签名称')


class ToolKbArticleModel(BaseModel):
    """
    教程文章表对应 pydantic 模型（管理端）
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    article_id: int | None = Field(default=None, description='文章ID')
    category_id: int | None = Field(default=None, description='分类ID')
    category_name: str | None = Field(default=None, description='分类名称')
    title: str | None = Field(default=None, description='标题')
    summary: str | None = Field(default=None, description='摘要')
    cover_url: str | None = Field(default=None, description='封面URL')
    content_md: str | None = Field(default=None, description='正文（Markdown）')
    tags: str | None = Field(default=None, description='标签名称（逗号分隔，兼容旧前端）')
    tag_ids: list[int] | None = Field(default=None, description='标签ID列表')
    tag_list: list[ToolKbArticleTagItemModel] | None = Field(default=None, description='标签列表')
    publish_status: Literal['0', '1', '2'] | None = Field(default=None, description='发布状态（0草稿 1发布 2下线）')
    publish_time: datetime | None = Field(default=None, description='发布时间')
    article_sort: int | None = Field(default=None, description='显示顺序')
    status: Literal['0', '1'] | None = Field(default=None, description='状态（0正常 1停用）')
    del_flag: Literal['0', '2'] | None = Field(default=None, description='删除标志（0存在 2删除）')
    create_by: str | None = Field(default=None, description='创建者')
    create_time: datetime | None = Field(default=None, description='创建时间')
    update_by: str | None = Field(default=None, description='更新者')
    update_time: datetime | None = Field(default=None, description='更新时间')
    remark: str | None = Field(default=None, description='备注')

    software_ids: list[int] | None = Field(default=None, description='关联的软件ID列表')

    @NotBlank(field_name='title', message='标题不能为空')
    @Size(field_name='title', min_length=0, max_length=200, message='标题长度不能超过200个字符')
    def get_title(self) -> str | None:
        return self.title

    @Size(field_name='summary', min_length=0, max_length=500, message='摘要长度不能超过500个字符')
    def get_summary(self) -> str | None:
        return self.summary

    @Size(field_name='cover_url', min_length=0, max_length=500, message='封面URL长度不能超过500个字符')
    def get_cover_url(self) -> str | None:
        return self.cover_url

    @Size(field_name='tags', min_length=0, max_length=500, message='标签长度不能超过500个字符')
    def get_tags(self) -> str | None:
        return self.tags

    def validate_fields(self) -> None:
        self.get_title()
        self.get_summary()
        self.get_cover_url()
        self.get_tags()


class ToolKbArticlePageQueryModel(BaseModel):
    """
    教程文章分页查询模型（管理端）
    """

    model_config = ConfigDict(alias_generator=to_camel)

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
    keyword: str | None = Field(default=None, description='关键字（标题/摘要）')
    category_id: int | None = Field(default=None, description='分类ID')
    tag_id: int | None = Field(default=None, description='标签ID')
    tag: str | None = Field(default=None, description='标签名称（单个标签过滤）')
    publish_status: Literal['0', '1', '2'] | None = Field(default=None, description='发布状态')
    status: Literal['0', '1'] | None = Field(default=None, description='状态（0正常 1停用）')


class DeleteToolKbArticleModel(BaseModel):
    """
    删除教程文章模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    article_ids: str = Field(description='需要删除的文章ID（逗号分隔）')


class ToolKbArticlePublishStatusModel(BaseModel):
    """
    修改教程文章发布状态模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    article_id: int = Field(description='文章ID')
    publish_status: Literal['0', '1', '2'] = Field(description='发布状态（0草稿 1发布 2下线）')
