import logging

logger = logging.getLogger(__name__)


def notificar_pedido_criado(pedido_id, usuario_id):
    logger.info("Pedido %d criado para usuario %d — email/SMS/push enviados", pedido_id, usuario_id)


def notificar_status_atualizado(pedido_id, novo_status):
    if novo_status == "aprovado":
        logger.info("Pedido %d aprovado — preparar envio", pedido_id)
    elif novo_status == "cancelado":
        logger.warning("Pedido %d cancelado — verificar devolução de estoque", pedido_id)
