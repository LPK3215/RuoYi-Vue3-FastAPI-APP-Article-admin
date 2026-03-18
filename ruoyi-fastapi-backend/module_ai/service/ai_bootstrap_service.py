from datetime import datetime

from sqlalchemy import select

from config.database import AsyncSessionLocal
from config.env import AIBootstrapConfig
from module_ai.entity.do.ai_model_do import AiModels
from utils.log_util import logger


class AiBootstrapService:
    """
    AI 默认模型初始化服务
    """

    @classmethod
    def _build_default_models(cls) -> list[AiModels]:
        now = datetime.now()
        models = [
            AiModels(
                model_code=AIBootstrapConfig.ai_bootstrap_ollama_model_code,
                model_name=AIBootstrapConfig.ai_bootstrap_ollama_model_name,
                provider='Ollama',
                model_sort=10,
                base_url=AIBootstrapConfig.ai_bootstrap_ollama_base_url,
                model_type='chat',
                max_tokens=4096,
                temperature=0.7,
                support_reasoning='N',
                support_images='N',
                status='0',
                create_by='system',
                create_time=now,
                update_by='system',
                update_time=now,
                remark='默认本地模型模板，可直接配合 Ollama 使用',
            )
        ]
        if AIBootstrapConfig.ai_bootstrap_openai_template_enabled:
            models.append(
                AiModels(
                    model_code=AIBootstrapConfig.ai_bootstrap_openai_model_code,
                    model_name=AIBootstrapConfig.ai_bootstrap_openai_model_name,
                    provider='OpenAI',
                    model_sort=20,
                    base_url=AIBootstrapConfig.ai_bootstrap_openai_base_url,
                    model_type='chat',
                    max_tokens=8192,
                    temperature=0.7,
                    support_reasoning='Y',
                    support_images='Y',
                    status='1',
                    create_by='system',
                    create_time=now,
                    update_by='system',
                    update_time=now,
                    remark='默认远程模型模板，填写 API Key 后启用',
                )
            )
        return models

    @classmethod
    async def bootstrap_default_models(cls) -> None:
        """
        在 AI 模型表为空时写入默认模型模板
        """
        if not AIBootstrapConfig.ai_bootstrap_enabled:
            return

        async with AsyncSessionLocal() as session:
            existing = (await session.execute(select(AiModels.model_id).limit(1))).scalar_one_or_none()
            if existing is not None:
                return

            default_models = cls._build_default_models()
            if not default_models:
                return

            session.add_all(default_models)
            try:
                await session.commit()
                logger.info(f'AI 默认模型初始化完成，共写入 {len(default_models)} 条记录')
            except Exception as exc:
                await session.rollback()
                logger.warning(f'AI 默认模型初始化失败：{exc}')
