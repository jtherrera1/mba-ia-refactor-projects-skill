from flask import Blueprint
import src.controllers.produto_controller as produto_ctrl
import src.controllers.usuario_controller as usuario_ctrl
import src.controllers.pedido_controller as pedido_ctrl
import src.controllers.relatorio_controller as relatorio_ctrl

bp = Blueprint("api", __name__)

bp.add_url_rule("/produtos",                       "listar_produtos",       produto_ctrl.listar,           methods=["GET"])
bp.add_url_rule("/produtos/busca",                 "buscar_produtos",       produto_ctrl.buscar,           methods=["GET"])
bp.add_url_rule("/produtos/<int:produto_id>",      "buscar_produto",        produto_ctrl.buscar_por_id,    methods=["GET"])
bp.add_url_rule("/produtos",                       "criar_produto",         produto_ctrl.criar,            methods=["POST"])
bp.add_url_rule("/produtos/<int:produto_id>",      "atualizar_produto",     produto_ctrl.atualizar,        methods=["PUT"])
bp.add_url_rule("/produtos/<int:produto_id>",      "deletar_produto",       produto_ctrl.deletar,          methods=["DELETE"])

bp.add_url_rule("/usuarios",                       "listar_usuarios",       usuario_ctrl.listar,           methods=["GET"])
bp.add_url_rule("/usuarios/<int:usuario_id>",      "buscar_usuario",        usuario_ctrl.buscar_por_id,    methods=["GET"])
bp.add_url_rule("/usuarios",                       "criar_usuario",         usuario_ctrl.criar,            methods=["POST"])
bp.add_url_rule("/login",                          "login",                 usuario_ctrl.login,            methods=["POST"])

bp.add_url_rule("/pedidos",                        "criar_pedido",          pedido_ctrl.criar,             methods=["POST"])
bp.add_url_rule("/pedidos",                        "listar_todos_pedidos",  pedido_ctrl.listar_todos,      methods=["GET"])
bp.add_url_rule("/pedidos/usuario/<int:usuario_id>","listar_pedidos_usuario",pedido_ctrl.listar_por_usuario,methods=["GET"])
bp.add_url_rule("/pedidos/<int:pedido_id>/status", "atualizar_status",      pedido_ctrl.atualizar_status,  methods=["PUT"])

bp.add_url_rule("/relatorios/vendas",              "relatorio_vendas",      relatorio_ctrl.vendas,         methods=["GET"])
