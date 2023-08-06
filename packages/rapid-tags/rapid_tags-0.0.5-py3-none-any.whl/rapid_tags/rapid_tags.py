# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Union
from urllib.parse import quote
import random, json

# Pip
from kcu import request

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- class: RapidTags ------------------------------------------------------------ #

class RapidTags:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        proxy: Optional[Union[List[str], str]] = None,
        user_agent: Optional[str] = None
    ):
        self.proxy = proxy
        self.user_agent = user_agent


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def get_tags(
        self,
        title: str,
        proxy: Optional[Union[List[str], str]] = None,
        user_agent: Optional[str] = None,
        debug: bool = False
    ) -> Optional[List[str]]:
        return RapidTags.get_tags_cls(title, proxy or self.proxy, user_agent or self.user_agent, debug=debug)

    @classmethod
    def get_tags_cls(
        cls,
        title: str,
        proxy: Optional[Union[List[str], str]] = None,
        user_agent: Optional[str] = None,
        debug: bool = False
    ) -> Optional[List[str]]:
        try:
            if type(proxy) == list:
                proxy = random.choice(proxy) if len(proxy) > 0 else None
            
            return [t.replace('\\', '') for t in request.get(
                'https://rapidtags.io/api/generator?query=' + quote(title),
                headers={
                    'Host': 'rapidtags.io',
                    'Accept': 'application/json',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Referer': 'https://rapidtags.io/generator',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
                    'TE': 'Trailers',
                    'Upgrade-Insecure-Requests': '1'
                },
                max_request_try_count=1,
                user_agent=user_agent,
                proxy=proxy,
                debug=debug
            ).json()['tags']]
        except Exception as e:
            if debug:
                print(e)

            return None


# ---------------------------------------------------------------------------------------------------------------------------------------- #s