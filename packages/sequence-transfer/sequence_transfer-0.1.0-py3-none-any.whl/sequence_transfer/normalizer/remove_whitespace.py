import unicodedata
from typing import Tuple
from sequence_transfer.sequence import Sequence
from sequence_transfer.sequence_transfer import SequenceTransfer


def is_whitespace(char):
    if char == " " or char == "\t" or char == "\n" or char == "\r":
        return True
    cat = unicodedata.category(char)
    if cat == "Zs":
        return True
    return False


def remove_whitespace(text: str) -> Tuple[str, SequenceTransfer]:
    output = ''
    transfers = []
    for i, char in enumerate(text):
        if not is_whitespace(char):
            transfers.append((Sequence(i, i+1), Sequence(len(output), len(output) + 1)))
            output += char
        else:
            transfers.append((Sequence(i, i+1), Sequence(len(output), len(output))))
    transfer = SequenceTransfer(
        Sequence(0, len(text)),
        Sequence(0, len(output)),
        transfers
    )
    return output, transfer
