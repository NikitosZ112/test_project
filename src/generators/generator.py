import openai
from typing import Dict
from config.settings import OPENAI_API_KEY
from src.utils.logger import get_logger

logger = get_logger(__name__)

class OpenAIDescGenerator:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY

    def generate_description(self, product_name: str, base_text: str) -> Dict[str, str]:
        """Генерирует описание через OpenAI"""
        try:
            prompt = f"""
            Сгенерируй SEO-описание для стоматологического товара "{product_name}".
            Исходный текст: {base_text}
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты копирайтер для стоматологического магазина."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return {
                "description": response.choices[0].message.content.strip(),
                "tokens_used": response.usage["total_tokens"]
            }
            
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            raise