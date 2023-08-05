from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    container_id: str,
    containable_id: str,
) -> Dict[str, Any]:
    url = "{}/containers/{container_id}/contents/{containable_id}".format(
        client.base_url, container_id=container_id, containable_id=containable_id
    )

    headers: Dict[str, Any] = client.get_headers()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, NotFoundError]]:
    if response.status_code == 200:
        return None
    if response.status_code == 404:
        return NotFoundError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    container_id: str,
    containable_id: str,
) -> Response[Union[None, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        container_id=container_id,
        containable_id=containable_id,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    container_id: str,
    containable_id: str,
) -> Optional[Union[None, NotFoundError]]:
    """ Delete a container content """

    return sync_detailed(
        client=client,
        container_id=container_id,
        containable_id=containable_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    container_id: str,
    containable_id: str,
) -> Response[Union[None, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        container_id=container_id,
        containable_id=containable_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    container_id: str,
    containable_id: str,
) -> Optional[Union[None, NotFoundError]]:
    """ Delete a container content """

    return (
        await asyncio_detailed(
            client=client,
            container_id=container_id,
            containable_id=containable_id,
        )
    ).parsed
