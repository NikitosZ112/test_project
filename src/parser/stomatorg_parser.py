import requests
from bs4 import BeautifulSoup
from typing import Optional
from src.utils.logger import get_logger
from typing import List

logger = get_logger(__name__)

class StomatorgParser:
    @staticmethod
    def get_product_description(url: str, product_name: str) -> Optional[str]:
        """Парсинг описания с stomatorg.ru"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Ищем описание (адаптируйте под актуальную структуру сайта)
            description = soup.find('div', class_='product-detail-description') or \
                         soup.find('div', class_='product-card__description')
            
            return description.get_text(strip=True) if description else None
            
        except Exception as e:
            logger.error(f"StomatorgParser error: {e}")
            return None
        
    def parse_product_list(self, catalog_url: str) -> List[dict]:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(catalog_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return [
                {'name': item.get_text(strip=True)}
                for item in soup.select('.product-title')  # Адаптируйте селектор
            ]
        except Exception as e:
            logger.error(f"Ошибка парсинга каталога: {e}")
            return []