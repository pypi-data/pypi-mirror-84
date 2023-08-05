from typing import Any, Dict, List, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class Dropdown:
    """  """

    options: Optional[List[Dict[Any, Any]]] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.options is None:
            options = None
        elif self.options is UNSET:
            options = UNSET
        else:
            options = []
            for options_item_data in self.options:
                options_item = options_item_data

                options.append(options_item)

        name = self.name
        id = self.id

        properties: Dict[str, Any] = dict()

        if options is not UNSET:
            properties["options"] = options
        if name is not UNSET:
            properties["name"] = name
        if id is not UNSET:
            properties["id"] = id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Dropdown":
        options = []
        for options_item_data in d.get("options") or []:
            options_item = options_item_data

            options.append(options_item)

        name = d.get("name")

        id = d.get("id")

        return Dropdown(
            options=options,
            name=name,
            id=id,
        )
