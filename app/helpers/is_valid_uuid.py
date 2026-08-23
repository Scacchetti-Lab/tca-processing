from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uuid import UUID

def is_valid_uuid(uuid_string):
    try:
        UUID(uuid_string)
        return True
    except ValueError:
        return False