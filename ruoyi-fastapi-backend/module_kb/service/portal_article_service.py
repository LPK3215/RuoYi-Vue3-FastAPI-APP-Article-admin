from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from exceptions.exception import ServiceException
from module_kb.dao.kb_article_dao import ToolKbArticleTagDao
from module_kb.dao.portal_article_dao import PortalArticleDao
from module_kb.entity.vo.portal_article_vo import (
    PortalArticleCategoryModel,
    PortalArticleDetailModel,
    PortalArticleListItemModel,
    PortalArticlePageQueryModel,
)
from module_software.entity.vo.portal_software_vo import PortalSoftwareListItemModel
from utils.common_util import CamelCaseUtil


class PortalArticleService:
    """
    用户端：教程文章服务层（仅查询发布数据）
    """

    @staticmethod
    def _normalize_tag_text(tag_names: list[str]) -> str | None:
        items = [str(name or '').strip() for name in tag_names if str(name or '').strip()]
        if not items:
            return None
        return ','.join(items)

    @classmethod
    async def _get_article_tag_mapping(cls, query_db: AsyncSession, article_ids: list[int]) -> dict[int, list[dict[str, Any]]]:
        unique_ids = [int(article_id) for article_id in dict.fromkeys(article_ids or []) if int(article_id) > 0]
        if not unique_ids:
            return {}
        return await ToolKbArticleTagDao.get_tags_by_article_ids(query_db, unique_ids)

    @classmethod
    def _compose_article_item(cls, article: dict[str, Any], article_tags_map: dict[int, list[dict[str, Any]]]) -> dict[str, Any]:
        article_id = int(article.get('articleId') or 0)
        tag_list = article_tags_map.get(article_id, [])
        tags_text = cls._normalize_tag_text([str(item.get('tagName') or '') for item in tag_list]) or article.get('tags')
        return {
            **article,
            'tagList': tag_list,
            'tags': tags_text,
        }

    @classmethod
    async def get_category_list_services(cls, query_db: AsyncSession) -> list[PortalArticleCategoryModel]:
        rows = await PortalArticleDao.get_category_list(query_db)
        if not rows:
            return []
        return [PortalArticleCategoryModel(**row) for row in rows]

    @classmethod
    async def get_article_list_services(
        cls, query_db: AsyncSession, query_object: PortalArticlePageQueryModel, is_page: bool = False
    ) -> PageModel[PortalArticleListItemModel] | list[dict]:
        result = await PortalArticleDao.get_article_list(query_db, query_object, is_page=is_page)
        if not is_page:
            article_ids = [int(item.get('articleId')) for item in result or [] if item.get('articleId')]
            article_tags_map = await cls._get_article_tag_mapping(query_db, article_ids)
            return [cls._compose_article_item(item, article_tags_map) for item in result or []]
        article_ids = [int(item.get('articleId')) for item in result.rows or [] if item.get('articleId')]
        article_tags_map = await cls._get_article_tag_mapping(query_db, article_ids)
        return PageModel[PortalArticleListItemModel](
            **{
                **result.model_dump(by_alias=True),
                'rows': [cls._compose_article_item(item, article_tags_map) for item in result.rows or []],
            }
        )

    @classmethod
    async def article_detail_services(cls, query_db: AsyncSession, article_id: int) -> PortalArticleDetailModel:
        article = await PortalArticleDao.get_article_detail_by_id(query_db, article_id)
        if not article:
            raise ServiceException(message='文章不存在或未发布')

        rows = await PortalArticleDao.get_related_softwares(query_db, article_id)
        softwares: list[PortalSoftwareListItemModel] = []
        for row in rows or []:
            software = row[0] if isinstance(row, (list, tuple)) and len(row) > 0 else {}
            category = row[1] if isinstance(row, (list, tuple)) and len(row) > 1 else {}
            softwares.append(
                PortalSoftwareListItemModel(
                    **{
                        **(software or {}),
                        'categoryName': (category or {}).get('categoryName'),
                    }
                )
            )

        tag_map = await cls._get_article_tag_mapping(query_db, [article_id])
        tag_list = tag_map.get(article_id, [])
        payload = CamelCaseUtil.transform_result(article)
        payload['tagList'] = tag_list
        payload['tags'] = cls._normalize_tag_text([str(item.get('tagName') or '') for item in tag_list]) or article.tags
        payload['softwares'] = softwares
        return PortalArticleDetailModel(**payload)
