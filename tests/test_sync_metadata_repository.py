from datetime import datetime, timezone

from db import Database
from db.sync_metadata_repository import SyncMetadataRepository
from db.user_repository import UserRepository


def main():

    database = Database()

    user_repository = UserRepository(database)

    sync_repository = SyncMetadataRepository(database)

    # --------------------------------------------------
    # 1. Get existing user
    # --------------------------------------------------

    user = user_repository.find_by_username(
        "Priyadrasta_Raut"
    )

    if user is None:

        print(
            "User not found. Run the real sync first."
        )

        return

    user_id = user["id"]

    print(
        f"Using user: "
        f"{user['username']} "
        f"(id={user_id})"
    )

    # --------------------------------------------------
    # 2. get_by_user_id()
    # --------------------------------------------------

    print("\n========== GET BEFORE SYNC ==========")

    result = sync_repository.get_by_user_id(
        user_id
    )

    print(result)

    # --------------------------------------------------
    # 3. start_sync()
    # --------------------------------------------------

    print("\n========== START SYNC ==========")

    result = sync_repository.start_sync(
        user_id
    )

    print(result)

    # --------------------------------------------------
    # 4. get_by_user_id() again
    # --------------------------------------------------

    print("\n========== GET AFTER START ==========")

    result = sync_repository.get_by_user_id(
        user_id
    )

    print(result)

    # --------------------------------------------------
    # 5. complete_sync()
    # --------------------------------------------------

    print("\n========== COMPLETE SYNC ==========")

    result = sync_repository.complete_sync(
        user_id=user_id,
        submission_id="123456789",
        submission_timestamp=datetime.now(
            timezone.utc
        ),
    )

    print(result)

    # --------------------------------------------------
    # 6. Verify completed state
    # --------------------------------------------------

    print("\n========== GET AFTER COMPLETE ==========")

    result = sync_repository.get_by_user_id(
        user_id
    )

    print(result)

    # --------------------------------------------------
    # 7. Test failure
    # --------------------------------------------------

    print("\n========== START SECOND SYNC ==========")

    sync_repository.start_sync(
        user_id
    )

    print(
        sync_repository.get_by_user_id(
            user_id
        )
    )

    print("\n========== FAIL SYNC ==========")

    sync_repository.fail_sync(
        user_id=user_id,
        error="Simulated synchronization failure",
    )

    print(
        sync_repository.get_by_user_id(
            user_id
        )
    )


if __name__ == "__main__":
    main()