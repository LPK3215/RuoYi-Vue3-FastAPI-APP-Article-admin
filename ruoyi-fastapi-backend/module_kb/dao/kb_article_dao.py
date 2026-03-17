from typing import Any

from sqlalchemy import and_, delete, desc, exists, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_kb.entity.do.kb_article_do import (
    ToolKbArticle,
    ToolKbArticleSoftware,
    ToolKbArticleTag,
    ToolKbCategory,
    ToolKbTag,
)
from module_kb.entity.vo.kb_article_vo import ToolKbArticleModel, ToolKbArticlePageQueryModel
from utils.common_util import CamelCaseUtil
from utils.page_util import PageUtil


class ToolKbArticleDao:
    """
    教程文章模块数据库操作层（管理端）
    """

    @classmethod
    async def get_article_detail_by_id(cls, db: AsyncSession, article_id: int) -> ToolKbArticle | None:
        article = (
            (
                await db.execute(
                    select(ToolKbArticle).where(ToolKbArticle.article_id == article_id, ToolKbArticle.del_flag == '0')
                )
            )
            .scalars()
            .first()
        )
        return article

    @classmethod
    async def get_article_list(
        cls, db: AsyncSession, query_object: ToolKbArticlePageQueryModel, is_page: bool = False
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
            select(ToolKbArticle, ToolKbCategory)
            .select_from(ToolKbArticle)
            .where(
                ToolKbArticle.del_flag == '0',
                or_(
                    ToolKbArticle.title.like(f'%{keyword}%'),
                    ToolKbArticle.summary.like(f'%{keyword}%'),
                )
                if keyword
                else True,
                ToolKbArticle.category_id == query_object.category_id if query_object.category_id else True,
                ToolKbArticle.article_type == query_object.article_type if query_object.article_type else True,
                tag_filter_clause,
                ToolKbArticle.publish_status == query_object.publish_status if query_object.publish_status else True,
                ToolKbArticle.status == query_object.status if query_object.status else True,
            )
            .join(
                ToolKbCategory,
                and_(
                    ToolKbArticle.category_id == ToolKbCategory.category_id,
                    ToolKbCategory.del_flag == '0',
                ),
                isouter=True,
            )
            .order_by(desc(ToolKbArticle.article_sort), desc(ToolKbArticle.update_time), desc(ToolKbArticle.article_id))
            .distinct()
        )

        return await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page=is_page)

    @classmethod
    async def add_article_dao(cls, db: AsyncSession, article: ToolKbArticleModel) -> ToolKbArticle:
        payload = article.model_dump(
            exclude={'article_id', 'software_ids', 'tag_ids', 'tag_list', 'category_name'},
            exclude_none=True,
            by_alias=False,
        )
        db_article = ToolKbArticle(**payload)
        db.add(db_article)
        await db.flush()
        return db_article

    @classmethod
    async def edit_article_dao(cls, db: AsyncSession, article: dict) -> None:
        await db.execute(update(ToolKbArticle), [article])

    @classmethod
    async def delete_article_dao(cls, db: AsyncSession, article_id: int, update_by: str, update_time: Any) -> None:
        await db.execute(
            update(ToolKbArticle)
            .where(ToolKbArticle.article_id == article_id)
            .values(del_flag='2', update_by=update_by, update_time=update_time)
        )


class ToolKbArticleSoftwareDao:
    """
    教程文章-软件关联数据库操作层（管理端）
    """

    @classmethod
    async def get_software_ids_by_article_id(cls, db: AsyncSession, article_id: int) -> list[int]:
        rows = (
            (
                await db.execute(
                    select(ToolKbArticleSoftware.software_id)
                    .where(ToolKbArticleSoftware.article_id == article_id)
                    .order_by(ToolKbArticleSoftware.sort, ToolKbArticleSoftware.id)
                )
            )
            .scalars()
            .all()
        )
        return [int(x) for x in (rows or [])]

    @classmethod
    async def replace_article_softwares(cls, db: AsyncSession, article_id: int, software_ids: list[int]) -> None:
        await db.execute(delete(ToolKbArticleSoftware).where(ToolKbArticleSoftware.article_id == article_id))
        if not software_ids:
            return
        items = [
            ToolKbArticleSoftware(article_id=article_id, software_id=int(sid), sort=index)
            for index, sid in enumerate(software_ids)
        ]
        db.add_all(items)
        await db.flush()


class ToolKbArticleTagDao:
    """
    教程文章-标签关联数据库操作层（管理端）
    """

    @classmethod
    async def get_tag_ids_by_article_id(cls, db: AsyncSession, article_id: int) -> list[int]:
        rows = (
            (
                await db.execute(
                    select(ToolKbArticleTag.tag_id)
                    .where(ToolKbArticleTag.article_id == article_id)
                    .order_by(ToolKbArticleTag.sort, ToolKbArticleTag.id)
                )
            )
            .scalars()
            .all()
        )
        return [int(x) for x in (rows or [])]

    @classmethod
    async def get_tags_by_article_ids(cls, db: AsyncSession, article_ids: list[int]) -> dict[int, list[dict[str, Any]]]:
        if not article_ids:
            return {}
        rows = (
            await db.execute(
                select(
                    ToolKbArticleTag.article_id.label('article_id'),
                    ToolKbTag.tag_id.label('tag_id'),
                    ToolKbTag.tag_name.label('tag_name'),
                )
                .select_from(ToolKbArticleTag)
                .join(
                    ToolKbTag,
                    and_(
                        ToolKbTag.tag_id == ToolKbArticleTag.tag_id,
                        ToolKbTag.del_flag == '0',
                    ),
                )
                .where(ToolKbArticleTag.article_id.in_(article_ids))
                .order_by(ToolKbArticleTag.sort, ToolKbArticleTag.id, ToolKbTag.tag_sort, ToolKbTag.tag_id)
            )
        ).all()
        result: dict[int, list[dict[str, Any]]] = {int(article_id): [] for article_id in article_ids}
        for row in rows or []:
            item = CamelCaseUtil.transform_result(row)
            article_id = int(item.get('articleId'))
            result.setdefault(article_id, []).append(
                {
                    'tagId': item.get('tagId'),
                    'tagName': item.get('tagName'),
                }
            )
        return result

    @classmethod
    async def replace_article_tags(cls, db: AsyncSession, article_id: int, tag_ids: list[int]) -> None:
        await db.execute(delete(ToolKbArticleTag).where(ToolKbArticleTag.article_id == article_id))
        if not tag_ids:
            return
        items = [ToolKbArticleTag(article_id=article_id, tag_id=int(tag_id), sort=index) for index, tag_id in enumerate(tag_ids)]
        db.add_all(items)
        await db.flush()
