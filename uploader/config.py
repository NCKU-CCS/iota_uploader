import os
from dataclasses import dataclass, field

import iota
from dotenv import load_dotenv


load_dotenv()

SEED = iota.crypto.types.Seed.random()
RECEIVER = str(iota.crypto.addresses.AddressGenerator(SEED).get_addresses(1)[0])


@dataclass
class Transaction:
    # pylint: disable=C0103
    address: str = None
    message: dict = field(default_factory=dict)
    tag: str = None
    # pylint: enable=C0103


URIS = [
    "http://node.deviceproof.org:14265",
    "http://node1.puyuma.org:14265",
    "http://node10.puyuma.org:14265",
    "https://node.deviceproof.org:443",
    "https://nodes.thetangle.org:443",
]

DB_URL = os.environ.get("DB_URL", 'mysql+pymysql://account:passwd@host:port/')


@dataclass
class DB_TABLE:
    # pylint: disable=C0103
    name: str = None
    database: str = None
    table: str = None
    # pylint: enable=C0103


DR_TABLES = [
    DB_TABLE(name="C_BEMS", database="shalun_c_ems", table="bems_aggregator_dr_event"),
    DB_TABLE(name="C_CEMS", database="shalun_cems", table="aggregator_dr_event"),
]
