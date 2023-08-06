from sequence_transfer.sequence import Sequence
from pprint import pprint
from sequence_transfer.sequence_transfer import SequenceTransfer


def lcs_transfer(x: str, y: str) -> SequenceTransfer:
    m = len(x)
    n = len(y)

    L = [[None] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif x[i - 1] == y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    transfers = []
    maybe_errors = []
    error_section = False
    equivalent_section = False
    start_src_section = fin_src_section = -1
    start_tgt_section = fin_tgt_section = -1
    last_value = L[m][n]

    while m > 0 and n > 0:
        max_neighbor = max(L[m - 1][n - 1], L[m][n - 1], L[m - 1][n])
        equivalent = last_value > max_neighbor
        if L[m - 1][n - 1] == max_neighbor:
            if not equivalent:
                if equivalent_section:
                    match = (
                        Sequence(start_src_section, fin_src_section),
                        Sequence(start_tgt_section, fin_tgt_section)
                    )
                    transfers.append(match)
                    equivalent_section = False
                if error_section:
                    start_src_section = m - 1
                    start_tgt_section = n - 1
                else:
                    start_src_section = m - 1
                    fin_src_section = m
                    start_tgt_section = n - 1
                    fin_tgt_section = n
                    error_section = True
            else:
                if error_section:
                    match = (
                        Sequence(start_src_section, fin_src_section),
                        Sequence(start_tgt_section, fin_tgt_section)
                    )
                    transfers.append(match)
                    maybe_errors.append(
                        (
                            (start_src_section, fin_src_section),
                            (start_tgt_section, fin_tgt_section)
                        )
                    )
                    error_section = False
                if equivalent_section:
                    start_src_section = m - 1
                    start_tgt_section = n - 1
                else:
                    start_src_section = m - 1
                    fin_src_section = m
                    start_tgt_section = n - 1
                    fin_tgt_section = n
                    equivalent_section = True
            m = m - 1
            n = n - 1
        elif L[m][n - 1] == max_neighbor:
            # match = (Sequence(m, m), Sequence(n - 1, n))
            if equivalent_section:
                match = (
                    Sequence(start_src_section, fin_src_section),
                    Sequence(start_tgt_section, fin_tgt_section)
                )
                transfers.append(match)
                equivalent_section = False
            if error_section:
                start_tgt_section = n - 1
            # else:
            #     start_src_section = m
            #     fin_src_section = m
            #     start_tgt_section = n - 1
            #     fin_tgt_section = n
            #     error_section = True
            n = n - 1
        elif L[m - 1][n] == max_neighbor:
            if equivalent_section:
                match = (
                    Sequence(start_src_section, fin_src_section),
                    Sequence(start_tgt_section, fin_tgt_section)
                )
                transfers.append(match)
                equivalent_section = False
            if error_section:
                start_src_section = m - 1
            else:
                start_src_section = m - 1
                fin_src_section = m
                start_tgt_section = n
                fin_tgt_section = n
                error_section = True
            m = m - 1
        last_value = max_neighbor

    if equivalent_section:
        match = (
            Sequence(start_src_section, fin_src_section),
            Sequence(start_tgt_section, fin_tgt_section)
        )
        transfers.append(match)
        equivalent_section = False
    elif error_section:
        match = (
            Sequence(start_src_section, fin_src_section),
            Sequence(start_tgt_section, fin_tgt_section)
        )
        transfers.append(match)
        maybe_errors.append(
            (
                (start_src_section, fin_src_section),
                (start_tgt_section, fin_tgt_section)
            )
        )
        error_section = False

    if m > 0:
        match = (Sequence(0, m), Sequence(0, 0))
        transfers.append(match)

    # while n > 0:
    #     match = (Sequence(m, m), Sequence(n - 1, n))
    #     transfers.append(match)
    #     n -= 1

    transfers.reverse()
    maybe_errors.reverse()

    return (
        SequenceTransfer(
            Sequence(0, len(x)),
            Sequence(0, len(y)),
            transfers
        ),
        tuple(maybe_errors)
    )
