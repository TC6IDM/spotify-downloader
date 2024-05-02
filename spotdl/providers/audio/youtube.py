"""
Youtube module for downloading and searching songs.
"""

import json
from typing import Any, Dict, List, Optional
import jsonpickle

from pytube import Search
from pytube import YouTube as PyTube

from spotdl.providers.audio.base import AudioProvider
from spotdl.types.result import Result

__all__ = ["YouTube"]


class YouTube(AudioProvider):
    """
    YouTube audio provider class
    """

    SUPPORTS_ISRC = False
    GET_RESULTS_OPTS: List[Dict[str, Any]] = [{}]

    def get_results(
        self, search_term: str, *_args, **_kwargs
    ) -> List[Result]:  # pylint: disable=W0221
        """
        Get results from YouTube

        ### Arguments
        - search_term: The search term to search for.
        - args: Unused.
        - kwargs: Unused.

        ### Returns
        - A list of YouTube results if found, None otherwise.
        """
        
        search_results: Optional[List[PyTube]] = Search(search_term).results

        if not search_results:
            return []

        results = []
        # print("Enter")
        # i=0
        for result in search_results:
            # i+=1
            # jsondata = jsonpickle.encode(result)
            # with open(f"{i}tt.json", "w") as outfile:
            #     outfile.write(json.dumps(json.loads(jsondata), indent=4))
            
            
            if result.watch_url:
                # print(result.watch_url)
                try:
                    duration = result.length
                except Exception:
                    duration = 0

                try:
                    views = result.views
                except Exception:
                    views = 0

                results.append(
                    Result(
                        source=self.name,
                        url=result.watch_url,
                        verified=False,
                        name=result.title,
                        duration=duration,
                        author=result.author,
                        search_query=search_term,
                        views=views,
                        result_id=result.video_id,
                    )
                )
        return results
