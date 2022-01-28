from __future__ import annotations
import asyncio
from typing import Any
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


def gaussian_blur_1d(
    signal: npt.ArrayLike,
    sigma: int,
    truncate: float = 4.0
):
    N = len(signal)
    half_len = (N- 1.) / 2
    x_kernel = np.linspace(-half_len, half_len, N)
    x_kernel = np.arange(-sigma * truncate, sigma * truncate + 1)
    kernel = normalize_array(gauss_pdf(x_kernel, 0, sigma))
    return np.convolve(signal, kernel, mode='same')


def gauss_pdf(
    x: Any,
    mu: float,
    sigma: float
)-> Any:
    s2 = sigma * np.sqrt(2)
    return np.exp(-((x - mu) / s2) ** 2) / (s2 * np.sqrt(2))



class ClientSessionWrapper:
    _instance: ClientSessionWrapper = None

    @staticmethod
    def get_instance() -> ClientSessionWrapper:
        if ClientSessionWrapper._instance is None:
            ClientSessionWrapper._instance = ClientSessionWrapper()
        return ClientSessionWrapper._instance

    def __init__(self) -> None:
        try:
            asyncio.get_running_loop() # purely to check for an active event loop
            self.session = ClientSession()
        except RuntimeError:
            raise RuntimeError("ClientSessionWrapper tried to construct a ClientSession "
                "outside of an event loop! Use utils.get_client_session() instead")

    def __del__(self) -> None:
        if self.session is not None:
            asyncio.run(self.session.close())

