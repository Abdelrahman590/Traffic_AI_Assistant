import os
from dotenv import load_dotenv

load_dotenv()

KAGGLE_API_URL = os.getenv("KAGGLE_API_URL", " https://basket-placidly-deftly.ngrok-free.dev")

REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "120"))

LICENSE_DOC_PATH = os.getenv("LICENSE_DOC_PATH", r"D:\traffic-ai-assistant\data\license_info.docx")
VIOLATIONS_XLSX_PATH = os.getenv("VIOLATIONS_XLSX_PATH", r"D:\traffic-ai-assistant\data\violations.xlsx")

VECTOR_STORE_DIR = os.getenv("VECTOR_STORE_DIR", "vector_store")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 80

# عدد النتائج المسترجعة
TOP_K = 4
