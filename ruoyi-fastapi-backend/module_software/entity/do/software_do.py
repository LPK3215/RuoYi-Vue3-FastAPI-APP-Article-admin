from datetime import datetime

from sqlalchemy import CHAR, BigInteger, Column, DateTime, Integer, String, Text

from config.database import Base
from config.env import DataBaseConfig
from utils.common_util import SqlalchemyUtil


class ToolSoftwareCategory(Base):
    """
    软件分类表
    """

    __tablename__ = 'tool_software_category'
    __table_args__ = {'comment': '软件分类表'}

    category_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='分类ID')
    category_code = Column(
        String(64),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='分类编码',
    )
    category_name = Column(String(100), nullable=False, comment='分类名称')
    category_sort = Column(Integer, nullable=True, server_default='0', comment='显示顺序')
    status = Column(CHAR(1), nullable=True, server_default='0', comment='状态（0正常 1停用）')
    del_flag = Column(CHAR(1), nullable=True, server_default='0', comment='删除标志（0代表存在 2代表删除）')
    create_by = Column(String(64), nullable=True, server_default="''", comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_by = Column(String(64), nullable=True, server_default="''", comment='更新者')
    update_time = Column(DateTime, nullable=True, default=datetime.now, comment='更新时间')
    remark = Column(
        String(500),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='备注',
    )


class ToolSoftware(Base):
    """
    软件信息表
    """

    __tablename__ = 'tool_software'
    __table_args__ = {'comment': '软件信息表'}

    software_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='软件ID')
    category_id = Column(BigInteger, nullable=True, comment='分类ID')
    software_name = Column(String(200), nullable=False, comment='软件名称')
    short_desc = Column(
        String(500),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='简短描述',
    )
    icon_url = Column(
        String(500),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='图标URL',
    )
    official_url = Column(
        String(500),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='官网地址',
    )
    repo_url = Column(
        String(500),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='开源地址/仓库地址',
    )
    author = Column(
        String(100),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='作者',
    )
    team = Column(
        String(100),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='团队/组织',
    )
    license = Column(
        String(128),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='许可证',
    )
    open_source = Column(CHAR(1), nullable=True, server_default='0', comment='是否开源（0否 1是）')
    tags = Column(
        String(500),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='标签（逗号分隔）',
    )
    description_md = Column(Text, nullable=True, comment='介绍（Markdown）')
    usage_md = Column(Text, nullable=True, comment='使用说明（Markdown）')
    publish_status = Column(CHAR(1), nullable=True, server_default='0', comment='发布状态（0草稿 1上架 2下架）')
    software_sort = Column(Integer, nullable=True, server_default='0', comment='显示顺序')
    status = Column(CHAR(1), nullable=True, server_default='0', comment='状态（0正常 1停用）')
    del_flag = Column(CHAR(1), nullable=True, server_default='0', comment='删除标志（0代表存在 2代表删除）')
    create_by = Column(String(64), nullable=True, server_default="''", comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_by = Column(String(64), nullable=True, server_default="''", comment='更新者')
    update_time = Column(DateTime, nullable=True, default=datetime.now, comment='更新时间')
    remark = Column(
        String(500),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='备注',
    )


class ToolSoftwareDownload(Base):
    """
    软件多平台下载配置表
    """

    __tablename__ = 'tool_software_download'
    __table_args__ = {'comment': '软件多平台下载配置表'}

    download_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='下载ID')
    software_id = Column(BigInteger, nullable=False, comment='软件ID')
    platform = Column(String(32), nullable=False, comment='平台标识（windows/mac/linux/android/ios/web/other等）')
    download_url = Column(String(500), nullable=False, comment='下载地址')
    version = Column(
        String(64),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='版本',
    )
    checksum = Column(
        String(128),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='校验值（可选）',
    )
    sort = Column(Integer, nullable=True, server_default='0', comment='显示顺序')
    remark = Column(
        String(500),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='备注',
    )
    create_time = Column(DateTime, nullable=True, default=datetime.now, comment='创建时间')


class ToolSoftwareResource(Base):
    """
    软件资源表（截图/文档/链接等，当前仅存 URL）
    """

    __tablename__ = 'tool_software_resource'
    __table_args__ = {'comment': '软件资源表'}

    resource_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='资源ID')
    software_id = Column(BigInteger, nullable=False, comment='软件ID')
    resource_type = Column(String(32), nullable=False, comment='资源类型（screenshot/doc/link/video/other等）')
    title = Column(
        String(200),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='标题',
    )
    resource_url = Column(String(500), nullable=False, comment='资源URL')
    sort = Column(Integer, nullable=True, server_default='0', comment='显示顺序')
    remark = Column(
        String(500),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='备注',
    )
    create_time = Column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
