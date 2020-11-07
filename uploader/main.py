from typing import List

from loguru import logger
from tangle import Iota
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

from config import URIS, Transaction, RECEIVER, DB_URL, DR_TABLES


def check_nodes(nodes: List[str]) -> List[str]:
    iota = Iota
    available_nodes = iota.check_nodes(nodes)
    logger.info(f"Available Nodes: {available_nodes}")
    return available_nodes


def send_message(node: str, transactions: List[Transaction]) -> str:
    iota = Iota
    transaction_hash = iota.send_to_iota(node=node, transactions=transactions)
    return transaction_hash


def upload_dr(node: str):
    for department in DR_TABLES:
        logger.info(f"[Get DR Data] Department: {department.name}")
        logger.debug(f"[Get DR Data] Database: {department.database}, Table: {department.table}")
        # Basic setting
        engine = create_engine(f"{DB_URL}{department.database}")
        session = sessionmaker(bind=engine)()
        base_schema = automap_base()
        base_schema.prepare(engine, reflect=True)
        dr_schema = base_schema.classes[department.table]
        # Query data
        dr_results = session.query(dr_schema).filter(dr_schema.blockchain_url.is_(None)).all()
        logger.info(f"[Get DR Data] Get {len(dr_results)} DR data")
        for dr_result in dr_results:
            # Dump db data to json
            result = {c.name: str(getattr(dr_result, c.name)) for c in dr_result.__table__.columns}
            logger.debug(f"{department.name}\n{result}")
            # Upload to IOTA
            transaction = Transaction(address=RECEIVER, message=result, tag=f"SHALUN_{department.name}")
            transaction_hash = send_message(node, [transaction])
            # Update transaction_hash in db
            try:
                if transaction_hash:
                    logger.debug(f"[Upload DR] Transaction hash: {transaction_hash}")
                    dr_result.blockchain_url = f"https://thetangle.org/transaction/{transaction_hash}"
                    session.commit()
                    logger.info("[Upload DR] Upload success")
                else:
                    logger.error("[Upload DR] No transaction hash")
            except Exception as error:
                logger.error("[Upload DR] Update db failed")
                logger.debug(error)
                session.rollback()


if __name__ == "__main__":
    available_nodes = check_nodes(nodes=URIS)
    if available_nodes:
        upload_dr(node=available_nodes[0])
    else:
        logger.error("ALL NODES DOWN")
