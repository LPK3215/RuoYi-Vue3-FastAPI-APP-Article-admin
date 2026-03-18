from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from common.constant import CommonConstant
from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_kb.dao.kb_tag_dao import ToolKbTagDao
from module_kb.entity.do.kb_article_do import ToolKbTag
from module_kb.entity.vo.kb_tag_vo import (
    DeleteToolKbTagModel,
    ToolKbTagModel,
    ToolKbTagOptionModel,
    ToolKbTagPageQueryModel,
)
from utils.common_util import CamelCaseUtil

MAX_TAG_NAME_LENGTH = 100


class ToolKbTagService:
    """
    教程标签模块服务层（管理端）
    """

    @staticmethod
    def _normalize_names(tag_names: list[str]) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        for raw_name in tag_names or []:
            name = str(raw_name or '').strip()
            if not name or name in seen:
                continue
            if len(name) > MAX_TAG_NAME_LENGTH:
                raise ServiceException(message=f'标签名称长度不能超过{MAX_TAG_NAME_LENGTH}个字符')
            seen.add(name)
            result.append(name)
        return result

    @classmethod
    async def get_tag_list_services(
        cls, query_db: AsyncSession, query_object: ToolKbTagPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict]:
        return await ToolKbTagDao.get_tag_list(query_db, query_object, is_page)

    @classmethod
    async def check_tag_name_unique_services(cls, query_db: AsyncSession, page_object: ToolKbTagModel) -> bool:
        tag_id = -1 if page_object.tag_id is None else page_object.tag_id
        exists = await ToolKbTagDao.get_tag_detail_by_info(query_db, ToolKbTagModel(tagName=page_object.tag_name))
        if exists and exists.tag_id != tag_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

    @classmethod
    async def check_tag_code_unique_services(cls, query_db: AsyncSession, page_object: ToolKbTagModel) -> bool:
        if not page_object.tag_code:
            return CommonConstant.UNIQUE
        tag_id = -1 if page_object.tag_id is None else page_object.tag_id
        exists = await ToolKbTagDao.get_tag_detail_by_info(query_db, ToolKbTagModel(tagCode=page_object.tag_code))
        if exists and exists.tag_id != tag_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

    @classmethod
    async def add_tag_services(cls, query_db: AsyncSession, page_object: ToolKbTagModel) -> CrudResponseModel:
        page_object.validate_fields()
        if not await cls.check_tag_name_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增标签{page_object.tag_name}失败，标签名称已存在')
        if not await cls.check_tag_code_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增标签{page_object.tag_name}失败，标签编码已存在')
        page_object.tag_sort = int(page_object.tag_sort or 0)
        try:
            await ToolKbTagDao.add_tag_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def edit_tag_services(cls, query_db: AsyncSession, page_object: ToolKbTagModel) -> CrudResponseModel:
        if page_object.tag_id is None:
            raise ServiceException(message='标签ID不能为空')
        page_object.validate_fields()
        edit_tag = page_object.model_dump(exclude_unset=True)
        current = await ToolKbTagDao.get_tag_detail_by_id(query_db, page_object.tag_id)
        if not current or current.del_flag != '0':
            raise ServiceException(message='标签不存在')
        if not await cls.check_tag_name_unique_services(query_db, page_object):
            raise ServiceException(message=f'修改标签{page_object.tag_name}失败，标签名称已存在')
        if not await cls.check_tag_code_unique_services(query_db, page_object):
            raise ServiceException(message=f'修改标签{page_object.tag_name}失败，标签编码已存在')
        edit_tag['tag_sort'] = int(edit_tag.get('tag_sort') or 0)
        try:
            await ToolKbTagDao.edit_tag_dao(query_db, edit_tag)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='更新成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def delete_tag_services(
        cls, query_db: AsyncSession, page_object: DeleteToolKbTagModel, update_by: str
    ) -> CrudResponseModel:
        if not page_object.tag_ids:
            raise ServiceException(message='传入标签id为空')
        tag_id_list = page_object.tag_ids.split(',')
        try:
            for tag_id_str in tag_id_list:
                tag_id = int(tag_id_str)
                tag = await ToolKbTagDao.get_tag_detail_by_id(query_db, tag_id)
                if not tag or tag.del_flag != '0':
                    raise ServiceException(message='标签不存在')
                used_count = await ToolKbTagDao.count_articles_by_tag_id(query_db, tag_id)
                if used_count > 0:
                    raise ServiceException(message=f'标签【{tag.tag_name}】已被教程使用，不能删除')
                await ToolKbTagDao.delete_tag_dao(query_db, tag_id, update_by, datetime.now())
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='删除成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def tag_detail_services(cls, query_db: AsyncSession, tag_id: int) -> ToolKbTagModel:
        tag = await ToolKbTagDao.get_tag_detail_by_id(query_db, tag_id)
        if not tag or tag.del_flag != '0':
            return ToolKbTagModel()
        return ToolKbTagModel(**CamelCaseUtil.transform_result(tag))

    @classmethod
    async def get_tag_options_services(cls, query_db: AsyncSession) -> list[ToolKbTagOptionModel]:
        rows = await ToolKbTagDao.get_tag_list(
            query_db, ToolKbTagPageQueryModel(status='0', pageNum=1, pageSize=1000), is_page=False
        )
        options: list[ToolKbTagOptionModel] = []
        for row in rows or []:
            if row.get('delFlag') != '0':
                continue
            options.append(ToolKbTagOptionModel(tagId=row.get('tagId'), tagName=row.get('tagName')))
        return options

    @classmethod
    async def ensure_tags_by_names_services(
        cls, query_db: AsyncSession, tag_names: list[str], operator_name: str | None = None
    ) -> list[ToolKbTag]:
        normalized_names = cls._normalize_names(tag_names)
        if not normalized_names:
            return []
        existing_tags = await ToolKbTagDao.get_tag_list_by_names(query_db, normalized_names)
        existing_map = {str(tag.tag_name): tag for tag in existing_tags}
        missing_names = [name for name in normalized_names if name not in existing_map]
        if missing_names:
            now = datetime.now()
            new_tags = [
                ToolKbTag(
                    tag_name=name,
                    tag_sort=0,
                    status='0',
                    del_flag='0',
                    create_by=operator_name or '',
                    create_time=now,
                    update_by=operator_name or '',
                    update_time=now,
                )
                for name in missing_names
            ]
            await ToolKbTagDao.add_tag_list_dao(query_db, new_tags)
            existing_map.update({str(tag.tag_name): tag for tag in new_tags})
        return [existing_map[name] for name in normalized_names if name in existing_map]

    @classmethod
    async def get_tags_by_ids_services(cls, query_db: AsyncSession, tag_ids: list[int]) -> list[ToolKbTag]:
        unique_ids = [int(tag_id) for tag_id in dict.fromkeys(tag_ids or []) if int(tag_id) > 0]
        if not unique_ids:
            return []
        tags = await ToolKbTagDao.get_tag_list_by_ids(query_db, unique_ids)
        tag_map = {int(tag.tag_id): tag for tag in tags}
        return [tag_map[tag_id] for tag_id in unique_ids if tag_id in tag_map]
