from src.database.connection import get_db

_PEDIDOS_SQL = """
    SELECT
        p.id          AS pedido_id,
        p.usuario_id,
        p.status,
        p.total,
        p.criado_em,
        ip.id         AS item_id,
        ip.produto_id,
        ip.quantidade,
        ip.preco_unitario,
        prod.nome     AS produto_nome
    FROM pedidos p
    LEFT JOIN itens_pedido ip   ON ip.pedido_id  = p.id
    LEFT JOIN produtos     prod ON prod.id        = ip.produto_id
"""


def _build_pedidos(rows):
    pedidos: dict = {}
    for row in rows:
        pid = row["pedido_id"]
        if pid not in pedidos:
            pedidos[pid] = {
                "id": pid,
                "usuario_id": row["usuario_id"],
                "status": row["status"],
                "total": row["total"],
                "criado_em": row["criado_em"],
                "itens": [],
            }
        if row["item_id"]:
            pedidos[pid]["itens"].append({
                "produto_id": row["produto_id"],
                "produto_nome": row["produto_nome"] or "Desconhecido",
                "quantidade": row["quantidade"],
                "preco_unitario": row["preco_unitario"],
            })
    return list(pedidos.values())


def get_todos():
    rows = get_db().execute(_PEDIDOS_SQL + " ORDER BY p.id").fetchall()
    return _build_pedidos(rows)


def get_por_usuario(usuario_id):
    rows = get_db().execute(
        _PEDIDOS_SQL + " WHERE p.usuario_id = ? ORDER BY p.id", (usuario_id,)
    ).fetchall()
    return _build_pedidos(rows)


def criar(usuario_id, itens):
    db = get_db()
    cursor = db.cursor()

    total = 0.0
    for item in itens:
        row = cursor.execute(
            "SELECT preco, estoque, nome FROM produtos WHERE id = ?",
            (item["produto_id"],),
        ).fetchone()
        if row is None:
            return {"erro": f"Produto {item['produto_id']} não encontrado"}
        if row["estoque"] < item["quantidade"]:
            return {"erro": f"Estoque insuficiente para {row['nome']}"}
        total += row["preco"] * item["quantidade"]

    cursor.execute(
        "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
        (usuario_id, total),
    )
    pedido_id = cursor.lastrowid

    for item in itens:
        preco = cursor.execute(
            "SELECT preco FROM produtos WHERE id = ?", (item["produto_id"],)
        ).fetchone()["preco"]
        cursor.execute(
            "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)"
            " VALUES (?, ?, ?, ?)",
            (pedido_id, item["produto_id"], item["quantidade"], preco),
        )
        cursor.execute(
            "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
            (item["quantidade"], item["produto_id"]),
        )

    db.commit()
    return {"pedido_id": pedido_id, "total": total}


def atualizar_status(pedido_id, novo_status):
    db = get_db()
    db.execute("UPDATE pedidos SET status = ? WHERE id = ?", (novo_status, pedido_id))
    db.commit()
