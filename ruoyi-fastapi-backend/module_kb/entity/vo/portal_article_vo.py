from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from module_software.entity.vo.portal_software_vo import PortalSoftwareListItemModel


class PortalArticleTagItemModel(BaseModel):
    """
    用户端：教程标签项模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    tag_id: int = Field(description='标签ID')
    tag_name: str = Field(description='标签名称')


class PortalArticleCategoryModel(BaseModel):
    """
    用户端：教程分类展示模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    category_id: int = Field(description='分类ID')
    category_code: str | None = Field(default=None, description='分类编码')
    category_name: str = Field(description='分类名称')
    article_count: int = Field(default=0, description='已发布文章数量')


class PortalArticleListItemModel(BaseModel):
    """
    用户端：教程文章列表项模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    article_id: int = Field(description='文章ID')
    title: str = Field(description='标题')
    summary: str | None = Field(default=None, description='摘要')
    cover_url: str | None = Field(default=None, description='封面URL')
    tags: str | None = Field(default=None, description='标签（逗号分隔）')
    tag_list: list[PortalArticleTagItemModel] = Field(default_factory=list, description='标签列表')
    article_type: str | None = Field(default=None, description='文章类型（字典 kb_article_type）')
    publish_time: datetime | None = Field(default=None, description='发布时间')
    update_time: datetime | None = Field(default=None, description='更新时间')


class PortalArticleDetailModel(BaseModel):
    """
    用户端：教程文章详情模型（含关联软件列表）
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, validate_by_name=True)

    article_id: int = Field(description='文章ID')
    title: str = Field(description='标题')
    summary: str | None = Field(default=None, description='摘要')
    cover_url: str | None = Field(default=None, description='封面URL')
    content_md: str | None = Field(default=None, description='正文（Markdown）')
    tags: str | None = Field(default=None, description='标签（逗号分隔）')
    tag_list: list[PortalArticleTagItemModel] = Field(default_factory=list, description='标签列表')
    article_type: str | None = Field(default=None, description='文章类型（字典 kb_article_type）')
    publish_time: datetime | None = Field(default=None, description='发布时间')
    update_time: datetime | None = Field(default=None, description='更新时间')

    softwares: list[PortalSoftwareListItemModel] = Field(default_factory=list, description='关联的软件列表（仅上架）')

    attachments: list[dict[str, object]] = Field(default_factory=list, description='附件列表（简化：[{name,url,size}]）')


class PortalArticlePageQueryModel(BaseModel):
    """
    用户端：教程文章列表查询模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
    keyword: str | None = Field(default=None, description='关键字（标题/摘要）')
    category_id: int | None = Field(default=None, description='分类ID')
    tag_id: int | None = Field(default=None, description='标签ID')
    tag: str | None = Field(default=None, description='标签（单个标签过滤）')
    article_type: str | None = Field(default=None, description='文章类型（字典 kb_article_type）')
    software_id: int | None = Field(default=None, description='软件ID（查询关联教程）')

