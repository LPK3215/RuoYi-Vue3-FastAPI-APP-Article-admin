from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank, Size


class ToolKbCategoryModel(BaseModel):
    """
    教程分类表对应 pydantic 模型（管理端）
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    category_id: int | None = Field(default=None, description='分类ID')
    parent_id: int | None = Field(default=0, description='父级ID（0为顶级）')
    category_code: str | None = Field(default=None, description='分类编码')
    category_name: str | None = Field(default=None, description='分类名称')
    category_sort: int | None = Field(default=None, description='显示顺序')
    status: Literal['0', '1'] | None = Field(default=None, description='状态（0正常 1停用）')
    del_flag: Literal['0', '2'] | None = Field(default=None, description='删除标志（0代表存在 2代表删除）')
    create_by: str | None = Field(default=None, description='创建者')
    create_time: datetime | None = Field(default=None, description='创建时间')
    update_by: str | None = Field(default=None, description='更新者')
    update_time: datetime | None = Field(default=None, description='更新时间')
    remark: str | None = Field(default=None, description='备注')

    @NotBlank(field_name='category_name', message='分类名称不能为空')
    @Size(field_name='category_name', min_length=0, max_length=100, message='分类名称长度不能超过100个字符')
    def get_category_name(self) -> str | None:
        return self.category_name

    @Size(field_name='category_code', min_length=0, max_length=64, message='分类编码长度不能超过64个字符')
    def get_category_code(self) -> str | None:
        return self.category_code

    @NotBlank(field_name='category_sort', message='显示顺序不能为空')
    def get_category_sort(self) -> int | None:
        return self.category_sort

    def validate_fields(self) -> None:
        self.get_category_name()
        self.get_category_code()
        self.get_category_sort()


class ToolKbCategoryQueryModel(ToolKbCategoryModel):
    """
    教程分类不分页查询模型
    """


class ToolKbCategoryPageQueryModel(ToolKbCategoryQueryModel):
    """
    教程分类分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteToolKbCategoryModel(BaseModel):
    """
    删除教程分类模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    category_ids: str = Field(description='需要删除的分类ID')


class ToolKbCategoryOptionModel(BaseModel):
    """
    教程分类下拉选项模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    category_id: int = Field(description='分类ID')
    category_name: str = Field(description='分类名称')

