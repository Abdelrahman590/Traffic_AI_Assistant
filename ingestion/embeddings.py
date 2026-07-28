from models.llm_loader import KaggleRemoteEmbeddings
from config import KAGGLE_API_URL


def get_embeddings_model() -> KaggleRemoteEmbeddings:
    return KaggleRemoteEmbeddings(api_url=KAGGLE_API_URL)
