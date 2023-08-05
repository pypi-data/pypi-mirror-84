from typing import List, Tuple, Union
from urllib.parse import parse_qsl, urlparse

import requests
from bs4 import BeautifulSoup
from tld import get_fld
from w3lib.url import url_query_cleaner

__author__ = "Elton H.Y. Chou"

__license__ = "MIT"
__version__ = "0.0.4-beta"
__maintainer__ = "Elton H.Y. Chou"
__email__ = "plscd748@gmail.com"


class NoMoreQS:
    """No more query string"""

    headers: dict = {}

    def __init__(self,
                 include_flds: Union[List[str], Tuple[str]] = (),
                 exclude_flds: Union[List[str], Tuple[str]] = (),
                 strict: bool = True):
        """
        Parameters
        ----------
        include_flds : Union[List[str], Tuple[str]], optional
            first-level domains list which are allowed to clean query string,
            by default []

        exclude_flds : Union[List[str], Tuple[str]], optional
            first-level domains which are disallowed to clean query string,
            by default []

        strict : bool, optional
            mode of clean, by default True
        """
        self.include_flds = include_flds
        self.exclude_flds = exclude_flds
        self.strict = strict

    def clean(self, url: str, cookies: dict = {}) -> str:
        """
        clean

        Parameters
        ----------
        url : str
            Any useable url.

        Returns
        -------
        str
            cleaned url, fbclid is always be cleaned.
        """
        fld = get_fld(url)

        cleaner = _super_cleaner if self.strict else _fbclid_cleaner

        is_allowed_fld = fld in self.exclude_flds
        if is_allowed_fld:
            cleaner = _fbclid_cleaner

        is_not_allowed_fld = fld in self.include_flds
        if is_not_allowed_fld:
            cleaner = _super_cleaner

        return cleaner(url, headers=self.headers, cookies=cookies)

    @staticmethod
    def remove_fbclid(url: str) -> str:
        """
        remove fbclid
        if you affraid the power of super cleaner,
        you can just clean the fbclid easily with this method.

        Parameters
        ----------
        url : str
            Any useable url.

        Returns
        -------
        str
            cleaned url, fbclid is always be cleaned.
        """
        return _fbclid_cleaner(url)


def _super_cleaner(url: str, headers: dict = {}, cookies: dict = {}) -> str:
    """
    super cleaner

    Parameters
    ----------
    url : str
        Any useable url.

    kwargs : dict, optional
        Optional arguments that ``request`` takes.

    Returns
    -------
    str
        cleaned url, fbclid is always be cleaned.
    """
    url = _fbclid_cleaner(url)
    page = _get_page(url, headers, cookies)

    if not page:
        return _fbclid_cleaner(url)

    canonical_url = _get_canonical_url(page)
    og_url = _get_og_url(page)

    origin_path_len = len(urlparse(url).path)
    og_path_len = len(urlparse(og_url).path)
    canonical_path_len = len(urlparse(canonical_url).path)

    origin_qs_len = count_qs_length(url)
    canonical_qs_len = count_qs_length(canonical_url)
    og_qs_len = count_qs_length(og_url)

    # path_len > qs_len > -(netloc)
    candidate_urls = sorted([
        (origin_path_len, origin_qs_len, -len(urlparse(url).netloc), url),
        (canonical_path_len, canonical_qs_len, -len(urlparse(canonical_url).netloc), canonical_url),
        (og_path_len, og_qs_len, -len(urlparse(og_url).netloc), og_url)
    ])

    for path_len, _, _, the_url in candidate_urls:
        if path_len:
            return the_url

    return url


def _fbclid_cleaner(url: str, **kwargs) -> str:
    """
    Clean the fbclid!

    Parameters
    ----------
    url : str
        Any useable url.

    Returns
    -------
    str
        cleaned url, fbclid is always be cleaned.
    """
    url = url_query_cleaner(url, ("fbclid"), remove=True)
    return url


def _get_canonical_url(page: BeautifulSoup) -> str:
    """
    get canonical url

    Parameters
    ----------
    page : BeautifulSoup
        BeautiifulSoup object

    Returns
    -------
    str
        link[canonical url]
    """
    canonical_url = page.select_one("link[rel='canonical']")

    if canonical_url:
        return _fbclid_cleaner(canonical_url["href"])

    return ''


def _get_og_url(page: BeautifulSoup) -> str:
    """
    get og:url

    Parameters
    ----------
    page : BeautifulSoup
        BeautiifulSoup object

    Returns
    -------
    str
        meta[og:url]
    """
    og_url_selector = "meta[property='og:url']"
    og_url = page.select_one(f"head > {og_url_selector}")
    if not og_url:
        og_url = page.select_one(f"body > {og_url_selector}")

    if og_url:
        return _fbclid_cleaner(og_url["content"])

    return ''


def _get_page(url: str, headers: dict = {}, cookies: dict = {}) -> BeautifulSoup:
    """
    Return page as BeautifulSoup object

    Parameters
    ----------
    url : str
        a useable url
    headers : dict, optional
        headers, by default {}
    cookies : dict, optional
        cookies, by default {}

    Returns
    -------
    BeautifulSoup
    """
    response = requests.get(url, headers=headers, cookies=cookies)

    if response.status_code > 400:
        return False

    page = BeautifulSoup(response.text, "lxml")
    return page


def parse_url_qs_to_dict(url: str) -> dict:
    """
    Return qs as dict, if no qs return {}

    Parameters
    ----------
    url : str
        validate url

    Returns
    -------
    dict
        qs as dict
    """
    if not url:
        return {}

    qs = urlparse(url).query
    dict_qs = dict(parse_qsl(qs))

    return dict_qs


def count_qs_length(url: str) -> int:
    return len(parse_url_qs_to_dict(url)) if url else 0
