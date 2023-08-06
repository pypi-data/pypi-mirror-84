import re
from io import StringIO
from typing import Sequence

_OPTION = (("?", False), {})
_OPEN_PARENTHESIS = (("(?:", False), {})
_CLOSE_PARENTHESIS = ((")", False), {})
_OPEN_BRACKETS = (("[", False), {})
_CLOSE_BRACKETS = (("]", False), {})
_ALTERNATION = (("|", False), {})


class _Trie:
    def __init__(self, words, left=r"\b", right=r"\b"):

        data = {}
        self.left = left
        self.right = right
        self.root = {(left, False): data}
        for word in set(words):
            ref = data
            for char in word[:-1]:
                fk, tk = (char, False), (char, True)
                key = tk if tk in ref else fk
                ref[key] = key in ref and ref[key] or {}
                ref = ref[key]
            if word:
                char = word[-1]
                ref[(char, True)] = ref.pop((char, False), {})  # mark as end

    def _to_regex(self):

        stack = [*self.root.items()]
        cumulative = StringIO()

        while stack:

            (char, end), children = stack.pop()
            cumulative.write(char)

            if not children:
                continue  # skip

            if end:
                stack.append(_OPTION)

            single, multiple = [], []
            for key, values in children.items():
                if values:
                    multiple.append((key, values))
                else:
                    single.append((key, values))

            requires_character_set = len(single) > 1
            requires_alternation = (multiple and single) or len(multiple) > 1
            requires_group = requires_alternation or (end and multiple)

            if requires_group:
                stack.append(_CLOSE_PARENTHESIS)

            if requires_character_set:
                stack.append(_CLOSE_BRACKETS)

            for child in single:
                stack.append(child)

            if requires_character_set:
                stack.append(_OPEN_BRACKETS)

            if requires_alternation and single:
                stack.append(_ALTERNATION)

            if multiple:
                head, *tail = multiple
                stack.append(head)

                for child in tail:
                    stack.append(_ALTERNATION)
                    stack.append(child)

            if requires_group:
                stack.append(_OPEN_PARENTHESIS)

        return cumulative.getvalue()

    def compile(self, flags=0):
        return re.compile(self.make(), flags=flags)

    def make(self):
        return rf"{self._to_regex()}{self.right}"


def compile(
    words: Sequence[str], left: str = r"\b", right: str = r"\b", flags: int = 0
):
    """
    Create a regular expression object from a set of strings

    Parameters
    ----------
    words : Sequence[str]
            Sequence or set of strings to be compiled

    left : str, optional
           Left delimiter for pattern

    right : str, optional
            Right delimiter for pattern

    flags : int, optional
            This value can be used to modify the expression can be any of the flags in re

    Returns
    -------
    Pattern
            A regular expression object which can be used for matching using its match(), search() and other methods

    Examples
    --------
    >>> import trrex as tx
    >>> pattern = tx.compile(['baby', 'bat', 'bad'])
    >>> pattern.findall('The baby was scared by the bad bat.')
    ['baby', 'bad', 'bat']
    """

    return _Trie(words, left=left, right=right).compile(flags)


def make(words: Sequence[str], left: str = r"\b", right: str = r"\b"):
    """
    Create a string that represents a regular expression object from a set of strings

    Parameters
    ----------
    words : Sequence[str]
        Sequence or set of strings to be made into a regex

    left : str, optional
           Left delimiter for pattern

    right : str, optional
            Right delimiter for pattern

    Returns
    -------
    String
            A string representing a regular expression pattern

    Examples
    --------
    >>> import re
    >>> import trrex as tx
    >>> pattern = tx.make(['baby', 'bat', 'bad'], left=" ", right=" ")
    >>> re.match(pattern, " baby ").group()
    ' baby '
    """

    return _Trie(words, left=left, right=right).make()
