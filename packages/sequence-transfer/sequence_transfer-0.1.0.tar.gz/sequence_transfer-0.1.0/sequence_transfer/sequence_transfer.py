from typing import List, Tuple, TypeVar
from sequence_transfer.sequence import Sequence
from prettytable import PrettyTable


class SequenceTransferException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class SequenceTransferPlugin:
    def apply(self, transfer: "Transfer", sequence: Sequence) -> Sequence:
        """
        :param transfer:
        :param sequence:
        :return:
        """
        pass


class SequenceTransfer:
    def __init__(self,
                 source: Sequence,
                 target: Sequence,
                 matches: List[Tuple[Sequence, Sequence]]):
        """
        :param source: for examples Sequence(0,6) = 0 1 2 3 4 5  = [0 6[  - Imagine string keys.
        :param target: for examples Sequence(0,10) = 0 1 2 3 4 5 6 7 8 9 = [0 10[
        :param matches: A list of pair of sub-sequences transfer that represents matches between source and target.
        - not true now. [Any sub-sequence in the source should have a size of 1 >]
        - The sequences in source have to be ordered, adjacent and "cover" the entire source sequence.
        - the sequences in target have only to be ordered. Holes are possible...
        Now you can use the 'apply' function and "invert" the transfer

        """
        # Source
        source.raise_if_empty()
        self._source = source

        # target
        target.raise_if_empty()
        self._target = target

        # Matches
        if not matches:
            raise SequenceTransferException(f"matches '{matches}' is empty")

        self._matches = []
        self._index = {}
        for i, (source_sequence, target_sequence) in enumerate(matches):
            # Some checks
            source_sequence.raise_if_empty()
            source_sequence.raise_if_not_in(source)
            target_sequence.raise_if_not_in(target)

            if i == 0:
                if source_sequence.start != source.start:
                    raise SequenceTransferException(
                        f"the source sequence_transfer of the first match {source_sequence} "
                        f"should be at the beginning of the source")
            if i > 1:
                previous_source_sequence = matches[i-1][0]
                if previous_source_sequence.stop != source_sequence.start:
                    raise SequenceTransferException(
                        f"adjacency error in the source match list between index {i-1} and {i}:"
                        f" {previous_source_sequence}  {source_sequence}")

                previous_target_sequence = matches[i-1][1]
                if previous_target_sequence.stop > target_sequence.start:
                    raise SequenceTransferException(
                        f"order error in the target match list between index {i-1} and {i}:"
                        f" {previous_target_sequence}  {target_sequence}")

            if i == len(matches)-1:
                if source_sequence.stop != source.stop:
                    raise SequenceTransferException(
                        f"the source sequence_transfer of the last match {source_sequence}  should stop at the end of "
                        f"the source")

            self._matches.append((source_sequence, target_sequence))
            if target_sequence.size:
                min_size = min(source_sequence.size, target_sequence.size)
                for sub_source_sequence, sub_target_sequence in zip(
                        source_sequence.split(min_size),
                        target_sequence.split(min_size)):
                    for j in sub_source_sequence.iter_index():
                        self._index[j] = sub_target_sequence
            else:
                for j in source_sequence.iter_index():
                    self._index[j] = target_sequence

    def apply(self, source_sequence: Sequence, plugin: SequenceTransferPlugin = None) -> Sequence:
        """
        :param source_sequence: any sub-sequence of the source
        :param plugin: SequenceTransferPlugin instance
        :return: transferred sub-sequence in the target
        """

        if plugin is not None:
            return plugin.apply(self, source_sequence)

        source_sequence.raise_if_not_in(self._source)

        if source_sequence.size == 0 and source_sequence.start == self._source.start:
            return Sequence(
                self._index[0].start,
                self._index[0].start,
            )
        elif source_sequence.size == 0 and source_sequence.stop == self._source.stop:
            return Sequence(
                self._index[self._source.size-1].stop,
                self._index[self._source.size-1].stop,
            )
        else:
            return Sequence.expand(
                self._index[source_sequence.start],
                self._index[source_sequence.stop-1]
            )

    def invert(self):
        return SequenceTransfer(
            self._target,
            self._source,
            self.get_inverted_matches()
        )

    def get_inverted_matches(self):
        return list(map(
            lambda match: (match[1], match[0]),
            filter(lambda match: match[1].size > 0, self._parallelize())
        ))

    def debug_in_text(self, source_text: str, target_text: str):
        table = PrettyTable(["SRC SLICE", "INDEX SRC", "TEXT SRC", "", "TEXT TGT", "INDEX TGT", "TGT SLICE"])
        parallel_matches = self._parallelize()

        for source_sequence, target_sequence in parallel_matches:
            col1 = source_sequence.slice_representation()
            col2 = "\n".join([str(i) for i in source_sequence.iter_index()])
            col3 = "\n".join([str([source_text[i]]) for i in source_sequence.iter_index()])
            col4 = '--->'
            col5 = "\n".join([str([target_text[i]]) for i in target_sequence.iter_index()])
            col6 = "\n".join([str(i) for i in target_sequence.iter_index()])
            col7 = target_sequence.slice_representation()
            table.add_row([
                col1, col2, col3, col4, col5, col6, col7
            ])

        print(table)

    def _parallelize(self):
        """
        create an empty sequence on the source foreach hole in the target and add them to the list of matches
        :return:
        """
        parallel_matches = []
        for i, (source_sequence, target_sequence) in enumerate(self._matches):
            if i == 0:
                last_target_sequence = Sequence(self._target.start, self._target.start)
            else:
                last_target_sequence = self._matches[i-1][1]

            # Resolving potential holes before the target
            between_target = Sequence.between(last_target_sequence, target_sequence)
            if between_target.size != 0:
                parallel_matches.append((
                    Sequence(source_sequence.start, source_sequence.start),
                    between_target
                ))

            # Already ok
            parallel_matches.append((
                source_sequence, target_sequence
            ))

            # Holes at the end
            if i == len(self._matches) - 1 and target_sequence.stop != self._target.stop:
                parallel_matches.append((
                    Sequence(self._source.stop, self._source.stop),
                    Sequence(target_sequence.stop, self._target.stop)
                ))

        return parallel_matches

    @staticmethod
    def compose(*args: "SequenceTransfer"):
        transfers = list(args)
        if len(transfers) < 1:
            raise SequenceTransferException('compose require at least two transfers')

        first_transfer = transfers[0]
        last_transfer = transfers[-1]

        matches = []

        for i, (sequence, _) in enumerate(first_transfer.matches):
            tmp = sequence
            for f in transfers:
                tmp = f.apply(tmp)

            if i > 0 and matches[-1][1] == tmp:
                match = (Sequence.expand(matches[-1][0], sequence), tmp)
                matches.pop()
                matches.append(match)
            else:
                matches.append((
                    sequence,
                    tmp
                ))

        return SequenceTransfer(
            first_transfer.source,
            last_transfer.target,
            matches
        )

    def get_source(self):
        return self._source
    source = property(get_source)

    def get_target(self):
        return self._target
    target = property(get_target)

    def get_matches(self):
        return self._matches
    matches = property(get_matches)

    def debug(self):
        for match in self._matches:
            print(match)
