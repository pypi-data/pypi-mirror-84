from typing import Any, Dict, Optional, cast

import attr

from ..models.fields import Fields
from ..types import UNSET


@attr.s(auto_attribs=True)
class LocationUpdate:
    """  """

    fields: Optional[Fields] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    parent_storage_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.fields is UNSET:
            fields = UNSET
        else:
            fields = self.fields.to_dict() if self.fields else None

        name = self.name
        parent_storage_id = self.parent_storage_id

        properties: Dict[str, Any] = dict()

        if fields is not UNSET:
            properties["fields"] = fields
        if name is not UNSET:
            properties["name"] = name
        if parent_storage_id is not UNSET:
            properties["parentStorageId"] = parent_storage_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "LocationUpdate":
        fields = None
        if d.get("fields") is not None:
            fields = Fields.from_dict(cast(Dict[str, Any], d.get("fields")))

        name = d.get("name")

        parent_storage_id = d.get("parentStorageId")

        return LocationUpdate(
            fields=fields,
            name=name,
            parent_storage_id=parent_storage_id,
        )
