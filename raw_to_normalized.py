from pathlib import Path
from diskcache import FanoutCache
import geocoder
import logging

from concurrent.futures import ThreadPoolExecutor
import backoff



log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

cache = FanoutCache('cache')
output_dir = Path('normalized')
raw = Path('raw')

class RetryMe(Exception):
    pass

@cache.memoize()
@backoff.on_exception(backoff.constant, RetryMe, max_tries=10)
def normalize(addr: str) -> str:
    log.info(f"Normalizing: {addr}")

    res = geocoder.arcgis(location=addr, timeout=12)
    if res:
        return res.current_result.address

    log.warning(f"Normalize failed for: {addr}")
    raise RetryMe(f"Error: {res.error}")

def normalize_stupid(addr: str) -> str:
    addr = addr.replace(',', ' ')
    addr = ' '.join(addr.split())
    return addr.replace('#', '').replace(' US', '').strip()

def normalize_addr_file(addr_file: Path) -> None:
    """
    Normalize the addresses in the given file.
    """
    log.info(f"Normalizing addresses in {addr_file.name}")

    with ThreadPoolExecutor(max_workers=28) as executor:
        normalized_addresses = executor.map(
            normalize,
            [addr.strip() for addr in addr_file.read_text().splitlines() if addr.strip()]
        )

    output_file = output_dir / addr_file.name
    output_dir.mkdir(exist_ok=True, parents=True)

    output_file.unlink(missing_ok=True)

    with open(output_file, 'w') as f:
        for addr in sorted(set(normalized_addresses)):
            f.write(addr + '\n')

def normalize_addr_files() -> None:
    for addr_file in sorted(raw.glob('*.txt')):
        normalize_addr_file(addr_file)