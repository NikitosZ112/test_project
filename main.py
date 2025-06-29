import sys
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass

sys.path.append(str(Path(__file__).parent))

# Импорты
from src.parser.eldent_parser import ElDentParser
from src.parser.stomatorg_parser import StomatorgParser
from src.formatters.html_formatter import HTMLFormatter
from src.utils.google_sheets import GoogleSheetClient
from src.utils.logger import get_logger

try:
    from src.generators.generator import OpenDescGenerator
except ImportError:
    from src.generators.hf_generator import HFDescGenerator as OpenDescGenerator

logger = get_logger(__name__)

@dataclass
class Product:
    id: str
    name: str

def parse_products_from_competitors() -> List[Product]:
    """Парсит список товаров с сайтов конкурентов"""
    products = []
    
    try:
        # Парсим товары с el-dent.ru
        el_dent_products = ElDentParser().parse_product_list(
            "https://el-dent.ru/catalog/stomatologicheskie-nakonechniki/"
        )
        products.extend([
            Product(f"EL-{idx}", item['name']) 
            for idx, item in enumerate(el_dent_products, 1)
        ])
    except Exception as e:
        logger.error(f"Ошибка парсинга каталога El-Dent: {e}")

    try:
        # Парсим товары с stomatorg.ru
        stomatorg_products = StomatorgParser().parse_product_list(
            "https://stomatorg.ru/catalog/bori/"
        )
        products.extend([
            Product(f"ST-{idx}", item['name'])
            for idx, item in enumerate(stomatorg_products, len(products)+1)
        ])
    except Exception as e:
        logger.error(f"Ошибка парсинга каталога Stomatorg: {e}")

    return products

def process_products(products: List[Product]) -> List[Dict]:
    """Обработка и генерация описаний"""
    results = []
    generator = OpenDescGenerator()
    formatter = HTMLFormatter()

    for product in products:
        try:
            # 1. Получаем описания с конкурентов
            descriptions = []
            
            try:
                el_dent_desc = ElDentParser().get_product_description(
                    f"https://el-dent.ru/search?q={product.name}",
                    product.name
                )
                if el_dent_desc:
                    descriptions.append(f"El-Dent: {el_dent_desc}")
            except Exception as e:
                logger.error(f"Ошибка парсинга El-Dent: {e}")

            try:
                stomatorg_desc = StomatorgParser().get_product_description(
                    f"https://stomatorg.ru/search?query={product.name}",
                    product.name
                )
                if stomatorg_desc:
                    descriptions.append(f"Stomatorg: {stomatorg_desc}")
            except Exception as e:
                logger.error(f"Ошибка парсинга Stomatorg: {e}")

            if not descriptions:
                continue

            # 2. Генерируем уникальное описание
            generated = generator.generate_description(
                product.name, 
                "\n\n".join(descriptions)
            )

            # 3. Форматируем
            results.append({
                "id": product.id,
                "name": product.name,
                "description": formatter.format_to_html(generated["description"]),
                "source_text": "\n---\n".join(descriptions)
            })

        except Exception as e:
            logger.error(f"Ошибка обработки {product.name}: {e}")

    return results

if __name__ == "__main__":
    logger.info("Начало парсинга каталогов конкурентов")
    
    # 1. Парсим список товаров
    products = parse_products_from_competitors()
    logger.info(f"Найдено {len(products)} товаров для обработки")
    
    # 2. Обрабатываем товары
    if products:
        processed_data = process_products(products)
        logger.info(f"Успешно обработано {len(processed_data)} товаров")
        
        # 3. Сохраняем в Google Sheets
        GoogleSheetClient().append_data(processed_data)
        logger.info("Данные сохранены в таблицу")
    else:
        logger.error("Не найдено товаров для обработки")