import enum
import logging

from bs4 import BeautifulSoup
from urllib.parse import urlparse

from diskcache import FanoutCache
import requests

from concurrent.futures import ThreadPoolExecutor

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
logging.basicConfig()

cache = FanoutCache('cache')

class LocationType(enum.Enum):
    TacoBell = "TacoBell"
    PizzaHut = "PizzaHut"
    KFC = "KFC"

    def get_dir_links_selector(self) -> str:
        if self == LocationType.TacoBell:
            return '.DirLinks'
        elif self == LocationType.PizzaHut:
            return '.Link.flex.gap-2.w-fit'
        elif self == LocationType.KFC:
            return '.Directory-listLink'

        raise NotImplementedError()

    def get_addresses_from_soup(self, soup: BeautifulSoup) -> list[str]:
        """
        Get the addresses from the soup object.
        """
        addresses = []

        if self == LocationType.TacoBell:
            address_elements = soup.select('.address')
            for address in address_elements:
                addresses.append(address.text.replace('\n', ' ').strip())
        elif self == LocationType.PizzaHut:
            groups = soup.select(".flex.flex-col.border.border-border-gray")
            for group in groups:
                address = group.select(".address-line")
                possible_addr = ' '.join([a.text for a in address]).strip()
                if possible_addr:
                    # get rid of excess spaces
                    addresses.append(' '.join(possible_addr.split()))
        elif self == LocationType.KFC:
            address_elements = soup.select('.c-address')
            for address in address_elements:
                addresses.append(address.text.replace('\n', ' ').strip())

        return addresses

@cache.memoize()
def _get_str(url: str) -> str:
    log.info(f"GET: {url}")
    response = requests.get(url)
    return response.text

def get(url: str) -> BeautifulSoup:
    """
    Fetch the HTML content from the given URL and return a BeautifulSoup object.
    """
    return BeautifulSoup(_get_str(url))


def get_locations(url: str, typ: LocationType, multithread: bool=True) -> list[str]:
    """
    Get the locations from the given URL.
    """
    soup = get(url)

    dir_links = soup.select(typ.get_dir_links_selector())

    hrefs = []
    for link in dir_links:
        hrefs.append(link.attrs['href'])

    locations = []
    hostname = urlparse(url).hostname

    if multithread:
        with ThreadPoolExecutor() as executor:
            locations.extend([item for sublist in list(executor.map(lambda href: get_locations(f'https://{hostname}/{href}', typ, multithread=True), hrefs)) for item in sublist])
    else:
        locations.extend([item for sublist in list(map(lambda href: get_locations(f'https://{hostname}/{href}', typ, multithread=False), hrefs)) for item in sublist])

    locations.extend(typ.get_addresses_from_soup(soup))

    # grr we get dups.. boo
    return sorted(set(locations))

