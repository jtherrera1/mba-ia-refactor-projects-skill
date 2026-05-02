import logging
from flask import request, jsonify
import src.models.produto_model as produto_model
from src.config.settings import CATEGORIAS_VALIDAS, NOME_MIN_LEN, NOME_MAX_LEN

logger = logging.getLogger(__name__)


def listar():
    produtos = produto_model.get_todos()
    logger.info("Listando %d produtos", len(produtos))
    return jsonify({"dados": produtos, "sucesso": True}), 200


def buscar():
    termo = request.args.get("q", "")
    categoria = request.args.get("categoria") or None
    preco_min = request.args.get("preco_min", type=float)
    preco_max = request.args.get("preco_max", type=float)
    resultados = produto_model.buscar(termo, categoria, preco_min, preco_max)
    return jsonify({"dados": resultados, "total": len(resultados), "sucesso": True}), 200


def buscar_por_id(produto_id):
    produto = produto_model.get_por_id(produto_id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404
    return jsonify({"dados": produto, "sucesso": True}), 200


def criar():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400
    erro = _validar(dados)
    if erro:
        return jsonify({"erro": erro}), 400
    produto_id = produto_model.criar(
        dados["nome"],
        dados.get("descricao", ""),
        dados["preco"],
        dados["estoque"],
        dados.get("categoria", "geral"),
    )
    logger.info("Produto criado com ID %d", produto_id)
    return jsonify({"dados": {"id": produto_id}, "sucesso": True, "mensagem": "Produto criado"}), 201


def atualizar(produto_id):
    if not produto_model.get_por_id(produto_id):
        return jsonify({"erro": "Produto não encontrado"}), 404
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400
    erro = _validar(dados)
    if erro:
        return jsonify({"erro": erro}), 400
    produto_model.atualizar(
        produto_id,
        dados["nome"],
        dados.get("descricao", ""),
        dados["preco"],
        dados["estoque"],
        dados.get("categoria", "geral"),
    )
    return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200


def deletar(produto_id):
    if not produto_model.get_por_id(produto_id):
        return jsonify({"erro": "Produto não encontrado"}), 404
    produto_model.deletar(produto_id)
    logger.info("Produto %d deletado", produto_id)
    return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200


def _validar(dados):
    for campo in ("nome", "preco", "estoque"):
        if campo not in dados:
            return f"{campo.capitalize()} é obrigatório"
    nome = dados["nome"]
    if len(nome) < NOME_MIN_LEN:
        return "Nome muito curto"
    if len(nome) > NOME_MAX_LEN:
        return "Nome muito longo"
    if dados["preco"] < 0:
        return "Preço não pode ser negativo"
    if dados["estoque"] < 0:
        return "Estoque não pode ser negativo"
    categoria = dados.get("categoria", "geral")
    if categoria not in CATEGORIAS_VALIDAS:
        return f"Categoria inválida. Válidas: {CATEGORIAS_VALIDAS}"
    return None
