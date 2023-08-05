from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.assay_run import AssayRun
from ...models.bad_request_error import BadRequestError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    assay_run_id: str,
) -> Dict[str, Any]:
    url = "{}/assay-runs/{assay_run_id}".format(client.base_url, assay_run_id=assay_run_id)

    headers: Dict[str, Any] = client.get_headers()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[AssayRun, BadRequestError]]:
    if response.status_code == 200:
        return AssayRun.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[AssayRun, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    assay_run_id: str,
) -> Response[Union[AssayRun, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        assay_run_id=assay_run_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    assay_run_id: str,
) -> Optional[Union[AssayRun, BadRequestError]]:
    """  """

    return sync_detailed(
        client=client,
        assay_run_id=assay_run_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    assay_run_id: str,
) -> Response[Union[AssayRun, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        assay_run_id=assay_run_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    assay_run_id: str,
) -> Optional[Union[AssayRun, BadRequestError]]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            assay_run_id=assay_run_id,
        )
    ).parsed
