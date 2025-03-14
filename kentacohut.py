from pathlib import Path
import logging
from itertools import combinations


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

normalized = Path('normalized')
combos = Path('combos')

def read_in_normalized() -> dict[str, set[str]]:
    normalized_dict = {}
    for addr_file in sorted(normalized.glob('*.txt')):
        normalized_dict[addr_file.stem] = set(addr_file.read_text().splitlines())
    return normalized_dict


def intersect_dict_sets(data: dict[str, set[str]]) -> dict[tuple[str, ...], set[str]]:
    max_size = len(data)

    result = {}
    keys = list(data.keys())

    for size in range(2, max_size + 1):
        for key_combo in combinations(keys, size):
            intersection = set.intersection(*(data[key] for key in key_combo))
            result[key_combo] = intersection

    return result

def find_restaurant_combos() -> dict[tuple[str, ...], set[str]]:
    normalized_dict = read_in_normalized()
    result = intersect_dict_sets(normalized_dict)

    combos.mkdir(exist_ok=True, parents=True)

    for key_combo, addresses in result.items():
        file_name = ('_'.join(sorted(key_combo))) + '.txt'
        combo_file = combos / file_name
        combo_file.unlink(missing_ok=True)

        with open(combo_file, 'w') as f:
            for addr in sorted(set(addresses)):
                f.write(addr + '\n')

    return result