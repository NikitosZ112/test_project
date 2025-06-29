import requests
from bs4 import BeautifulSoup
from typing import Optional
from src.utils.logger import get_logger
from typing import List

logger = get_logger(__name__)

class ElDentParser:
    @staticmethod
    def get_product_description(url: str, product_name: str) -> Optional[str]:
        """Парсит описание с сайта el-dent.ru"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            description = soup.find('div', class_='product-description')
            return description.get_text(strip=True) if description else None
            
        except Exception as e:
            logger.error(f"Ошибка парсинга {url}: {e}")
            return None
        
    def parse_product_list(self, catalog_url: str) -> List[dict]:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(catalog_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            products = []
            
            for item in soup.select('.product-card'):  # Адаптируйте селектор
                name = item.select_one('.product-name').get_text(strip=True)
                products.append({'name': name})
                
            return products
        except Exception as e:
            logger.error(f"Ошибка парсинга каталога: {e}")
            return []