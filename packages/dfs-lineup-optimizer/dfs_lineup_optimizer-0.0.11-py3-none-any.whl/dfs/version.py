from typing import Optional

import pkg_resources

version: Optional[str] = None


def get_version() -> str:
    global version
    if version:
        return version
    try:
        version = pkg_resources.get_distribution('dfs-lineup-optimizer').version
    except pkg_resources.DistributionNotFound:
        version = 'LOCAL'
    return version
