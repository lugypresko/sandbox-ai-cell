from collections import deque
from typing import Deque, Iterable, Tuple

from ..models.signals import SignalPoint


class EvidenceBuffer:
    def __init__(self, maxlen: int) -> None:
        if maxlen < 2:
            raise ValueError("maxlen must be >= 2")
        self._items: Deque[SignalPoint] = deque(maxlen=maxlen)

    def add(self, sample: SignalPoint) -> None:
        if self._items and sample.timestamp < self._items[-1].timestamp:
            raise ValueError("timestamps must be non-decreasing")
        self._items.append(sample)

    def extend(self, samples: Iterable[SignalPoint]) -> None:
        for sample in samples:
            self.add(sample)

    def samples(self) -> Tuple[SignalPoint, ...]:
        return tuple(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def is_full(self) -> bool:
        return len(self._items) == self._items.maxlen
