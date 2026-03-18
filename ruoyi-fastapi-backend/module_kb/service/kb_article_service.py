import json
from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_kb.dao.kb_article_dao import ToolKbArticleDao, ToolKbArticleSoftwareDao, ToolKbArticleTagDao
from module_kb.dao.kb_category_dao import ToolKbCategoryDao
from module_kb.entity.do.kb_article_do import ToolKbTag
from module_kb.entity.vo.kb_article_vo import (
    DeleteToolKbArticleModel,
    ToolKbArticleModel,
    ToolKbArticlePageQueryModel,
    ToolKbArticlePublishStatusModel,
)
from module_kb.service.kb_tag_service import ToolKbTagService
from utils.common_util import CamelCaseUtil

MAX_KB_TAGS_LENGTH = 500
MAX_KB_ATTACHMENTS_LENGTH = 4000


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
    def _normalize_tag_text(cls, tag_names: list[str]) -> str | None:
        if not tag_names:
            return None
        norm = ','.join([name for name in tag_names if name])
        if not norm:
            return None
        if len(norm) > MAX_KB_TAGS_LENGTH:
            raise ServiceException(message=f'标签长度不能超过 {MAX_KB_TAGS_LENGTH} 个字符')
        return norm

    @classmethod
    def _build_tag_payload(cls, tags: list[ToolKbTag]) -> tuple[list[int], list[dict[str, Any]], str | None]:
        if not tags:
            return [], [], None
        tag_list = [{'tagId': int(tag.tag_id), 'tagName': str(tag.tag_name)} for tag in tags]
        tag_ids = [int(tag.tag_id) for tag in tags]
        tags_text = cls._normalize_tag_text([str(tag.tag_name) for tag in tags])
        return tag_ids, tag_list, tags_text

    @classmethod
    def _normalize_attachments(cls, raw: str | None) -> str | None:
        """附件存储为 JSON 字符串；这里做基本清洗与长度限制。"""
        text = (raw or '').strip()
        if not text:
            return None
        # 允许前端直接传 /common/upload 返回的 fileName 列表，这里只接受 JSON list
        try:
            data = json.loads(text)
        except Exception as exc:
            raise ServiceException(message='附件格式不合法（需为 JSON）') from exc

        if not isinstance(data, list):
            raise ServiceException(message='附件格式不合法（需为数组）')

        cleaned: list[dict[str, Any]] = []
        for item in data:
            if not isinstance(item, dict):
                continue
            name = str(item.get('name') or '').strip()
            url = str(item.get('url') or '').strip()
            if not name or not url:
                continue
            size = item.get('size')
            try:
                size_int = int(size) if size is not None else None
            except Exception:
                size_int = None
            cleaned.append({'name': name[:200], 'url': url[:500], 'size': size_int})

        if not cleaned:
            return None

        out = json.dumps(cleaned, ensure_ascii=False)
        if len(out) > MAX_KB_ATTACHMENTS_LENGTH:
            raise ServiceException(message=f'附件信息过长（最多 {MAX_KB_ATTACHMENTS_LENGTH} 字符）')
        return out

    @classmethod
    async def _resolve_article_tags(
        cls, query_db: AsyncSession, article: ToolKbArticleModel
    ) -> tuple[list[int], list[dict[str, Any]], str | None]:
        tag_names = cls._split_tags(article.tags or '')
        if tag_names:
            tags = await ToolKbTagService.ensure_tags_by_names_services(
                query_db, tag_names, operator_name=article.update_by or article.create_by
            )
            return cls._build_tag_payload(tags)

        tag_ids = [int(tag_id) for tag_id in dict.fromkeys(article.tag_ids or []) if int(tag_id) > 0]
        if not tag_ids:
            return [], [], None
        tags = await ToolKbTagService.get_tags_by_ids_services(query_db, tag_ids)
        if len(tags) != len(tag_ids):
            raise ServiceException(message='部分标签不存在')
        return cls._build_tag_payload(tags)

    @classmethod
    async def _get_article_tag_mapping(cls, query_db: AsyncSession, article_ids: list[int]) -> dict[int, list[dict[str, Any]]]:
        unique_ids = [int(article_id) for article_id in dict.fromkeys(article_ids or []) if int(article_id) > 0]
        if not unique_ids:
            return {}
        return await ToolKbArticleTagDao.get_tags_by_article_ids(query_db, unique_ids)

    @classmethod
    def _compose_article_row(cls, row: Any, article_tags_map: dict[int, list[dict[str, Any]]]) -> dict[str, Any]:
        article = row[0] if isinstance(row, (list, tuple)) and len(row) > 0 else row
        category = row[1] if isinstance(row, (list, tuple)) and len(row) > 1 else {}
        article = article or {}
        category = category or {}
        article_id = int(article.get('articleId') or 0)
        tag_list = article_tags_map.get(article_id, [])
        tags_text = cls._normalize_tag_text([str(item.get('tagName') or '') for item in tag_list]) or article.get('tags')
        return {
            **article,
            'categoryName': category.get('categoryName') if isinstance(category, dict) else None,
            'tagIds': [int(item.get('tagId')) for item in tag_list if item.get('tagId') is not None],
            'tagList': tag_list,
            'tags': tags_text,
        }

    @classmethod
    async def get_article_list_services(
        cls, query_db: AsyncSession, query_object: ToolKbArticlePageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict]:
        query_result = await ToolKbArticleDao.get_article_list(query_db, query_object, is_page=is_page)
        if is_page:
            article_ids = []
            for row in query_result.rows:
                article = row[0] if isinstance(row, (list, tuple)) and row else {}
                if isinstance(article, dict) and article.get('articleId'):
                    article_ids.append(int(article.get('articleId')))
            article_tags_map = await cls._get_article_tag_mapping(query_db, article_ids)
            return PageModel[ToolKbArticleModel](
                **{
                    **query_result.model_dump(by_alias=True),
                    'rows': [cls._compose_article_row(row, article_tags_map) for row in query_result.rows],
                }
            )

        if not query_result:
            return []
        article_ids = []
        for row in query_result:
            article = row[0] if isinstance(row, (list, tuple)) and row else {}
            if isinstance(article, dict) and article.get('articleId'):
                article_ids.append(int(article.get('articleId')))
        article_tags_map = await cls._get_article_tag_mapping(query_db, article_ids)
        return [cls._compose_article_row(row, article_tags_map) for row in query_result]

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
        tag_map = await cls._get_article_tag_mapping(query_db, [article_id])
        tag_list = tag_map.get(article_id, [])
        payload = CamelCaseUtil.transform_result(article)
        payload['softwareIds'] = software_ids
        payload['categoryName'] = category_name
        payload['tagIds'] = [int(item.get('tagId')) for item in tag_list if item.get('tagId') is not None]
        payload['tagList'] = tag_list
        payload['tags'] = cls._normalize_tag_text([str(item.get('tagName') or '') for item in tag_list]) or article.tags
        payload['attachments'] = getattr(article, 'attachments', None)
        payload['articleType'] = getattr(article, 'article_type', None)
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
        tag_ids, _, tags_text = await cls._resolve_article_tags(query_db, article)
        article.tags = tags_text
        if 'attachments' in article.model_fields_set:
            article.attachments = cls._normalize_attachments(article.attachments)
        article.publish_status = article.publish_status or '0'
        article.status = article.status or '0'
        article.article_sort = int(article.article_sort or 0)
        now = datetime.now()
        if article.publish_status == '1' and not article.publish_time:
            article.publish_time = now
        try:
            db_article = await ToolKbArticleDao.add_article_dao(query_db, article)
            created_article_id = int(db_article.article_id)
            await ToolKbArticleSoftwareDao.replace_article_softwares(
                query_db, created_article_id, article.software_ids or []
            )
            await ToolKbArticleTagDao.replace_article_tags(query_db, created_article_id, tag_ids)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功', result={'articleId': created_article_id})
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def edit_article_services(cls, query_db: AsyncSession, article: ToolKbArticleModel) -> CrudResponseModel:
        if not article.article_id:
            raise ServiceException(message='缺少文章ID')
        article.validate_fields()
        if 'category_id' in article.model_fields_set:
            article.category_id = int(article.category_id) if int(article.category_id or 0) > 0 else None
            if article.category_id:
                category = await ToolKbCategoryDao.get_category_detail_by_id(query_db, int(article.category_id))
                if not category:
                    raise ServiceException(message='分类不存在')
        db_article = await ToolKbArticleDao.get_article_detail_by_id(query_db, article.article_id)
        if not db_article:
            raise ServiceException(message='文章不存在')

        payload = article.model_dump(
            exclude={'software_ids', 'tag_ids', 'tag_list', 'category_name'},
            exclude_unset=True,
            by_alias=False,
        )
        if 'attachments' in payload:
            payload['attachments'] = cls._normalize_attachments(payload.get('attachments'))
        should_update_tags = 'tags' in article.model_fields_set or 'tag_ids' in article.model_fields_set
        tag_ids: list[int] = []
        if should_update_tags:
            tag_ids, _, tags_text = await cls._resolve_article_tags(query_db, article)
            payload['tags'] = tags_text
        if payload.get('publish_status') == '1' and not payload.get('publish_time'):
            payload['publish_time'] = datetime.now()
        try:
            await ToolKbArticleDao.edit_article_dao(query_db, payload)
            if 'software_ids' in article.model_fields_set:
                await ToolKbArticleSoftwareDao.replace_article_softwares(
                    query_db, int(article.article_id), article.software_ids or []
                )
            if should_update_tags:
                await ToolKbArticleTagDao.replace_article_tags(query_db, int(article.article_id), tag_ids)
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
