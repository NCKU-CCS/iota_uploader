import json
from typing import List

import requests
from loguru import logger
from iota import Iota as iota
from iota import HttpAdapter, ProposedTransaction, Address, TryteString, Tag

from config import Transaction


class Iota:
    @staticmethod
    def check_nodes(nodes: List[str], timeout: int = 5) -> List[str]:
        """check available nodes

        Args:
            nodes (List[str]): nodes for testing
            timeout (int): timeout for testing

        Returns:
            List[str]: available nodes
        """
        available_nodes: List[str] = list()
        for node in nodes:
            logger.info(f"[CHECK NODES] Testing {node}")
            try:
                api = iota(HttpAdapter(node, timeout=timeout))
                # Check node alive
                node_info = api.get_node_info()
                # Show Node Info
                logger.debug(node_info)
                # Check node milestone is latest
                assert node_info["latestMilestone"] == node_info["latestSolidSubtangleMilestone"]
                logger.success(f"[CHECK NODES] Node is alive. URI: {node}")
                available_nodes.append(node)
            except AssertionError:
                logger.warning(f"[CHECK NODES] Node is not up to date. URI: {node}")
            except requests.exceptions.ConnectionError:
                logger.error(f"[CHECK NODES] Node is down. URI: {node}")
            except requests.exceptions.ReadTimeout:
                logger.error(f"[CHECK NODES] Node timeout. URI: {node}")
        return available_nodes

    @staticmethod
    def send_to_iota(node: str, transactions: List[Transaction], local_pow: bool = False) -> str:
        """send json type data to IOTA

        Args:
            node (str): IOTA node
            transactions (List[Transaction]): transactions
            local_pow (bool, optional): local pow, might failed. Defaults to False.

        Returns:
            str: transaction hash
        """
        logger.info(f"[SEND TO IOTA] Data: {transactions}")
        # Prepare transactions
        transfers = [
            ProposedTransaction(
                address=Address(transaction.address),
                message=TryteString.from_bytes(json.dumps(transaction.message).encode()),
                tag=Tag(transaction.tag.replace("_", "9")),
                value=0,
            )
            for transaction in transactions
        ]
        # Create adapter
        logger.info(f"[SEND TO IOTA] IOTA node: {node}")
        api = iota(adapter=node, local_pow=local_pow)
        # Send transactions to IOTA
        logger.info("[SEND TO IOTA] Sending...")
        bundle_result = api.send_transfer(transfers=transfers)["bundle"]
        logger.info("[SEND TO IOTA]            Done")
        # Transaction hash
        logger.info(
            f"[SEND TO IOTA] Transaction hash: {bundle_result.transactions[0].hash}, Bundle hash: {bundle_result.hash}"
        )
        # Show bundle result
        logger.debug(bundle_result.as_json_compatible())
        return str(bundle_result.transactions[0].hash)
