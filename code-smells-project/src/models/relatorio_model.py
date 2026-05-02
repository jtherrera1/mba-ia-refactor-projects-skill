from src.database.connection import get_db
from src.config.settings import (
    DISCOUNT_TIER_HIGH,
    DISCOUNT_TIER_MED,
    DISCOUNT_TIER_LOW,
    DISCOUNT_RATE_HIGH,
    DISCOUNT_RATE_MED,
    DISCOUNT_RATE_LOW,
)


def get_relatorio_vendas():
    db = get_db()
    total_pedidos = db.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]
    faturamento = db.execute("SELECT COALESCE(SUM(total), 0) FROM pedidos").fetchone()[0]
    pendentes = db.execute("SELECT COUNT(*) FROM pedidos WHERE status='pendente'").fetchone()[0]
    aprovados = db.execute("SELECT COUNT(*) FROM pedidos WHERE status='aprovado'").fetchone()[0]
    cancelados = db.execute("SELECT COUNT(*) FROM pedidos WHERE status='cancelado'").fetchone()[0]

    if faturamento > DISCOUNT_TIER_HIGH:
        desconto = faturamento * DISCOUNT_RATE_HIGH
    elif faturamento > DISCOUNT_TIER_MED:
        desconto = faturamento * DISCOUNT_RATE_MED
    elif faturamento > DISCOUNT_TIER_LOW:
        desconto = faturamento * DISCOUNT_RATE_LOW
    else:
        desconto = 0.0

    return {
        "total_pedidos": total_pedidos,
        "faturamento_bruto": round(faturamento, 2),
        "desconto_aplicavel": round(desconto, 2),
        "faturamento_liquido": round(faturamento - desconto, 2),
        "pedidos_pendentes": pendentes,
        "pedidos_aprovados": aprovados,
        "pedidos_cancelados": cancelados,
        "ticket_medio": round(faturamento / total_pedidos, 2) if total_pedidos > 0 else 0,
    }
