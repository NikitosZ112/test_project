import requests
from config.settings import HF_API_KEY, HF_API_URL

class HFDescGenerator:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    def generate_description(self, product_name: str, base_text: str) -> dict:
        try:
            response = requests.post(
                HF_API_URL,
                headers=self.headers,
                json={"inputs": f"Сгенерируй описание для {product_name}: {base_text}"}
            )
            return {"description": response.json()[0]["generated_text"]}
        except Exception as e:
            print(f"HF API Error: {e}")
            return {"description": ""}