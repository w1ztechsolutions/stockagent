"""TTL-aware in-memory session store used by the agent memory tool."""

from __future__ import annotations

import threading
import time
from typing import Any

from app.providers.base import ChatMessage

SESSION_TTL = 30 * 60  # seconds


class SessionMemory:
    def __init__(self, ttl: int = SESSION_TTL) -> None:
        self._sessions: dict[str, dict[str, Any]] = {}
        self._lock = threading.Lock()
        self.ttl = ttl

    def _now(self) -> float:
        return time.monotonic()

    def _purge_if_expired(self, session_id: str) -> None:
        entry = self._sessions.get(session_id)
        if entry and self._now() - entry["updated_at"] > self.ttl:
            self._sessions.pop(session_id, None)

    def add(self, session_id: str, message: ChatMessage) -> None:
        with self._lock:
            self._purge_if_expired(session_id)
            entry = self._sessions.get(session_id)
            if entry is None:
                entry = {"messages": [], "updated_at": self._now()}
                self._sessions[session_id] = entry
            entry["messages"].append(message)
            entry["updated_at"] = self._now()

    def get_history(self, session_id: str) -> list[ChatMessage]:
        with self._lock:
            self._purge_if_expired(session_id)
            entry = self._sessions.get(session_id)
            return list(entry["messages"]) if entry else []

    def clear(self, session_id: str) -> None:
        with self._lock:
            self._sessions.pop(session_id, None)

    def active_sessions(self) -> list[str]:
        with self._lock:
            now = self._now()
            valid: list[str] = []
            for session_id, entry in list(self._sessions.items()):
                if now - entry["updated_at"] > self.ttl:
                    self._sessions.pop(session_id, None)
                else:
                    valid.append(session_id)
            return valid


MEMORY = SessionMemory()