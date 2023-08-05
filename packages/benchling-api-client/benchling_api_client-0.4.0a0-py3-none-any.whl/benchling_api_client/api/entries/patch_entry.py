from typing import Any, Dict, Optional, cast

import httpx

from ...client import Client
from ...models.entry import Entry
from ...models.entry_patch import EntryPatch
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    entry_id: str,
    json_body: EntryPatch,
) -> Dict[str, Any]:
    url = "{}/entries/{entry_id}".format(client.base_url, entry_id=entry_id)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Entry]:
    if response.status_code == 200:
        return Entry.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Entry]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    entry_id: str,
    json_body: EntryPatch,
) -> Response[Entry]:
    kwargs = _get_kwargs(
        client=client,
        entry_id=entry_id,
        json_body=json_body,
    )

    response = httpx.patch(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    entry_id: str,
    json_body: EntryPatch,
) -> Optional[Entry]:
    """  """

    return sync_detailed(
        client=client,
        entry_id=entry_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    entry_id: str,
    json_body: EntryPatch,
) -> Response[Entry]:
    kwargs = _get_kwargs(
        client=client,
        entry_id=entry_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    entry_id: str,
    json_body: EntryPatch,
) -> Optional[Entry]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            entry_id=entry_id,
            json_body=json_body,
        )
    ).parsed
