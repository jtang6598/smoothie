from __future__ import annotations
import asyncio
import numpy as np
import numpy.typing as npt
from aiohttp import ClientSession


async def get_client_session():
    """
    Util function to keep track of a single ClientSession instance. This also 
    serves to ensure that the ClientSession is initialized in a coroutine for safety.
    """
    return ClientSessionWrapper.get_instance().session


def normalize_array(arr: npt.ArrayLike) -> npt.ArrayLike:
    """
    Normalize a numpy array so that its elements sum to 1.
    """
    return arr / np.sum(arr)


class ClientSessionWrapper:
    _instance: ClientSessionWrapper = None

    @staticmethod
    def get_instance() -> ClientSessionWrapper:
        if ClientSessionWrapper._instance is None:
            ClientSessionWrapper._instance = ClientSessionWrapper()
        return ClientSessionWrapper._instance

    def __init__(self) -> None:
        self.session = ClientSession()

    def __del__(self) -> None:
        if self.session is not None:
            asyncio.run(self.session.close())

