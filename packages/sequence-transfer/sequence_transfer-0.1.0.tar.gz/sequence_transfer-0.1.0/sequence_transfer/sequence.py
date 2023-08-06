from typing import List, Tuple, Optional, Union, Any
from colorama import Fore, Style


#  Exceptions


class InvalidSequenceException(Exception):
    def __init__(self, start, stop):
        super().__init__(f"Invalid sequence_transfer Stop < start: [{start} {stop}[")


class SequenceNotInException(Exception):
    def __init__(self, sequence1: "Sequence", sequence2: "Sequence"):
        super().__init__(f"Sequence {sequence1} not in {sequence2}")


class EmptySequenceException(Exception):
    def __init__(self, sequence: "Sequence"):
        super().__init__(f"Sequence {sequence} is empty")


class NotContextualizedSequenceException(Exception):
    def __init__(self, sequence: "Sequence"):
        super().__init__(f"Sequence {sequence} has no context")


# Sequence. The queen...


class Sequence:
    def __init__(self, start: int, stop: int, context: "SequenceContext" = None):
        """
        A sequence is a pair of number (n,p) with n<=p. The equal sign has his importance.
        Formally, the set of all sequences is defined as: S = {(n,p) ∈  ℤ², n<=p}

        A sequence [n,p[ is intrinsically as we said it before: 2 numbers, but it 's equivalent to
        a sequence of numbers from n to p (with p excluded). For example [2 8[ is equivalent to the sequence
        2 3 4 5 6 7. But this equivalence is broken when n=p.

        :param start: Where the sequence start
        :param stop: Where the sequence stop (not included)
        :param context: The materialization of the sequence: A sequence of concrete things like chars, tokens
                Important: A subsequence of a sequence share his context
        """
        if stop < start:
            raise InvalidSequenceException(start, stop)
        self._start = start
        self._stop = stop
        self._size = stop - start
        self._context = context

    def get_start(self):
        return self._start
    start = property(get_start)

    def get_stop(self):
        return self._stop
    stop = property(get_stop)

    def get_size(self):
        return self._size
    size = property(get_size)

    def is_subsequence(self, sequence):
        return sequence.start <= self._start and self._stop <= sequence.stop

    def raise_if_not_in(self, sequence):
        if not self.is_subsequence(sequence):
            raise SequenceNotInException(self, sequence)

    def is_empty(self):
        return self._size == 0

    def raise_if_empty(self):
        if self.is_empty():
            raise EmptySequenceException(self)

    def raise_if_not_contextualized(self):
        if self._context is None:
            raise NotContextualizedSequenceException(self)

    def split(self, n: Optional[int] = None) -> List["Sequence"]:
        """
        split the sequence in n sequences of "similar" size. If n == None -> n = self.size
        :param n:
        :return:
        """
        if n is None:
            n = self._size

        sizes = [self._size // n]*n
        for i in range(self._size % n):
            sizes[i] += 1

        sequences = []
        for i, size in enumerate(sizes):
            if i == 0:
                start = self._start
            else:
                start = sequences[-1].stop
            stop = start + size
            sequences.append(Sequence(start, stop))
        return sequences

    @staticmethod
    def expand(sequence1: "Sequence", sequence2: "Sequence") -> "Sequence":
        """
        [2 5[ 5 6 [7 9[  ->  0 1 [2 9[ 9
        :param sequence1:
        :param sequence2:
        :return:
        """
        if sequence1.start <= sequence2.stop:
            return Sequence(sequence1.start, sequence2.stop)
        else:
            return Sequence(sequence2.stop, sequence1.start)

    @staticmethod
    def between(sequence1: "Sequence", sequence2: "Sequence") -> "Sequence":
        return Sequence(sequence1.stop, sequence2.start)

    def iter_index(self):
        return iter(range(self.start, self.stop))

    def __iter__(self):
        sequence_type = type(self)
        return iter([sequence_type(i, i+1, context=self._context) for i in self.iter_index()])

    def __len__(self):
        return self._size

    def __getitem__(self, key):
        sequence_type = type(self)
        if type(key) is int:
            new_start = self._start + key
            sequence = sequence_type(new_start, new_start + 1, context=self._context)
            if not sequence.is_subsequence(self):
                raise KeyError()
            return sequence

        elif type(key) is tuple:
            return self._get_item(key[0], key[1])
        elif type(key) is slice:
            return self._get_item(key.start, key.stop)

    def _get_item(self, start, stop):
        if start is None:
            start = self._start
        elif start < 0:
            start = self._stop + start
        else:
            start = self._start + start

        if stop is None:
            stop = self._stop
        elif stop < 0:
            stop = self._stop + stop
        else:
            stop = self._start + stop

        sequence_type = type(self)
        sequence = sequence_type(start, stop, context=self._context)
        if not sequence.is_subsequence(self):
            raise KeyError()
        return sequence

    def __setitem__(self, key, value):
        raise ValueError("sequence item changes are not allowed")

    def __eq__(self, other):
        if self._start != other.start or self._stop != other.stop:
            return False
        return True

    def __repr__(self):
        return self.slice_representation()

    def slice_representation(self):
        return f"[{self.start}:{self.stop}]"

    def get_context(self):
        return self._context

    def set_context(self, context: Union[str, List["Token"]]):
        self._context = context

    context = property(get_context, set_context)


#  Sequence Element


class Token:
    def __init__(self, text: str):
        self._text = text
        if " " in text:
            raise ValueError(f"token with whitespace `{text}`")

    def get_text(self) -> str:
        return self._text
    text = property(get_text)

    def __len__(self) -> int:
        return len(self._text)


class Char:
    def __init__(self, text: str):
        self._text = text

    def get_text(self) -> str:
        return self._text
    text = property(get_text)

    def __len__(self) -> int:
        return len(self._text)


#  Contexts


class SequenceContext:
    def __init__(self, content: List[Any]):
        self._content = content

    def get_content(self):
        return self._content
    content = property(get_content)

    def materialize_sequence(self, sequence: Sequence) -> List:
        return self._content[sequence.start:sequence.stop]


class TextualSequenceContext(SequenceContext):
    def get_sequence_text(self, sequence) -> str:
        return ''


class CharSequenceContext(TextualSequenceContext):
    def __init__(self, content: List[Char]):
        super().__init__(content)

    def get_sequence_text(self, sequence: Sequence):
        elements_as_text = map(lambda x: x.text, self._content[sequence.start: sequence.stop])
        return "".join(elements_as_text)

    def represent_sequence(self, sequence: Sequence) -> str:
        return self.get_sequence_text(sequence)

    def represent_sequence_in_context(self, sequence: Sequence) -> str:
        print(f"representing {sequence} in {self}")
        return "".join([
                self.represent_sequence(Sequence(0, sequence.start)),
                Fore.CYAN + self.represent_sequence(sequence) + Style.RESET_ALL,
                self.represent_sequence(Sequence(sequence.stop, len(self._content))),
            ])


class TokenSequenceContext(TextualSequenceContext):
    def __init__(self, content: List[Token]):
        super().__init__(content)

    def get_sequence_text(self, sequence):
        elements_as_text = map(lambda x: x.text, self._content[sequence.start: sequence.stop])
        return " ".join(elements_as_text)

    def represent_sequence(self, sequence: Sequence) -> str:
        return self.get_sequence_text(sequence)

    def represent_sequence_in_context(self, sequence: Sequence) -> str:
        return " ".join([
                self.represent_sequence(Sequence(0, sequence.start)),
                Fore.CYAN + self.represent_sequence(sequence) + Style.RESET_ALL,
                self.represent_sequence(Sequence(sequence.stop, len(self._content))),
            ])


# Special Sequences


class ContextualizedSequence(Sequence):
    def materialize(self, sequence: Optional[Sequence] = None):
        if sequence is None:
            sequence = self
        return self._context.content[sequence.start: sequence.stop]


class TextualSequence(ContextualizedSequence):
    def in_context(self) -> str:
        return self._context.represent_sequence_in_context(self)  # TODO Check

    def get_text(self, sequence: Optional[Sequence] = None) -> str:
        if sequence is None:
            sequence = self
        return self._context.get_sequence_text(sequence)
    text = property(get_text)


class TokenSequence(TextualSequence):
    @staticmethod
    def new(tokens: List[str]) -> "TokenSequence":
        if type(tokens) is not list:
            raise ValueError(f"TokenSequence expect a list of string")
        return TokenSequence(0, len(tokens), TokenSequenceContext(list(map(lambda token: Token(token), tokens))))

    def __init__(self, start: int, stop: int, context: TokenSequenceContext):
        super().__init__(start, stop, context)


class CharSequence(TextualSequence):
    @staticmethod
    def new(text: str) -> "CharSequence":
        if type(text) is not str:
            raise ValueError(f"CharSequence expect a string")
        return CharSequence(0, len(text), CharSequenceContext(list(map(lambda char: Char(char), text))))

    def __init__(self, start: int, stop: int, context: CharSequenceContext):
        super().__init__(start, stop, context)




