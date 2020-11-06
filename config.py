from dataclasses import dataclass


@dataclass
class Transaction:
    # pylint: disable=C0103
    address: str = None
    message: str = None
    tag: str = None
    # pylint: enable=C0103


RECEIVER = "RPFTKVV9YCCZAFDTFLJULPHWXUY9TRMAWMJPHZCTENYJGPXFPHSBT9P9IKEEIUEBUYOESEGFPYMGKUCNZLAAOZTVTB"

URIS = [
    "http://node.deviceproof.org:14265",
    "http://node1.puyuma.org:14265",
    "http://node10.puyuma.org:14265",
    "https://node.deviceproof.org:443",
    "https://nodes.thetangle.org:443",
]
