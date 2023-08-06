from typing import List
from sequence_transfer.sequence_transfer import SequenceTransfer
from sequence_transfer.sequence import Sequence
from sequence_transfer.sequence import Token


def token_to_text_transfer(tokens: List[Token]):
    str_index = 0
    transfers = []
    for i, token in enumerate(tokens):
        transfers.append((
            Sequence(i, i+1),
            Sequence(str_index, str_index + len(token))
        ))
        str_index += len(token)
        if i != len(tokens)-1:
            str_index += 1

    return SequenceTransfer(
        Sequence(0, len(tokens)),
        Sequence(0, str_index),
        transfers
    )

