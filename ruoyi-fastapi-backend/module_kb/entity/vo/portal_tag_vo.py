from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class PortalTagItemModel(BaseModel):
    """用户端：标签项（带文章数量）"""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    tag_id: int = Field(description='标签ID')
    tag_name: str = Field(description='标签名称')
    article_count: int = Field(default=0, description='已发布文章数量')

