from typing import Any, Dict, Optional, cast

import httpx

from ...client import Client
from ...models.project_list import ProjectList
from ...models.sort import Sort
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
    sort: Optional[Sort] = Sort.MODIFIEDAT,
    archive_reason: Optional[str] = None,
    ids: Optional[str] = None,
) -> Dict[str, Any]:
    url = "{}/projects".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    if sort is UNSET:
        json_sort = UNSET
    else:
        json_sort = sort.value if sort else None

    params: Dict[str, Any] = {}
    if next_token is not None:
        params["nextToken"] = next_token
    if page_size is not None:
        params["pageSize"] = page_size
    if sort is not None:
        params["sort"] = json_sort
    if archive_reason is not None:
        params["archiveReason"] = archive_reason
    if ids is not None:
        params["ids"] = ids

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[ProjectList]:
    if response.status_code == 200:
        return ProjectList.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[ProjectList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
    sort: Optional[Sort] = Sort.MODIFIEDAT,
    archive_reason: Optional[str] = None,
    ids: Optional[str] = None,
) -> Response[ProjectList]:
    kwargs = _get_kwargs(
        client=client,
        next_token=next_token,
        page_size=page_size,
        sort=sort,
        archive_reason=archive_reason,
        ids=ids,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
    sort: Optional[Sort] = Sort.MODIFIEDAT,
    archive_reason: Optional[str] = None,
    ids: Optional[str] = None,
) -> Optional[ProjectList]:
    """  """

    return sync_detailed(
        client=client,
        next_token=next_token,
        page_size=page_size,
        sort=sort,
        archive_reason=archive_reason,
        ids=ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
    sort: Optional[Sort] = Sort.MODIFIEDAT,
    archive_reason: Optional[str] = None,
    ids: Optional[str] = None,
) -> Response[ProjectList]:
    kwargs = _get_kwargs(
        client=client,
        next_token=next_token,
        page_size=page_size,
        sort=sort,
        archive_reason=archive_reason,
        ids=ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
    sort: Optional[Sort] = Sort.MODIFIEDAT,
    archive_reason: Optional[str] = None,
    ids: Optional[str] = None,
) -> Optional[ProjectList]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            next_token=next_token,
            page_size=page_size,
            sort=sort,
            archive_reason=archive_reason,
            ids=ids,
        )
    ).parsed
