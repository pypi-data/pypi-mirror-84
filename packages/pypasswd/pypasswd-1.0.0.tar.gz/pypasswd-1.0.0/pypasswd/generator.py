"""generator.py:

This module implements the ``PasswdGenerator`` class which does the actual
password generation and a ``main`` function which is the entrypoint to a
simple program to generate a password.
"""

import argparse
import functools
import operator
import secrets
import string

from typing import List, FrozenSet


class PasswdGenerator:
    """Secure password generator.

    Attributes:
        __character_sets: List[FrozenSet[str]]   a list of set of characters
                                                 to choose from for password
                                                 generation.
    """

    def __init__(self, character_strings: List[str] = None) -> None:
        """Create a new PasswdGenerator object.

        This function raises a ``TypeError`` if ``character_strings`` is not a
        list of strings and a ``ValueError`` if ``character_strings`` is an
        empty list.

        :param character_strings: list of strings which will be used as character sets
        :type character_strings: List[str]
        """

        if character_strings is None:
            character_strings = [
                string.ascii_lowercase,
                string.ascii_uppercase,
                string.digits,
                string.punctuation,
            ]
        elif not isinstance(character_strings, list) or not all(
            isinstance(s, str) for s in character_strings
        ):
            raise TypeError(
                "parameter 'character_strings' must be a list of strings"
            )
        elif not character_strings:
            raise ValueError("parameter 'character_strings' cannot be empty")

        self.__character_sets: List[FrozenSet[str]] = list(
            frozenset(character_string)
            for character_string in character_strings
        )

    def __call__(self, length: int = 64, no_strict: bool = False) -> str:
        """Actually generate a password. It is important to check at least one
        character from every character set was included in the password.

        This function raises a ``TypeError`` if ``length`` is not an integer
        of ``strict`` is not a boolean.

        A ``ValueError`` is raised if the asked length is smaller of equal to
        ``0`` or if ``strict`` is ``True`` and the wanted length is smaller
        than the length of the character set list.

        :param length: length of the password to generate
        :type length: int
        :param no_strict: do not enforce strict generation
        :type no_strict: bool
        :return: generated password
        :rtype: str
        """
        if not isinstance(length, int):
            raise TypeError("parameter 'length' must be a positive integer")
        elif not isinstance(no_strict, bool):
            raise TypeError("parameter 'strict' must be a boolean")
        elif length <= 0:
            raise ValueError("parameter 'length' must be a positive integer")
        elif not no_strict and length < len(self.__character_sets):
            raise ValueError(
                "when using strict generation, 'length' must be bigger than character set count"
            )

        character_list: List[str] = list(
            functools.reduce(operator.or_, self.__character_sets)
        )
        passwd: str = "".join(
            secrets.choice(character_list) for _ in range(length)
        )

        if no_strict:
            return passwd

        while not all(
            any(c in charset for c in passwd)
            for charset in self.__character_sets
        ):
            passwd = "".join(
                secrets.choice(character_list) for _ in range(length)
            )
        return passwd


def main() -> None:
    """This function is to be called as a script using the ``pypasswd``
    command.

    ``main`` will parse arguments, create a ``PasswdGenerator`` object then
    call it as many times as required to get passwords.

    """
    argument_parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Securely generate a random password."
    )
    argument_parser.add_argument(
        "-n",
        "--number",
        type=int,
        default=1,
        help="number of passwords to generate (default: 1)",
        metavar="N",
    )
    argument_parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=64,
        help="size of each password (default: 64)",
        metavar="L",
    )
    argument_parser.add_argument(
        "-c",
        "--charsets",
        nargs="+",
        default=None,
        help="strings of characters to choose from (default: lowercase, uppercase, digits and punctuation)",
        metavar="str",
    )
    argument_parser.add_argument(
        "-S",
        "--no-strict",
        action="store_true",
        default=False,
        help="do not force having at least one character from each character set (default: False)",
    )
    parsed_args: argparse.Namespace = argument_parser.parse_args()
    passwd_generator: PasswdGenerator = PasswdGenerator(parsed_args.charsets)
    for _ in range(parsed_args.number):
        print(passwd_generator(parsed_args.length, parsed_args.no_strict))


if __name__ == "__main__":
    main()
