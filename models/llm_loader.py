


from typing import Any, List, Mapping, Optional
import requests

from langchain_core.language_models.llms import LLM
from langchain_core.embeddings import Embeddings

from config import KAGGLE_API_URL, REQUEST_TIMEOUT


class KaggleRemoteLLM(LLM):

    api_url: str = KAGGLE_API_URL
    system_prompt: str = ""
    temperature: float = 0.3
    max_new_tokens: int = 512

    @property
    def _llm_type(self) -> str:
        return "kaggle_remote_llm"

    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any) -> str:
        payload = {
            "prompt": prompt,
            "system_prompt": self.system_prompt,
            "max_new_tokens": kwargs.get("max_new_tokens", self.max_new_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
        }
        try:
            response = requests.post(
                f"{self.api_url}/generate",
                json=payload,
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("text", "").strip()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(
                f"تعذر الاتصال بسيرفر Kaggle على {self.api_url}. "
                f"تأكد إن سيشن Kaggle شغالة ولينك ngrok محدث في .env. التفاصيل: {e}"
            )

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"api_url": self.api_url}


class KaggleRemoteEmbeddings(Embeddings):

    def __init__(self, api_url: str = KAGGLE_API_URL):
        self.api_url = api_url

    def _embed(self, texts: List[str]) -> List[List[float]]:
        try:
            response = requests.post(
                f"{self.api_url}/embed",
                json={"texts": texts},
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()
            return data["embeddings"]
        except requests.exceptions.RequestException as e:
            raise ConnectionError(
                f"تعذر الاتصال بسيرفر Kaggle على {self.api_url}. "
                f"تأكد إن سيشن Kaggle شغالة ولينك ngrok محدث في .env. التفاصيل: {e}"
            )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # نبعتهم على دفعات عشان منحملش الطلب أكتر من اللازم
        batch_size = 32
        all_embeddings: List[List[float]] = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            all_embeddings.extend(self._embed(batch))
        return all_embeddings

    def embed_query(self, text: str) -> List[float]:
        return self._embed([text])[0]


def check_server_health(api_url: str = KAGGLE_API_URL) -> bool:
    """للتأكد إن سيرفر Kaggle شغال قبل ما نستخدمه."""
    try:
        response = requests.get(f"{api_url}/health", timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
