from fastapi import Depends, FastAPI

from services.sync_service import SyncService
from api.dependencies import get_sync_service


app = FastAPI()


@app.post("/internal/users/{username}/sync")
def sync_user(
    username: str,
    sync_service: SyncService = Depends(get_sync_service),
):

    return sync_service.sync_user(
        username
    )

