"""Statistics tracking for MCP Assist."""
from __future__ import annotations

import time
import logging
from dataclasses import dataclass, field
from typing import Optional, Callable, Any
from collections import deque
from datetime import datetime, date

_LOGGER = logging.getLogger(__name__)


@dataclass
class ResponseTimeTracker:
    """Tracks response times with rolling averages."""

    # Maximum number of samples to keep for rolling average
    max_samples: int = 100
    _fast_path_times: deque = field(default_factory=lambda: deque(maxlen=100))
    _llm_times: deque = field(default_factory=lambda: deque(maxlen=100))

    # Last recorded values
    fast_path_last: float = 0.0
    llm_last: float = 0.0

    def record_fast_path(self, duration_ms: float) -> None:
        """Record a Fast Path response time."""
        self._fast_path_times.append(duration_ms)
        self.fast_path_last = duration_ms

    def record_llm(self, duration_ms: float) -> None:
        """Record an LLM response time."""
        self._llm_times.append(duration_ms)
        self.llm_last = duration_ms

    @property
    def fast_path_avg(self) -> float:
        """Calculate average Fast Path response time."""
        if not self._fast_path_times:
            return 0.0
        return sum(self._fast_path_times) / len(self._fast_path_times)

    @property
    def llm_avg(self) -> float:
        """Calculate average LLM response time."""
        if not self._llm_times:
            return 0.0
        return sum(self._llm_times) / len(self._llm_times)

    def to_dict(self) -> dict:
        """Export response time statistics as dictionary."""
        return {
            "fast_path_avg_response_time": round(self.fast_path_avg, 1),
            "fast_path_last_response_time": round(self.fast_path_last, 1),
            "llm_avg_response_time": round(self.llm_avg, 1),
            "llm_last_response_time": round(self.llm_last, 1),
        }


class MCPAssistStatistics:
    """Central statistics manager for MCP Assist."""

    def __init__(self) -> None:
        """Initialize statistics manager."""
        self._response_times = ResponseTimeTracker()

        # Counters
        self._fast_path_hits: int = 0
        self._fast_path_misses: int = 0
        self._pre_resolve_hits: int = 0
        self._pre_resolve_attempts: int = 0
        self._llm_calls: int = 0
        self._llm_errors: int = 0
        self._tokens_used: int = 0

        # Daily tracking
        self._current_date: date = date.today()
        self._requests_today: int = 0
        self._llm_calls_today: int = 0
        self._tokens_today: int = 0

        # Status
        self._status: str = "online"
        self._last_request_time: Optional[datetime] = None

        # Listeners for sensor updates
        self._listeners: list[Callable[[], None]] = []

    def add_listener(self, callback: Callable[[], None]) -> Callable[[], None]:
        """Add a listener that gets called when stats change."""
        self._listeners.append(callback)

        def remove_listener():
            if callback in self._listeners:
                self._listeners.remove(callback)

        return remove_listener

    def _notify_listeners(self) -> None:
        """Notify all listeners of stats change."""
        for listener in self._listeners:
            try:
                listener()
            except Exception as e:
                _LOGGER.warning("Error notifying stats listener: %s", e)

    def _check_date_rollover(self) -> None:
        """Reset daily counters if date has changed."""
        today = date.today()
        if today != self._current_date:
            _LOGGER.info("Date rollover detected, resetting daily counters")
            self._current_date = today
            self._requests_today = 0
            self._llm_calls_today = 0
            self._tokens_today = 0

    def record_request(self) -> None:
        """Record a new request."""
        self._check_date_rollover()
        self._requests_today += 1
        self._last_request_time = datetime.now()
        self._notify_listeners()

    def record_fast_path_hit(self, duration_ms: float) -> None:
        """Record a successful Fast Path execution."""
        self._fast_path_hits += 1
        self._response_times.record_fast_path(duration_ms)
        self._notify_listeners()

    def record_fast_path_miss(self) -> None:
        """Record a Fast Path miss (fallback to LLM)."""
        self._fast_path_misses += 1
        self._notify_listeners()

    def record_pre_resolve_attempt(self, success: bool) -> None:
        """Record a pre-resolve attempt."""
        self._pre_resolve_attempts += 1
        if success:
            self._pre_resolve_hits += 1
        self._notify_listeners()

    def record_llm_call(self, duration_ms: float, tokens: int = 0) -> None:
        """Record an LLM call."""
        self._check_date_rollover()
        self._llm_calls += 1
        self._llm_calls_today += 1
        self._tokens_used += tokens
        self._tokens_today += tokens
        self._response_times.record_llm(duration_ms)
        self._notify_listeners()

    def record_llm_error(self) -> None:
        """Record an LLM error."""
        self._llm_errors += 1
        self._notify_listeners()

    def set_status(self, status: str) -> None:
        """Set the current status."""
        self._status = status
        self._notify_listeners()

    @property
    def fast_path_rate(self) -> float:
        """Calculate Fast Path success rate as percentage."""
        total = self._fast_path_hits + self._fast_path_misses
        if total == 0:
            return 0.0
        return round((self._fast_path_hits / total) * 100, 1)

    @property
    def pre_resolve_rate(self) -> float:
        """Calculate pre-resolve success rate as percentage."""
        if self._pre_resolve_attempts == 0:
            return 0.0
        return round((self._pre_resolve_hits / self._pre_resolve_attempts) * 100, 1)

    def get_stats(self) -> dict[str, Any]:
        """Get all statistics as a dictionary."""
        self._check_date_rollover()
        return {
            # Status
            "status": self._status,
            "last_request_time": self._last_request_time.isoformat() if self._last_request_time else None,

            # Response times
            **self._response_times.to_dict(),

            # Fast Path
            "fast_path_hits": self._fast_path_hits,
            "fast_path_misses": self._fast_path_misses,
            "fast_path_rate": self.fast_path_rate,

            # Pre-resolve
            "pre_resolve_hits": self._pre_resolve_hits,
            "pre_resolve_attempts": self._pre_resolve_attempts,
            "pre_resolve_rate": self.pre_resolve_rate,

            # LLM
            "llm_calls_total": self._llm_calls,
            "llm_calls_today": self._llm_calls_today,
            "llm_errors": self._llm_errors,
            "tokens_used_total": self._tokens_used,
            "tokens_used_today": self._tokens_today,

            # Daily
            "requests_today": self._requests_today,
        }


class TimingContext:
    """Context manager for timing operations."""

    def __init__(
        self,
        stats: MCPAssistStatistics,
        operation_type: str,
        tokens_callback: Optional[Callable[[], int]] = None,
    ):
        """Initialize timing context.

        Args:
            stats: The statistics manager
            operation_type: Either "fast_path" or "llm"
            tokens_callback: Optional callback to get token count after operation
        """
        self._stats = stats
        self._operation_type = operation_type
        self._tokens_callback = tokens_callback
        self._start_time: Optional[float] = None

    def __enter__(self) -> "TimingContext":
        """Start timing."""
        self._start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Stop timing and record."""
        if self._start_time is not None:
            duration_ms = (time.perf_counter() - self._start_time) * 1000

            if self._operation_type == "fast_path":
                self._stats.record_fast_path_hit(duration_ms)
            elif self._operation_type == "llm":
                tokens = 0
                if self._tokens_callback:
                    try:
                        tokens = self._tokens_callback()
                    except Exception:
                        pass
                self._stats.record_llm_call(duration_ms, tokens)

        return False

    def mark_failed(self) -> None:
        """Mark operation as failed (don't record timing)."""
        self._start_time = None
