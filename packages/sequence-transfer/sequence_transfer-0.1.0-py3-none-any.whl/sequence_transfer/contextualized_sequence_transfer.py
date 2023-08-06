from typing import Union, List, Tuple, Optional
from sequence_transfer.sequence_transfer import SequenceTransfer, SequenceTransferPlugin
from sequence_transfer.sequence import ContextualizedSequence
from pytablewriter import MarkdownTableWriter
from pytablewriter.style import Style
from itertools import zip_longest
from typing import Any


class ContextualizedTransfer(SequenceTransfer):
    def __init__(self,
                 source: ContextualizedSequence,
                 target: ContextualizedSequence,
                 matches: List[Tuple[ContextualizedSequence, ContextualizedSequence]]):
        super().__init__(source, target, matches)

    def apply(self, sequence: Any, plugin: Optional[SequenceTransferPlugin] = None) -> \
            Any:
        if plugin is not None:
            return plugin.apply(self, sequence)

        sequence_type = type(sequence)
        transferred = super().apply(sequence, plugin)
        return sequence_type(transferred.start, transferred.stop, self._target.context)

    def invert(self):
        matches = self.get_inverted_matches()
        return ContextualizedTransfer(self._target, self._source, matches)

    def debug(self):
        parallel_matches = self._parallelize()
        writer = MarkdownTableWriter()
        writer.table_name = "debug"
        writer.headers = ["Src slice", "Index src", "Text src", "", "Text tgt", "Index tgt", "Tgt slice"]
        writer.column_styles = [Style(align='center')]*7

        rows = []
        for source_sequence, target_sequence in parallel_matches:
            source_sequence.context = self._source.context
            target_sequence.context = self._target.context
            col1 = source_sequence.slice_representation()
            col2 = "\n".join([str(i) for i in source_sequence.iter_index()])
            col3 = "\n".join([s.context.get_sequence_text(s) for s in source_sequence])
            col4 = '--->'
            col5 = "\n".join([s.context.get_sequence_text(s) for s in target_sequence])
            col6 = "\n".join([str(i) for i in target_sequence.iter_index()])
            col7 = target_sequence.slice_representation()
            for a, b, c, d, e, f, g in zip_longest(
                    [col1],
                    col2.split('\n'),
                    col3.split('\n'),
                    [col4],
                    col5.split('\n'),
                    col6.split('\n'),
                    [col7]):
                rows.append([
                    a, b, c, d, e, f, g
                ])
            rows.append([""]*7)
        rows.pop()
        writer.value_matrix = rows
        writer.write_table()




