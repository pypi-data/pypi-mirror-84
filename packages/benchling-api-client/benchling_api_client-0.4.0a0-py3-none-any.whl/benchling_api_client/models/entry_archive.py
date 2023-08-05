from typing import Any, Dict, List

import attr

from ..models.reason import Reason


@attr.s(auto_attribs=True)
class EntryArchive:
    """  """

    entry_ids: List[str]
    reason: Reason

    def to_dict(self) -> Dict[str, Any]:
        entry_ids = self.entry_ids

        reason = self.reason.value

        properties: Dict[str, Any] = dict()

        properties["entryIds"] = entry_ids
        properties["reason"] = reason
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryArchive":
        entry_ids = d["entryIds"]

        reason = Reason(d["reason"])

        return EntryArchive(
            entry_ids=entry_ids,
            reason=reason,
        )
