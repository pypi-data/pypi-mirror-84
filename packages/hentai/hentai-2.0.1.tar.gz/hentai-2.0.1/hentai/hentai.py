#!/usr/bin/env python3

"""
Implements a wrapper class around nhentai's RESTful API.
Copyright (C) 2020  hentai-chan (dev.hentai-chan@outlook.com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import annotations

import csv
import json
import random
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum, unique
from importlib.resources import path as resource_path
from pathlib import Path
from typing import List, Tuple
from urllib.parse import urljoin, urlparse
from urllib.request import getproxies

import requests
from faker import Faker
from requests import HTTPError, Session
from requests.adapters import HTTPAdapter
from requests.models import Response
from urllib3.util.retry import Retry

try:
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 7
except AssertionError:
    raise RuntimeError("Hentai requires Python 3.7+!") 


@dataclass
class Tag:
    """
    A data class that bundles related `Tag` properties and useful helper methods.
    """
    id: int
    type: str
    name: str
    url: str
    count: int

    @staticmethod
    def get_ids(tags: List[Tag]) -> int or List[int]:
        """
        Return a list of IDs corresponding to the passed Tag objects.
        
        ### Example:
        ```python
        >>> from hentai import Hentai, Tag
        >>> doujin = Hentai(177013)
        >>> Tag.get_ids(doujin.artist)
        3981
        ```
        """
        ids = [tag.id for tag in tags]
        return ids[0] if len(ids) == 1 else ids

    @staticmethod
    def get_types(tags: List[Tag]) -> str or List[str]:
        """
        Return a list of types corresponding to the passed Tag objects.

        ### Example:
        ```python
        >>> from hentai import Hentai, Tag
        >>> doujin = Hentai(177013)
        >>> Tag.get_types(doujin.artist)
        'artist'
        ```
        """
        types = [tag.type for tag in tags]
        return types[0] if len(types) == 1 else types 

    @staticmethod
    def get_names(tags: List[Tag]) -> str or List[str]:
        """
        Return a list of capitalized names corresponding to the passed Tag objects.

        ### Example:
        ```python
        >>> from hentai import Hentai, Tag
        >>> doujin = Hentai(177013)
        >>> Tag.get_names(doujin.artist)
        'Shindol'
        ```
        """
        capitalize_all = lambda sequence: ' '.join([word.capitalize() for word in sequence.split(' ')])
        artists = [capitalize_all(tag.name) for tag in tags]
        return artists[0] if len(artists) == 1 else artists

    @staticmethod
    def get_urls(tags: List[Tag]) -> str or List[str]:
        """
        Return a list of URLs corresponding to the passed Tag objects.
        
        ### Example:
        ```python
        >>> from hentai import Hentai, Tag
        >>> doujin = Hentai(177013)
        >>> Tag.get_urls(doujin.artist)
        '/artist/shindol/'
        ```
        """
        urls = [tag.url for tag in tags]
        return urls[0] if len(urls) == 1 else urls

    @staticmethod
    def get_counts(tags: List[Tag]) -> int or List[int]:
        """
        Return a list of counts (of occurrences) corresponding to the passed Tag objects.

        ### Example:
        ```python
        >>> from hentai import Hentai, Tag
        >>> doujin = Hentai(177013)
        >>> Tag.get_counts(doujin.artist)
        279
        ```
        """
        counts = [tag.count for tag in tags]
        return counts[0] if len(counts) == 1 else counts


@dataclass
class Page:
    """
    A data class that bundles related `Page` properties.
    """
    url: str
    ext: str
    width: int
    height: int

    @property
    def filename(self) -> Path:
        """
        Return the file name for this `Page` as Path object.

        ### Example:
        ```python
        >>> from hentai import Hentai
        >>> doujin = Hentai(177013)
        >>> [page.filename for page in doujin.pages]
        [WindowsPath('1.jpg'), WindowsPath('2.jpg'), ...]
        """
        num = Path(urlparse(self.url).path).name
        return Path(num).with_suffix(self.ext)


@unique
class Sort(Enum):
    """
    Exposed endpoints used to sort queries. Defaults to `Popular`.
    """
    PopularYear = 'popular-year'
    PopularMonth = 'popular-month'
    PopularWeek = 'popular-week'
    PopularToday = 'popular-today'
    Popular = 'popular'
    Date = 'date'


@unique
class Option(Enum):
    """
    Defines export options for the `Hentai` class.
    """
    Raw = 'raw'
    ID = 'id'
    Title = 'title'
    Scanlator = 'scanlator'
    URL = 'url'
    API = 'api'
    MediaID = 'media_id'
    UploadDate = 'upload_date'
    Favorites = 'favorites'
    Tag = 'tag'
    Language = 'language'
    Artist = 'artist'
    Category = 'category'
    Cover = 'cover'
    Thumbnail = 'thumbnail'
    Images = 'images'
    PageCount = 'pages'


@unique
class Format(Enum):
    """
    Title format. In some instances, `Format.Japanese` or `Format.Pretty` return
    `None`.
    """
    English = 'english'
    Japanese = 'japanese'
    Pretty = 'pretty'


@unique
class Extension(Enum):
    """
    Known file extensions used by `nhentai` images.
    """
    JPG = 'j'
    PNG = 'p'
    GIF = 'g'

    @classmethod
    def convert(cls, key: str) -> str:
        """
        Convert Extension enum to its string representation.

        ### Example:
        ```python
        >>> from hentai import Extension
        >>> Extension.convert('j')
        '.jpg'
        ```
        """
        return f".{cls(key).name.lower()}"


class RequestHandler(object):
    """
    Defines a synchronous request handler class.
    """
    _timeout = (3.05, 1)
    _total = 5
    _status_forcelist = [413, 429, 500, 502, 503, 504]
    # sleep between fails = backoff_factor * (2 ** (total - 1))
    _backoff_factor = 1
    _fake = Faker()

    def __init__(self, 
                 timeout: Tuple[float, float]=_timeout, 
                 total: int=_total, 
                 status_forcelist: List[int]=_status_forcelist, 
                 backoff_factor: int=_backoff_factor):
        """
        Instantiates a new session and uses sane default params that can be modified
        later on to change the way `Hentai` object make their requests.
        """
        self.timeout = timeout
        self.total = total        
        self.status_forcelist = status_forcelist
        self.backoff_factor = backoff_factor

    @property
    def retry_strategy(self) -> Retry:
        """
        Return a retry strategy for this session. 
        """
        return Retry(self.total, self.status_forcelist, self.backoff_factor)

    @property
    def session(self) -> Session:
        """
        Return this session object used for making GET and POST requests.
        """
        assert_status_hook = lambda response, *args, **kwargs: response.raise_for_status()
        session = requests.Session()
        session.mount("https://", HTTPAdapter(max_retries = self.retry_strategy))
        session.hooks['response'] = [assert_status_hook]
        session.headers.update({
            "User-Agent" : RequestHandler._fake.chrome(version_from=80, version_to=86, build_from=4100, build_to=4200)
        })
        return session
    
    def get(self, url: str, params: dict=None, **kwargs) -> Response:
        """
        Returns the GET request encoded in `utf-8`.
        """
        response = self.session.get(url, timeout = self.timeout, params = params, proxies=getproxies(), **kwargs)
        response.encoding = 'utf-8'
        return response


class Hentai(RequestHandler):
    """
    # Python Hentai API Wrapper
    Implements a wrapper class around `nhentai`'s RESTful API that inherits from
    `RequestHandler`. Note that the content of this module is generally considered 
    NSFW.
    """
    HOME = "https://nhentai.net/" 
    _URL = urljoin(HOME, '/g/')
    _API = urljoin(HOME, '/api/gallery/')

    def __init__(self, 
                 id: int=0, 
                 timeout: Tuple[float, float]=RequestHandler._timeout, 
                 total: int=RequestHandler._total, 
                 status_forcelist: List[int]=RequestHandler._status_forcelist, 
                 backoff_factor: int=RequestHandler._backoff_factor,
                 json: dict=None):
        """
        Start a request session and parse meta data from `nhentai.net` for this `id`.

        ## Basic Usage:
        ```python
        >>> from hentai import Hentai
        >>> doujin = Hentai(177013)
        >>> print(doujin)
        '[ShindoLA] METAMORPHOSIS (Complete) [English]'
        ```
        """
        if id and not json:
            self.id = id
            super().__init__(timeout, total, status_forcelist, backoff_factor)
            self.handler = RequestHandler(self.timeout, self.total, self.status_forcelist, self.backoff_factor)
            self.url = urljoin(Hentai._URL, str(self.id))
            self.api = urljoin(Hentai._API, str(self.id))
            self.response = self.handler.get(self.api)
            self.json = self.response.json()
        elif not id and json:
            self.json = json
            self.id = Hentai.get_id(self.json)
            self.url = Hentai.get_url(self.json)
            self.api = Hentai.get_api(self.json)
        else:
            raise TypeError('Define either id or json argument, but not both or none')

    def __str__(self) -> str:
        return self.title()

    def __repr__(self) -> str:
        return f"ID({self.id})"
    
    @staticmethod
    def get_id(json: dict) -> int:
        """
        Return the ID of an raw nhentai response object.
        """
        return int(json['id'])

    @staticmethod
    def get_url(json: dict) -> str:
        """
        Return the URL of an raw nhentai response object.
        """
        return urljoin(Hentai._URL, str(Hentai.get_id(json)))

    @staticmethod
    def get_api(json: dict) -> str:
        """
        Return the API access point of an raw nhentai response object.
        """
        return urljoin(Hentai._API, str(Hentai.get_id(json)))

    @staticmethod
    def get_media_id(json: dict) -> int:
        """
        Return the media ID of an raw nhentai response object.
        """
        return int(json['media_id'])

    @property
    def media_id(self) -> int:
        """
        Return the media id of this `Hentai` object.
        """
        return Hentai.get_media_id(self.json)   

    @staticmethod
    def get_title(json: dict, format: Format=Format.English) -> str:
        """
        Return the title of an raw nhentai response object. The format of the title
        defaults to `English`, which is the verbose counterpart to `Pretty`.
        """
        return json['title'].get(format.value)

    def title(self, format: Format=Format.English) -> str:
        """
        Return the title of this `Hentai` object. The format of the title
        defaults to `English`, which is the verbose counterpart to `Pretty`.
        """
        return Hentai.get_title(self.json, format)

    @staticmethod
    def get_scanlator(json: dict) -> str:
        """
        Return the scanlator of an raw nhentai response object. This information
        is often not specified by the provider.
        """
        return json['scanlator']

    @property
    def scanlator(self) -> str:
        """
        Return the scanlator of this `Hentai` object. This information is often 
        not specified by the provider.
        """
        return Hentai.get_scanlator(self.json)

    @staticmethod
    def get_cover(json: dict) -> str:
        """
        Return the cover URL of an raw nhentai response object.
        """
        cover_ext = Extension.convert(json['images']['cover']['t'])
        return f"https://t.nhentai.net/galleries/{Hentai.get_media_id(json)}/cover{cover_ext}"

    @property
    def cover(self) -> str:
        """
        Return the cover URL of this `Hentai` object.
        """
        return Hentai.get_cover(self.json)

    @staticmethod
    def get_thumbnail(json: dict) -> str:
        """
        Return the thumbnail URL of an raw nhentai response object.
        """
        thumb_ext = Extension.convert(json['images']['thumbnail']['t'])
        return f"https://t.nhentai.net/galleries/{Hentai.get_media_id(json)}/thumb{thumb_ext}"

    @property
    def thumbnail(self):
        """
        Return the thumbnail URL of this `Hentai` object.
        """
        return Hentai.get_thumbnail(self.json)

    @staticmethod
    def get_upload_date(json: dict) -> datetime:
        """
        Return the upload date of an raw nhentai response object.
        """
        return datetime.fromtimestamp(json['upload_date'])

    @property
    def upload_date(self) -> datetime:
        """
        Return the upload date of this `Hentai` object.
        """
        return Hentai.get_upload_date(self.json)

    __tag = lambda json, type: [Tag(tag['id'], tag['type'], tag['name'], tag['url'], tag['count']) for tag in json['tags'] if tag['type'] == type]
    
    @staticmethod
    def get_tag(json: dict) -> List[Tag]:
        """
        Return all tags of type tag of an raw nhentai response object.
        """
        return Hentai.__tag(json, 'tag')

    @property
    def tag(self) -> List[Tag]:
        """
        Return all tags of type tag of this `Hentai` object.
        """
        return Hentai.get_tag(self.json)

    @staticmethod
    def get_language(json: dict) -> List[Tag]:
        """
        Return all tags of type language of an raw nhentai response object.
        """
        return Hentai.__tag(json, 'language')

    @property
    def language(self) -> List[Tag]:
        """
        Return all tags of type language of this `Hentai` object.
        """
        return Hentai.get_language(self.json)

    @staticmethod
    def get_artist(json: dict) -> List[Tag]:
        """
        Return all tags of type artist of an raw nhentai response object.
        """
        return Hentai.__tag(json, 'artist')

    @property
    def artist(self) -> List[Tag]:
        """
        Return all tags of type artist of this `Hentai` object.
        """
        return Hentai.get_artist(self.json)

    @staticmethod
    def get_category(json: dict) -> List[Tag]:
        """
        Return all tags of type category of an raw nhentai response object.
        """
        return Hentai.__tag(json, 'category')

    @property
    def category(self) -> List[Tag]:
        """
        Return all tags of type category of this `Hentai` object.
        """
        return Hentai.get_category(self.json)

    @staticmethod
    def get_num_pages(json: dict) -> int:
        """
        Return the total number of pages of an raw nhentai response object.
        """
        return int(json['num_pages'])

    @property
    def num_pages(self) -> int:
        """
        Return the total number of pages of this `Hentai` object.
        """
        return Hentai.get_num_pages(self.json)

    @staticmethod
    def get_num_favorites(json: dict) -> int:
        """
        Return the number of times the raw nhentai response object has been favorited.
        """
        return int(json['num_favorites'])

    @property
    def num_favorites(self) -> int:
        """Return the number of times this `Hentai` object has been favorited."""
        return Hentai.get_num_favorites(self.json)

    @staticmethod
    def get_pages(json: dict) -> List[Page]:
        """
        Return a collection of pages detailing URL, file extension, width an 
        height of an raw nhentai response object.
        """
        pages = json['images']['pages']
        extension = lambda num: Extension.convert(pages[num]['t'])
        image_url = lambda num: f"https://i.nhentai.net/galleries/{Hentai.get_media_id(json)}/{num}{extension(num - 1)}"
        return [Page(image_url(num + 1), Extension.convert(_['t']), _['w'], _['h']) for num, _ in enumerate(pages)]

    @property
    def pages(self) -> List[Page]:
        """
        Return a collection of pages detailing URL, file extension, width an 
        height of this `Hentai` object.
        """
        return Hentai.get_pages(self.json)

    @staticmethod
    def get_image_urls(json: dict) -> List[str]:
        """
        Return all image URLs of an raw nhentai response object, excluding cover and
        thumbnail.
        """
        return [image.url for image in Hentai.get_pages(json)]

    @property
    def image_urls(self) -> List[str]:
        """
        Return all image URLs of this `Hentai` object, excluding cover and thumbnail.
        """
        return Hentai.get_image_urls(self.json)

    def download(self, dest: Path=Path.cwd(), delay: int=0) -> None:
        """
        Download all image URLs of this `Hentai` object to `dest` in a new folder,
        excluding cover and thumbnail. Set a `delay` between each image download 
        in seconds.
        """
        dest = dest.joinpath(self.title(Format.Pretty))
        dest.mkdir(parents=True, exist_ok=True)
        for image_url in self.image_urls:
            response = self.handler.get(image_url, stream=True)
            filename = dest.joinpath(dest.joinpath(image_url).name)
            with open(filename, mode='wb') as file_handler:
                for chunk in response.iter_content(1024):
                    file_handler.write(chunk)
                time.sleep(delay)

    def export(self, filename: Path, options: List[Option]=None) -> None:
        """
        Store user-customized data about this `Hentai` object as a JSON file.
        """
        tmp = []
        tmp.append(self.json)
        Utils.static_export(tmp, filename, options)

    @staticmethod
    def exists(id: int, make_request: bool=True) -> bool:
        """
        Check whether or not the magic number exists on `nhentai.net`, or set 
        `make_request` to `False` to search for validated IDs in an internal file.
        """
        if make_request:
            try:
                return RequestHandler().get(urljoin(Hentai._URL, str(id))).ok        
            except HTTPError:
                return False
        else:
            with resource_path('hentai.data', 'ids.csv') as data_path:
                with open(data_path, mode='r', encoding='utf-8') as file_handler:
                    reader = csv.reader(file_handler)
                    for row in reader:
                        if id == int(row[0]):
                            return True
            return False


class Utils(object):
    """
    # Hentai Utility Library

    This class provides a handful of miscellaneous static methods: 

    ### Example 1
    ```python
    >>> from hentai import Utils
    >>> random_id = Utils.get_random_id()
    >>> # the id changes after each invocation
    >>> print(random_id)
    177013
    ```

    ### Example 2
    ```python
    from hentai import Hentai, Sort, Format, Utils
    >>> # fetches 25 responses per query
    >>> for doujin in Utils.search_by_query('tag:loli', sort=Sort.PopularWeek):
    ...   print(Hentai.get_title(doujin))
    Ikenai Koto ja Nai kara
    Onigashima Keimusho e Youkoso
    Matayurushou to Hitori de Dekiru Himari-chan
    ```
    """
    @staticmethod
    def get_random_id(make_request: bool=True, handler=RequestHandler()) -> int:
        """
        Return a random magic number. Set `make_request` to `False` to use 
        already validated IDs in an internal file.
        """
        if make_request:
            response = handler.session.get(urljoin(Hentai.HOME, 'random'))
            return int(urlparse(response.url).path[3:-1])
        else:
            with resource_path('hentai.data', 'ids.csv') as data_path:
                with open(data_path, mode='r', encoding='utf-8') as file_handler:
                    reader = csv.reader(file_handler)
                    return random.choice([int(row[0]) for row in reader])

    @staticmethod
    def get_random_hentai(make_request: bool=True) -> Hentai:
        """
        Return a random `Hentai` object. Set `make_request` to `False` to use 
        already validated IDs in an internal file.
        """
        return Hentai(Utils.get_random_id(make_request))

    @staticmethod
    def download_queue(ids: List[int], dest: Path=Path.cwd(), delay: int=0) -> None:
        """
        Download all image URLs for multiple magic numbers to `dest` in newly 
        created folders. Set a `delay` between each image download in seconds.
        """
        [Hentai(id).download(dest, delay) for id in ids]

    @staticmethod
    def browse_homepage(start_page: int, end_page: int, handler=RequestHandler()) -> List[dict]:
        """
        Return an iterated list of raw nhentai response objects that are currently 
        featured on the homepage in range of `[start_page, end_page]`.
        """
        if start_page > end_page:
            raise ValueError("Invalid argument passed to function (requires start_page <= end_page).")
        data = []
        for page in range(start_page, end_page + 1):
            payload = { 'page' : page }
            response = handler.get(urljoin(Hentai.HOME, 'api/galleries/all'), params=payload).json()
            data.extend(response['result'])
        return data

    @staticmethod
    def get_homepage(page: int=1, handler=RequestHandler()) -> List[dict]:
        """
        Return an iterated list of raw nhentai response objects that are currently 
        featured on the homepage.
        """
        return Utils.browse_homepage(page, page, handler)

    @staticmethod
    def search_by_query(query: str, page: int=1, sort: Sort=Sort.Popular, handler=RequestHandler()) -> List[dict]:
        """
        Return a list of raw nhentai response objects on page=`page` matching this 
        search `query` sorted by `sort`.
        """
        payload = { 'query' : query, 'page' : page, 'sort' : sort.value }
        response = handler.get(urljoin(Hentai.HOME, '/api/galleries/search'), params=payload).json()
        return response['result']

    @staticmethod
    def search_all_by_query(query: str, sort: Sort=Sort.Popular, handler=RequestHandler()) -> List[dict]:
        """
        Return an iterated list of all raw nhentai response objects matching this 
        search `query` sorted by `sort`.

        ### Example:
        ```python
        >>> from hentai import Utils, Sort, Format
        >>> popular_3d = Utils.search_all_by_query(query="tag:3d", sort=Sort.PopularWeek)
        >>> for doujin in popular_3d:
        ...   print(Hentai.get_title(doujin, format=Format.Pretty))
        A Rebel's Journey:  Chang'e
        COMIC KURiBERON 2019-06 Vol. 80
        Mixed Wrestling Japan 2019
        ```
        """
        data = []
        payload = { 'query' : query, 'page' : 1, 'sort' : sort.value }
        response = handler.get(urljoin(Hentai.HOME, '/api/galleries/search'), params=payload).json()
        for page in range(1, int(response['num_pages']) + 1):
            data.extend(Utils.search_by_query(query, page, sort, handler))
        return data

    @staticmethod
    def static_export(iterable, filename: Path, options: List[Option]=None) -> None:
        """
        Store user-customized data of raw nhentai response objects as a JSON file.

        ### Example:
        ```python
        >>> from hentai import Utils, Sort, Option
        >>> popular_loli = Utils.search_by_query('tag:loli', sort=Sort.PopularWeek)
        >>> # filter file content using options
        >>> custom = [Option.ID, Option.Title, Option.UploadDate]
        >>> Utils.static_export(popular_loli, 'popular_loli.json', options=custom)
        ```
        """
        if options is None:
            Utils.static_export(iterable, filename, options=[opt for opt in Option if opt.value != 'raw'])
        elif Option.Raw in options:
            with open(filename, mode='w', encoding='utf-8') as file_handler:
                json.dump(iterable, file_handler)
        else:
            content = { 'result' : [] }
            for index, doujin in enumerate(iterable):
                data = {}
                if Option.ID in options:
                    data['id'] = Hentai.get_id(doujin)
                if Option.Title in options:
                    data['title'] = Hentai.get_title(doujin, format=Format.Pretty)
                if Option.Scanlator in options:
                    data['scanlator'] = Hentai.get_scanlator(doujin)
                if Option.URL in options:
                    data['url'] = Hentai.get_url(doujin)
                if Option.API in options:
                    data['api'] = Hentai.get_api(doujin)
                if Option.MediaID in options:
                    data['media_id'] = Hentai.get_media_id(doujin)
                if Option.UploadDate in options:
                    epos = Hentai.get_upload_date(doujin).replace(tzinfo=timezone.utc).timestamp()
                    data['upload_date'] = round(epos)
                if Option.Favorites in options:
                    data['favorites'] = Hentai.get_num_favorites(doujin)
                if Option.Tag in options:
                    data['tag'] = Tag.get_names(Hentai.get_tag(doujin))
                if Option.Language in options:
                    data['language'] = Tag.get_names(Hentai.get_language(doujin))
                if Option.Artist in options:
                    data['artist'] = Tag.get_names(Hentai.get_artist(doujin))
                if Option.Category in options:
                    data['category'] = Tag.get_names(Hentai.get_category(doujin))
                if Option.Cover in options:
                    data['cover'] = Hentai.get_cover(doujin)
                if Option.Thumbnail in options:
                    data['thumbnail'] = Hentai.get_thumbnail(doujin)
                if Option.Images in options:
                    data['images'] = Hentai.get_image_urls(doujin)
                if Option.PageCount in options:
                    data['pages'] = Hentai.get_num_pages(doujin)
                content['result'].insert(index, data)
            with open(filename, mode='w', encoding='utf-8') as file_handler:
                json.dump(content, file_handler)

