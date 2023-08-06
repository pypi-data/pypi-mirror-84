from typing import List
from concurrent.futures import ThreadPoolExecutor

from .validators import validate_node


def validate(nodes: List[dict]):
    with ThreadPoolExecutor(max_workers=1000) as executor:
        return list(executor.map(validate_node, nodes))
