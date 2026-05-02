from flask import jsonify
import src.models.relatorio_model as relatorio_model


def vendas():
    relatorio = relatorio_model.get_relatorio_vendas()
    return jsonify({"dados": relatorio, "sucesso": True}), 200
