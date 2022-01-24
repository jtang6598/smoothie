import numpy as np
import numpy.typing as npt
from aiohttp import ClientSession

async def get_client_session():
    """
    Util function to keep track of a single ClientSession instance. This also 
    serves to ensure that the ClientSession is initialized in a coroutine for safety.
    """
    if ClientSessionWrapper.session is None:
        ClientSessionWrapper.session = ClientSession()
    return ClientSessionWrapper.session

def normalize_array(arr: npt.ArrayLike) -> npt.ArrayLike:
    """
    Normalize a numpy array so that its elements sum to 1.
    """
    return arr / np.sum(arr)

class ClientSessionWrapper:
    session: ClientSession

