"""Simple in-memory context storage for CAG."""

from threading import RLock


class ContextStore:
    """Stores context values grouped by user_id.

    This implementation is intentionally small and volatile: data lives only
    while the Python process is running. It is useful for the exercise,
    demos, and unit tests, but not for production persistence.
    """

    def __init__(self):
        self._data = {}
        self._lock = RLock()

    def save(self, user_id, key, value):
        """Save or update a context item for one user.

        Returns True when the value is stored successfully.
        """
        if not user_id:
            raise ValueError("user_id is required")
        if not key:
            raise ValueError("key is required")
        if value is None:
            raise ValueError("value is required")

        normalized_user_id = str(user_id)
        normalized_key = str(key)

        with self._lock:
            self._data.setdefault(normalized_user_id, {})[normalized_key] = value

        return True

    def list_for_user(self, user_id):
        """Return all context items for a user as API-friendly dictionaries."""
        if not user_id:
            return []

        normalized_user_id = str(user_id)

        with self._lock:
            user_context = dict(self._data.get(normalized_user_id, {}))

        return [
            {"key": key, "value": value}
            for key, value in user_context.items()
        ]