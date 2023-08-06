from typing import Tuple
from sequence_transfer.sequence_transfer import SequenceTransfer
from sequence_transfer.sequence import Sequence


def to_lower(text: str) -> Tuple[str, SequenceTransfer]:
    sequence = Sequence(0, len(text))
    transfer = SequenceTransfer(
        sequence,
        sequence,
        [(sequence, sequence)]
    )
    return text.lower(), transfer
