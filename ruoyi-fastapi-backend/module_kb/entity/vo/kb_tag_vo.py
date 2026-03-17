from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank, Size


class ToolKbTagModel(BaseModel):
    """
    教程标签表对应 pydantic 模型（管理端）
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    tag_id: int | None = Field(default=None, description='标签ID')
    tag_code: str | None = Field(default=None, description='标签编码')
    tag_name: str | None = Field(default=None, description='标签名称')
    tag_sort: int | None = Field(default=None, description='显示顺序')
    status: Literal['0', '1'] | None = Field(default=None, description='状态（0正常 1停用）')
    del_flag: Literal['0', '2'] | None = Field(default=None, description='删除标志（0代表存在 2代表删除）')
    create_by: str | None = Field(default=None, description='创建者')
    create_time: datetime | None = Field(default=None, description='创建时间')
    update_by: str | None = Field(default=None, description='更新者')
    update_time: datetime | None = Field(default=None, description='更新时间')
    remark: str | None = Field(default=None, description='备注')

    @NotBlank(field_name='tag_name', message='标签名称不能为空')
    @Size(field_name='tag_name', min_length=0, max_length=100, message='标签名称长度不能超过100个字符')
    def get_tag_name(self) -> str | None:
        return self.tag_name

    @Size(field_name='tag_code', min_length=0, max_length=64, message='标签编码长度不能超过64个字符')
    def get_tag_code(self) -> str | None:
        return self.tag_code

    @NotBlank(field_name='tag_sort', message='显示顺序不能为空')
    def get_tag_sort(self) -> int | None:
        return self.tag_sort

    def validate_fields(self) -> None:
        self.get_tag_name()
        self.get_tag_code()
        self.get_tag_sort()


class ToolKbTagQueryModel(ToolKbTagModel):
    """
    教程标签不分页查询模型
    """


class ToolKbTagPageQueryModel(ToolKbTagQueryModel):
    """
    教程标签分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteToolKbTagModel(BaseModel):
    """
    删除教程标签模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    tag_ids: str = Field(description='需要删除的标签ID，多个用逗号分隔')


class ToolKbTagOptionModel(BaseModel):
    """
    教程标签下拉选项模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    tag_id: int = Field(description='标签ID')
    tag_name: str = Field(description='标签名称')

