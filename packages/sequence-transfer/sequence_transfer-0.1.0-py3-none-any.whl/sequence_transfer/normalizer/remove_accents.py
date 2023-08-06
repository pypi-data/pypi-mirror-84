import unicodedata
from typing import Tuple
from sequence_transfer.sequence import Sequence
from sequence_transfer.sequence_transfer import SequenceTransfer


def remove_accents(text: str) -> Tuple[str, SequenceTransfer]:
    output = ''
    transfers = []
    for i, char in enumerate(text):
        normalized = unicodedata.normalize("NFD", char)
        without_accent = ''
        for char2 in normalized:
            cat = unicodedata.category(char2)
            if cat == "Mn":
                continue
            without_accent += char2

        else:
            transfers.append((
                Sequence(i, i + 1),
                Sequence(len(output), len(output) + len(without_accent))
            ))
        output += without_accent

    transfer = SequenceTransfer(
        Sequence(0, len(text)),
        Sequence(0, len(output)),
        transfers
    )
    return output, transfer
