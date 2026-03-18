from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class LocalInstalledSoftwareModel(BaseModel):
    """本机已安装软件信息（扫描结果）。"""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: str = Field(description='唯一标识（registry path）')
    name: str = Field(description='软件名称')
    version: str | None = Field(default=None, description='版本')
    publisher: str | None = Field(default=None, description='发布者/厂商')
    install_location: str | None = Field(default=None, description='安装路径')
    icon_path: str | None = Field(default=None, description='图标路径（可能为 exe/ico）')
    url: str | None = Field(default=None, description='官网/介绍链接')
    uninstall_string: str | None = Field(default=None, description='卸载命令')
    scope: str | None = Field(default=None, description='来源范围（HKLM/HKCU/WOW6432）')


class LocalSoftwareScanImportRequestModel(BaseModel):
    """导入本机扫描结果请求。"""

    model_config = ConfigDict(alias_generator=to_camel)

    ids: list[str] | None = Field(default=None, description='要导入的扫描ID列表；为空则导入全部')
    category_id: int | None = Field(default=None, description='导入到的软件分类ID；为空则自动创建/使用默认分类')
    update_support: bool = Field(default=False, description='遇到同名软件是否更新')
    overwrite: bool = Field(default=False, description='更新时是否覆盖已有字段（默认仅补齐空字段）')


class LocalSoftwareScanImportResultModel(BaseModel):
    """导入结果摘要。"""

    model_config = ConfigDict(alias_generator=to_camel)

    scanned: int = Field(default=0, description='扫描到的软件数量')
    selected: int = Field(default=0, description='选中的软件数量')
    created: int = Field(default=0, description='新增数量')
    updated: int = Field(default=0, description='更新数量')
    skipped: int = Field(default=0, description='跳过数量')
    errors: int = Field(default=0, description='失败数量')
    error_samples: list[str] = Field(default_factory=list, description='错误示例（最多10条）')


class LocalSoftwareScanQueryModel(BaseModel):
    """扫描查询参数。"""

    model_config = ConfigDict(alias_generator=to_camel)

    keyword: str | None = Field(default=None, description='关键字（名称/发布者/版本）')
    limit: int = Field(default=500, description='最多返回数量（默认500，最大3000）')
