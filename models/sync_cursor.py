from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SyncCursor:

    submission_id: str | None = None

    submission_timestamp: datetime | None = None

    @property
    def exists(self) -> bool:
        return self.submission_id is not None