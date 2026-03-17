from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_kb.dao.kb_article_dao import ToolKbArticleDao, ToolKbArticleSoftwareDao
from module_kb.dao.kb_category_dao import ToolKbCategoryDao
from module_kb.entity.vo.kb_article_vo import (
    DeleteToolKbArticleModel,
    ToolKbArticleModel,
    ToolKbArticlePageQueryModel,
    ToolKbArticlePublishStatusModel,
)

MAX_KB_TAGS_LENGTH = 500


class ToolKbArticleService:
    """
    教程文章模块服务层（管理端）
    """

    @staticmethod
    def _split_tags(tags: str) -> list[str]:
        raw = tags or ''
        raw = raw.replace('，', ',').replace('；', ',').replace(';', ',')
        raw = raw.replace('\r\n', ',').replace('\n', ',').replace('\r', ',').replace('\t', ',')
        parts = [p.strip() for p in raw.split(',')]
        seen: set[str] = set()
        result: list[str] = []
        for p in parts:
            if not p or p in seen:
                continue
            seen.add(p)
            result.append(p)
        return result

    @classmethod
    def _normalize_tags(cls, tags: str | None) -> str | None:
        if not tags:
            return None
        parts = cls._split_tags(tags)
        if not parts:
            return None
        norm = ','.join(parts)
        if len(norm) > MAX_KB_TAGS_LENGTH:
            raise ServiceException(message=f'标签长度不能超过 {MAX_KB_TAGS_LENGTH} 个字符')
        return norm

    @classmethod
    async def get_article_list_services(
        cls, query_db: AsyncSession, query_object: ToolKbArticlePageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict]:
        query_result = await ToolKbArticleDao.get_article_list(query_db, query_object, is_page=is_page)
        if is_page:
            return PageModel[ToolKbArticleModel](
                **{
                    **query_result.model_dump(by_alias=True),
                    'rows': [
                        {
                            **(row[0] or {}),
                            'categoryName': (row[1] or {}).get('categoryName') if isinstance(row[1], dict) else None,
                        }
                        for row in query_result.rows
                    ],
                }
            )

        if not query_result:
            return []
        return [
            {**(row[0] or {}), 'categoryName': (row[1] or {}).get('categoryName') if isinstance(row[1], dict) else None}
            for row in query_result
        ]

    @classmethod
    async def article_detail_services(cls, query_db: AsyncSession, article_id: int) -> ToolKbArticleModel:
        article = await ToolKbArticleDao.get_article_detail_by_id(query_db, article_id)
        if not article:
            raise ServiceException(message='文章不存在')
        software_ids = await ToolKbArticleSoftwareDao.get_software_ids_by_article_id(query_db, article_id)
        category_name: str | None = None
        if article.category_id:
            category = await ToolKbCategoryDao.get_category_detail_by_id(query_db, int(article.category_id))
            if category:
                category_name = str(category.category_name)
        payload = ToolKbArticleModel.model_validate(article).model_dump(by_alias=True)
        payload['softwareIds'] = software_ids
        payload['categoryName'] = category_name
        return ToolKbArticleModel(**payload)

    @classmethod
    async def add_article_services(cls, query_db: AsyncSession, article: ToolKbArticleModel) -> CrudResponseModel:
        article.validate_fields()
        if article.category_id is not None:
            article.category_id = int(article.category_id) if int(article.category_id or 0) > 0 else None
            if article.category_id:
                category = await ToolKbCategoryDao.get_category_detail_by_id(query_db, int(article.category_id))
                if not category:
                    raise ServiceException(message='分类不存在')
        article.tags = cls._normalize_tags(article.tags)
        article.publish_status = article.publish_status or '0'
        article.status = article.status or '0'
        article.article_sort = int(article.article_sort or 0)
        now = datetime.now()
        if article.publish_status == '1' and not article.publish_time:
            article.publish_time = now
        try:
            db_article = await ToolKbArticleDao.add_article_dao(query_db, article)
            await ToolKbArticleSoftwareDao.replace_article_softwares(
                query_db, db_article.article_id, article.software_ids or []
            )
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功', result={'articleId': int(db_article.article_id)})
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def edit_article_services(cls, query_db: AsyncSession, article: ToolKbArticleModel) -> CrudResponseModel:
        if not article.article_id:
            raise ServiceException(message='缺少文章ID')
        article.validate_fields()
        if article.category_id is not None:
            article.category_id = int(article.category_id) if int(article.category_id or 0) > 0 else None
            if article.category_id:
                category = await ToolKbCategoryDao.get_category_detail_by_id(query_db, int(article.category_id))
                if not category:
                    raise ServiceException(message='分类不存在')
        db_article = await ToolKbArticleDao.get_article_detail_by_id(query_db, article.article_id)
        if not db_article:
            raise ServiceException(message='文章不存在')

        payload = article.model_dump(exclude={'software_ids'}, exclude_none=True, by_alias=False)
        payload['tags'] = cls._normalize_tags(article.tags)
        if payload.get('publish_status') == '1' and not payload.get('publish_time'):
            payload['publish_time'] = datetime.now()
        try:
            await ToolKbArticleDao.edit_article_dao(query_db, payload)
            await ToolKbArticleSoftwareDao.replace_article_softwares(
                query_db, int(article.article_id), article.software_ids or []
            )
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='更新成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def delete_article_services(
        cls, query_db: AsyncSession, page_object: DeleteToolKbArticleModel, update_by: str
    ) -> CrudResponseModel:
        if not page_object.article_ids:
            raise ServiceException(message='传入文章id为空')
        ids = [x.strip() for x in (page_object.article_ids or '').split(',') if x.strip()]
        if not ids:
            raise ServiceException(message='传入文章id为空')
        update_time = datetime.now()
        try:
            for raw in ids:
                article_id = int(raw)
                current = await ToolKbArticleDao.get_article_detail_by_id(query_db, article_id)
                if not current:
                    raise ServiceException(message='文章不存在')
                await ToolKbArticleDao.delete_article_dao(
                    query_db, article_id, update_by=update_by, update_time=update_time
                )
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='删除成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def change_publish_status_services(
        cls, query_db: AsyncSession, page_object: ToolKbArticlePublishStatusModel, update_by: str
    ) -> CrudResponseModel:
        article = await ToolKbArticleDao.get_article_detail_by_id(query_db, page_object.article_id)
        if not article:
            raise ServiceException(message='文章不存在')

        update_time = datetime.now()
        payload = {
            'article_id': int(page_object.article_id),
            'publish_status': page_object.publish_status,
            'update_by': update_by,
            'update_time': update_time,
        }
        if page_object.publish_status == '1':
            payload['publish_time'] = update_time
        try:
            await ToolKbArticleDao.edit_article_dao(query_db, payload)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='更新成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc
