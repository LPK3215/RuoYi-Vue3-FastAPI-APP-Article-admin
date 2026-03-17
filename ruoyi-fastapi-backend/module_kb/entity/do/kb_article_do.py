from datetime import datetime

from sqlalchemy import CHAR, BigInteger, Column, DateTime, Integer, String, Text

from config.database import Base
from config.env import DataBaseConfig
from utils.common_util import SqlalchemyUtil


class ToolKbArticle(Base):
    """
    教程文章表
    """

    __tablename__ = 'tool_kb_article'
    __table_args__ = {'comment': '教程文章表'}

    article_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='文章ID')
    category_id = Column(BigInteger, nullable=True, comment='分类ID')
    title = Column(String(200), nullable=False, comment='标题')
    summary = Column(
        String(500),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='摘要',
    )
    cover_url = Column(
        String(500),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='封面URL',
    )
    content_md = Column(Text, nullable=True, comment='正文（Markdown）')
    tags = Column(
        String(500),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='标签（逗号分隔）',
    )
    publish_status = Column(CHAR(1), nullable=True, server_default='0', comment='发布状态（0草稿 1发布 2下线）')
    publish_time = Column(DateTime, nullable=True, comment='发布时间')
    article_sort = Column(Integer, nullable=True, server_default='0', comment='显示顺序')
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


class ToolKbArticleSoftware(Base):
    """
    教程文章关联软件表
    """

    __tablename__ = 'tool_kb_article_software'
    __table_args__ = {'comment': '教程文章关联软件表'}

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='主键ID')
    article_id = Column(BigInteger, nullable=False, comment='文章ID')
    software_id = Column(BigInteger, nullable=False, comment='软件ID')
    sort = Column(Integer, nullable=True, server_default='0', comment='显示顺序')
    remark = Column(
        String(500),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='备注',
    )
    create_time = Column(DateTime, nullable=True, default=datetime.now, comment='创建时间')


class ToolKbCategory(Base):
    """
    教程分类表（扁平 + 预留 parent_id）
    """

    __tablename__ = 'tool_kb_category'
    __table_args__ = {'comment': '教程分类表'}

    category_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='分类ID')
    parent_id = Column(BigInteger, nullable=True, server_default='0', comment='父级ID（0为顶级）')
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
