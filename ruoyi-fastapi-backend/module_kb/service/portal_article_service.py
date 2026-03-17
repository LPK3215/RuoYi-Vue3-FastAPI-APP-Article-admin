from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from exceptions.exception import ServiceException
from module_kb.dao.portal_article_dao import PortalArticleDao
from module_kb.entity.vo.portal_article_vo import (
    PortalArticleCategoryModel,
    PortalArticleDetailModel,
    PortalArticleListItemModel,
    PortalArticlePageQueryModel,
)
from module_software.entity.vo.portal_software_vo import PortalSoftwareListItemModel


class PortalArticleService:
    """
    用户端：教程文章服务层（仅查询发布数据）
    """

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
            return result
        return PageModel[PortalArticleListItemModel](**result.model_dump(by_alias=True))

    @classmethod
    async def article_detail_services(cls, query_db: AsyncSession, article_id: int) -> PortalArticleDetailModel:
        article = await PortalArticleDao.get_article_detail_by_id(query_db, article_id)
        if not article:
            raise ServiceException(message='文章不存在或未发布')

        rows = await PortalArticleDao.get_related_softwares(query_db, article_id)
        softwares: list[PortalSoftwareListItemModel] = []
        for row in rows or []:
            software = row[0] if isinstance(row, list) and len(row) > 0 else {}
            category = row[1] if isinstance(row, list) and len(row) > 1 else {}
            softwares.append(
                PortalSoftwareListItemModel(
                    **{
                        **(software or {}),
                        'categoryName': (category or {}).get('categoryName'),
                    }
                )
            )

        payload = PortalArticleDetailModel.model_validate(article).model_dump(by_alias=True)
        payload['softwares'] = softwares
        return PortalArticleDetailModel(**payload)
