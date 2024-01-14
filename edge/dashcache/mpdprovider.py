from abc import ABC, abstractmethod

from xml.etree import ElementTree
from xml.etree.ElementTree import Element


from typing import List, Literal, Dict

from mpd import MPD



class MPDProvider(ABC):
    @property
    @abstractmethod
    def mpd(self) -> MPD:
        pass

    @abstractmethod
    async def start(self, mpd_url):
        """
        Start the provider service

        Parameters
        ----------
        mpd_url
        """
        pass

    @abstractmethod
    async def stop(self):
        """
        Stop the repeated updates if there is one
        """
        pass


class MPDProviderImpl(MPDProvider):
    raise NotImplementedError
