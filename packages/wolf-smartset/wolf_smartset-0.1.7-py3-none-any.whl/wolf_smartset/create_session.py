import logging

from httpx import AsyncClient, Headers

from wolf_smartset import constants
from wolf_smartset.helpers import bearer_header

_LOGGER = logging.getLogger(__name__)


async def create_session(session: AsyncClient, token: str):
    resp = await session.post(constants.BASE_URL + "/api/portal/CreateSession2",
                              headers=Headers({**bearer_header(token),
                                               **{"Content-Type": "application/json", "Content-Length": "0"}}))

    json = resp.json()
    _LOGGER.debug('Create Session response: %s', json)
    return json['BrowserSessionId']
