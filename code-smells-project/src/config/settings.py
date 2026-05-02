import os

SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
DB_PATH = os.environ.get("DB_PATH", "loja.db")

CATEGORIAS_VALIDAS = ["informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"]
STATUS_VALIDOS = ["pendente", "aprovado", "enviado", "entregue", "cancelado"]

NOME_MIN_LEN = 2
NOME_MAX_LEN = 200

DISCOUNT_TIER_HIGH = 10_000
DISCOUNT_TIER_MED = 5_000
DISCOUNT_TIER_LOW = 1_000
DISCOUNT_RATE_HIGH = 0.10
DISCOUNT_RATE_MED = 0.05
DISCOUNT_RATE_LOW = 0.02
