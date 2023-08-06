from typing import Tuple
from sequence_transfer.sequence import Sequence
from sequence_transfer.sequence_transfer import SequenceTransfer


def is_separator(text: str, index: int) -> bool:
    if text[index + 1] == "#":
        return True
    else:
        return False


def remove_bert_separator(text: str) -> Tuple[str, SequenceTransfer]:
    output = ""

    i = 0
    j = 0
    transfers = []

    while i < len(text):
        char = text[i]
        if char == "#" and is_separator(text, i):
            transfers.append((Sequence(i, i + 3), Sequence(j, j + 1)))
            output += text[i + 2]
            i += 3
            j += 1
        else:
            transfers.append((Sequence(i, i + 1), Sequence(j, j + 1)))
            output += text[i]
            i += 1
            j += 1

    transfer = SequenceTransfer(
        Sequence(0, len(text)),
        Sequence(0, len(output)),
        transfers
    )

    return output, transfer
