from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class SoftwareFacetItemModel(BaseModel):
    """
    通用筛选项（值 + 数量）
    """

    model_config = ConfigDict(alias_generator=to_camel)

    value: str = Field(description='筛选项值')
    count: int = Field(default=0, description='数量（软件数）')


class SoftwareFacetsModel(BaseModel):
    """
    软件筛选项聚合（用于前端构建筛选 UI）
    """

    model_config = ConfigDict(alias_generator=to_camel)

    tags: list[SoftwareFacetItemModel] = Field(default_factory=list, description='标签列表')
    licenses: list[SoftwareFacetItemModel] = Field(default_factory=list, description='许可证列表')
    authors: list[SoftwareFacetItemModel] = Field(default_factory=list, description='作者列表')
    teams: list[SoftwareFacetItemModel] = Field(default_factory=list, description='团队/组织列表')
    platforms: list[SoftwareFacetItemModel] = Field(default_factory=list, description='平台列表（存在下载配置）')

