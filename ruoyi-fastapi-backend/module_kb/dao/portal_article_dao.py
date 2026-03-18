from typing import Any

from sqlalchemy import and_, desc, exists, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_kb.entity.do.kb_article_do import (
    ToolKbArticle,
    ToolKbArticleSoftware,
    ToolKbArticleTag,
    ToolKbCategory,
    ToolKbTag,
)
from module_kb.entity.vo.portal_article_vo import PortalArticlePageQueryModel
from module_software.entity.do.software_do import ToolSoftware, ToolSoftwareCategory
from utils.common_util import CamelCaseUtil
from utils.page_util import PageUtil

DEFAULT_TAG_LIMIT = 50
MAX_TAG_LIMIT = 200


class PortalArticleDao:
    """
    用户端：教程文章数据库操作层（仅查询发布数据）
    """

    @classmethod
    async def get_category_list(cls, db: AsyncSession) -> list[dict[str, Any]]:
        """
        获取用户端教程分类列表（仅正常且未删除），并附带已发布文章数量。

        仅返回“有已发布文章”的分类，避免用户端出现空分类。
        """
        query = (
            select(
                ToolKbCategory.category_id.label('category_id'),
                ToolKbCategory.category_code.label('category_code'),
                ToolKbCategory.category_name.label('category_name'),
                func.count(ToolKbArticle.article_id).label('article_count'),
            )
            .select_from(ToolKbCategory)
            .join(
                ToolKbArticle,
                and_(
                    ToolKbArticle.category_id == ToolKbCategory.category_id,
                    ToolKbArticle.del_flag == '0',
                    ToolKbArticle.status == '0',
                    ToolKbArticle.publish_status == '1',
                ),
                isouter=True,
            )
            .where(ToolKbCategory.del_flag == '0', ToolKbCategory.status == '0')
            .group_by(
                ToolKbCategory.category_id,
                ToolKbCategory.category_code,
                ToolKbCategory.category_name,
                ToolKbCategory.category_sort,
            )
            .having(func.count(ToolKbArticle.article_id) > 0)
            .order_by(ToolKbCategory.category_sort, ToolKbCategory.category_id)
        )
        rows = (await db.execute(query)).mappings().all()
        return CamelCaseUtil.transform_result([dict(row) for row in (rows or [])])

    @classmethod
    async def get_tag_list(cls, db: AsyncSession, limit: int = 50) -> list[dict[str, Any]]:
        """获取用户端教程标签列表（仅正常且未删除），并附带已发布文章数量。

        仅返回“有已发布文章”的标签，避免用户端出现空标签。
        """
        safe_limit = int(limit or 0)
        if safe_limit <= 0:
            safe_limit = DEFAULT_TAG_LIMIT
        safe_limit = min(MAX_TAG_LIMIT, safe_limit)

        query = (
            select(
                ToolKbTag.tag_id.label('tag_id'),
                ToolKbTag.tag_name.label('tag_name'),
                func.count(ToolKbArticle.article_id).label('article_count'),
            )
            .select_from(ToolKbTag)
            .join(
                ToolKbArticleTag,
                ToolKbArticleTag.tag_id == ToolKbTag.tag_id,
                isouter=True,
            )
            .join(
                ToolKbArticle,
                and_(
                    ToolKbArticle.article_id == ToolKbArticleTag.article_id,
                    ToolKbArticle.del_flag == '0',
                    ToolKbArticle.status == '0',
                    ToolKbArticle.publish_status == '1',
                ),
                isouter=True,
            )
            .where(ToolKbTag.del_flag == '0', ToolKbTag.status == '0')
            .group_by(ToolKbTag.tag_id, ToolKbTag.tag_name, ToolKbTag.tag_sort)
            .having(func.count(ToolKbArticle.article_id) > 0)
            .order_by(func.count(ToolKbArticle.article_id).desc(), ToolKbTag.tag_sort, ToolKbTag.tag_id)
            .limit(safe_limit)
        )
        rows = (await db.execute(query)).mappings().all()
        return CamelCaseUtil.transform_result([dict(row) for row in (rows or [])])

    @classmethod
    async def get_article_detail_by_id(cls, db: AsyncSession, article_id: int) -> ToolKbArticle | None:
        article = (
            (
                await db.execute(
                    select(ToolKbArticle).where(
                        ToolKbArticle.article_id == article_id,
                        ToolKbArticle.del_flag == '0',
                        ToolKbArticle.status == '0',
                        ToolKbArticle.publish_status == '1',
                    )
                )
            )
            .scalars()
            .first()
        )
        return article

    @classmethod
    async def get_article_list(
        cls, db: AsyncSession, query_object: PortalArticlePageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        keyword = (query_object.keyword or '').strip()
        tag = (query_object.tag or '').strip()
        relation_tag_clause = (
            exists(
                select(ToolKbArticleTag.id)
                .select_from(ToolKbArticleTag)
                .join(
                    ToolKbTag,
                    and_(
                        ToolKbTag.tag_id == ToolKbArticleTag.tag_id,
                        ToolKbTag.del_flag == '0',
                    ),
                )
                .where(
                    ToolKbArticleTag.article_id == ToolKbArticle.article_id,
                    ToolKbArticleTag.tag_id == query_object.tag_id if query_object.tag_id else True,
                    ToolKbTag.tag_name.like(f'%{tag}%') if tag else True,
                )
            )
            if query_object.tag_id or tag
            else True
        )
        tag_filter_clause = relation_tag_clause
        if tag and not query_object.tag_id:
            tag_filter_clause = or_(relation_tag_clause, ToolKbArticle.tags.like(f'%{tag}%'))
        query = (
            select(ToolKbArticle)
            .select_from(ToolKbArticle)
            .where(
                ToolKbArticle.del_flag == '0',
                ToolKbArticle.status == '0',
                ToolKbArticle.publish_status == '1',
                or_(
                    ToolKbArticle.title.like(f'%{keyword}%'),
                    ToolKbArticle.summary.like(f'%{keyword}%'),
                )
                if keyword
                else True,
                ToolKbArticle.category_id == query_object.category_id if query_object.category_id else True,
                ToolKbArticle.article_type == query_object.article_type if query_object.article_type else True,
                tag_filter_clause,
            )
            .order_by(desc(ToolKbArticle.article_sort), desc(ToolKbArticle.publish_time), desc(ToolKbArticle.article_id))
            .distinct()
        )

        if query_object.software_id:
            query = query.join(
                ToolKbArticleSoftware, ToolKbArticleSoftware.article_id == ToolKbArticle.article_id
            ).where(ToolKbArticleSoftware.software_id == query_object.software_id)

        return await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page=is_page)

    @classmethod
    async def get_related_softwares(cls, db: AsyncSession, article_id: int) -> list[list[dict[str, Any]]]:
        query = (
            select(ToolSoftware, ToolSoftwareCategory)
            .select_from(ToolKbArticleSoftware)
            .join(ToolSoftware, ToolSoftware.software_id == ToolKbArticleSoftware.software_id)
            .outerjoin(ToolSoftwareCategory, ToolSoftwareCategory.category_id == ToolSoftware.category_id)
            .where(
                ToolKbArticleSoftware.article_id == article_id,
                ToolSoftware.del_flag == '0',
                ToolSoftware.status == '0',
                ToolSoftware.publish_status == '1',
            )
            .order_by(ToolKbArticleSoftware.sort, ToolKbArticleSoftware.id)
        )
        rows = await PageUtil.paginate(db, query, 1, 9999, is_page=False)
        if not rows:
            return []
        return rows  # 每行是 [softwareDict, categoryDict]
