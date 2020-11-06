from typing import List

from loguru import logger
from uploader.tangle import Iota

from config import URIS, Transaction, RECEIVER


TX = Transaction(address=RECEIVER, message="test123", tag="TEST",)


def check_nodes(nodes: List[str]) -> List[str]:
    iota = Iota
    available_nodes = iota.check_nodes(nodes)
    logger.info(f"Available Nodes: {available_nodes}")
    return available_nodes


def send_message(node: str, transactions: List[Transaction]) -> str:
    iota = Iota
    bundle_hash = iota.send_to_iota(node=node, transactions=transactions)
    return bundle_hash


if __name__ == "__main__":
    available_nodes = check_nodes(nodes=URIS)
    send_message(node=available_nodes[0], transactions=[TX])
