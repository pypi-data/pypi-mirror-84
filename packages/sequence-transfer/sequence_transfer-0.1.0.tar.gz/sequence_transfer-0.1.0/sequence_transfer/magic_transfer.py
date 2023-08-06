from typing import Union, Tuple
from prettytable import PrettyTable
from sequence_transfer.sequence_transfer import SequenceTransfer
from sequence_transfer.normalizer.remove_whitespace import remove_whitespace
from sequence_transfer.normalizer.remove_html_entities import remove_html_entities
from sequence_transfer.normalizer.remove_bert_separator import remove_bert_separator
from sequence_transfer.normalizer.to_lower import to_lower
from sequence_transfer.normalizer.remove_accents import remove_accents
from sequence_transfer.lcs_transfer import lcs_transfer
from sequence_transfer.token_to_text_transfer import token_to_text_transfer
from sequence_transfer.sequence import CharSequence, TokenSequence, TokenSequenceContext
from sequence_transfer.contextualized_sequence_transfer import ContextualizedTransfer


class MagicTransfer(ContextualizedTransfer):
    def __init__(self,
                 source: Union[CharSequence, TokenSequence],
                 target: Union[CharSequence, TokenSequence]):

        normalized_source, t1 = _normalize(source)
        normalized_target, t2 = _normalize(target)
        t2_inv = t2.invert()

        t3, error = lcs_transfer(normalized_source, normalized_target)
        self._error = TransferError(
            normalized_source, normalized_target, error
        )
        t4 = SequenceTransfer.compose(t1, t3, t2_inv)

        if isinstance(source.context, TokenSequenceContext) or \
                isinstance(target.context, TokenSequenceContext):
            compose = []
            if isinstance(source.context, TokenSequenceContext):
                compose.append(
                    token_to_text_transfer(source.context.content)
                )
            compose.append(t4)
            if isinstance(target.context, TokenSequenceContext):
                compose.append(
                    token_to_text_transfer(target.context.content).invert()
                )
            t4 = SequenceTransfer.compose(*compose)

        super().__init__(source, target, t4.matches)

    def get_error(self):
        return self._error
    error = property(get_error)


def _normalize(sequence:  Union[CharSequence, TokenSequence]):
    text1 = sequence.text
    text2, t1 = remove_whitespace(text1)
    text3, t2 = remove_bert_separator(text2)
    text4, t3 = remove_html_entities(text3)
    text5, t4 = to_lower(text4)
    text6, t5 = remove_accents(text5)
    t = SequenceTransfer.compose(t1, t2, t3, t4, t5)
    return text6, t


class TransferError:
    def __init__(self, src: str, tgt: str, errors: Tuple) -> None:
        table = PrettyTable(
            ["SRC UNICODE", "SRC CHAR", "", "TGT CHAR", "TGT UNICODE"]
        )
        num_errors = 0
        for error in errors:
            src_slice, tgt_slice = error
            src_pointer = src_slice[0]
            tgt_pointer = tgt_slice[0]
            col3 = '--->'
            while src_pointer < src_slice[1] or tgt_pointer < tgt_slice[1]:

                if src_pointer < src_slice[1]:
                    col1 = hex(ord(src[src_pointer]))
                    col2 = f"['{src[src_pointer]}']"
                    src_pointer += 1
                    num_errors += 1
                else:
                    col1 = ""
                    col2 = ""

                if tgt_pointer < tgt_slice[1]:
                    col5 = hex(ord(tgt[tgt_pointer]))
                    col4 = f"['{tgt[tgt_pointer]}']"
                    tgt_pointer += 1
                    num_errors += 1
                else:
                    col5 = ""
                    col4 = ""

                table.add_row([col1, col2, col3, col4, col5])
                col3 = ""

            table.add_row(["", "", "", "", ""])

        error_rate = "%.2f" % (num_errors * 100 / (len(src) + len(tgt)))

        self._table = table
        self._error = float(error_rate)

    def get_table(self):
        print(self._table)
    debug = property(get_table)

    def get_error(self):
        return self._error
    rate = property(get_error)
