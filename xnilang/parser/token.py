#!/usr/bin/env python
#
#  Copyright 2015 XiaoJSoft Studio.
#
#  Use of this source code is governed by a proprietary license. You can not read, change or
#  redistribute this source code unless you have a written authorization from the copyright
#  holder listed above.
#

#  Import other modules.
import xnilang.parser.error as _error

#  Token types.
TOKEN_TYPE_OPERAND = "operand"
TOKEN_TYPE_PARENTHESIS = "parenthesis"
TOKEN_TYPE_SYMBOL = "symbol"

#  Token sub-types.
TOKEN_SUBTYPE_OPERAND_FLOAT = "float"
TOKEN_SUBTYPE_OPERAND_INTEGER = "integer"
TOKEN_SUBTYPE_PARENTHESIS_LEFT = "left"
TOKEN_SUBTYPE_PARENTHESIS_RIGHT = "right"


class Token:
    """Token class."""

    def __init__(self, symbol, token_type, token_subtype, position):
        """Initialize the token.

        :type symbol: str
        :type token_type: str
        :type token_subtype: str
        :type position: int
        :param symbol: The token symbol.
        :param token_type: The type of the token.
        :param token_subtype: The sub-type of the token.
        :param position: The token position.
        """

        self._symbol = symbol
        self._type = token_type
        self._subtype = token_subtype
        self._position = position

    def get_symbol(self):
        """Get the token symbol.

        :rtype : str
        :return: The symbol.
        """

        return self._symbol

    def get_type(self):
        """Get the type of the token.

        :rtype : str
        :return: The type.
        """

        return self._type

    def get_subtype(self):
        """Get the sub-type of the token.

        :rtype : str
        :return: The sub-type.
        """

        return self._subtype

    def get_position(self):
        """Get the token position.

        :rtype : int
        :return: The position.
        """

        return self._position

    def is_operand(self):
        """Get whether the token is an operand (float or integer).

        :rtype : bool
        :return: True if so.
        """

        return self.get_type() == TOKEN_TYPE_OPERAND

    def is_float_operand(self):
        """Get whether the token is a float.

        :rtype : bool
        :return: True if so.
        """

        return self.is_operand() and self.get_subtype() == TOKEN_SUBTYPE_OPERAND_FLOAT

    def is_integer_operand(self):
        """Get whether the token is an integer.

        :rtype : bool
        :return: True if so.
        """

        return self.is_operand() and self.get_subtype() == TOKEN_SUBTYPE_OPERAND_INTEGER

    def is_parenthesis(self):
        """Get whether the token is a parenthesis.

        :rtype : bool
        :return: True if so.
        """

        return self.get_type() == TOKEN_TYPE_PARENTHESIS

    def is_left_parenthesis(self):
        """Get whether the token is a left parenthesis.

        :rtype : bool
        :return: True if so.
        """

        return self.is_parenthesis() and self.get_subtype() == TOKEN_SUBTYPE_PARENTHESIS_LEFT

    def is_right_parenthesis(self):
        """Get whether the token is a right parenthesis.

        :rtype : bool
        :return: True if so.
        """

        return self.is_parenthesis() and self.get_subtype() == TOKEN_SUBTYPE_PARENTHESIS_RIGHT

    def is_symbol(self):
        """Get whether the token is a symbol.

        :rtype : bool
        :return: True if so.
        """

        return self.get_type() == TOKEN_TYPE_SYMBOL

    @staticmethod
    def create_float_operand(symbol, position):
        """Create a float operand token.

        :type symbol: str
        :type position: int
        :param symbol: The token symbol.
        :param position: The token position.
        :rtype : Token
        :return: The token.
        """

        return Token(symbol, TOKEN_TYPE_OPERAND, TOKEN_SUBTYPE_OPERAND_FLOAT, position)

    @staticmethod
    def create_integer_operand(symbol, position):
        """Create an integer operand token.

        :type symbol: str
        :type position: int
        :param symbol: The token symbol.
        :param position: The token position.
        :rtype : Token
        :return: The token.
        """

        return Token(symbol, TOKEN_TYPE_OPERAND, TOKEN_SUBTYPE_OPERAND_INTEGER, position)

    @staticmethod
    def create_left_parenthesis(position):
        """Create a left parenthesis token.

        :type position: int
        :param position: The token position.
        :rtype : Token
        :return: The token.
        """

        return Token("(", TOKEN_TYPE_PARENTHESIS, TOKEN_SUBTYPE_PARENTHESIS_LEFT, position)

    @staticmethod
    def create_right_parenthesis(position):
        """Create a right parenthesis token.

        :type position: int
        :param position: The token position.
        :rtype : Token
        :return: The token.
        """

        return Token(")", TOKEN_TYPE_PARENTHESIS, TOKEN_SUBTYPE_PARENTHESIS_RIGHT, position)

    @staticmethod
    def create_symbol(symbol, position):
        """Create a symbol token.

        :type symbol: str
        :type position: int
        :param symbol: The token symbol.
        :param position: The token position.
        :rtype : Token
        :return: The token.
        """

        return Token(symbol, TOKEN_TYPE_SYMBOL, "", position)


def _is_separator(ch):
    """Get whether a character is a separator.

    :type ch: str
    :param ch: The character.
    :rtype : bool
    :return: True if so.
    """

    return ch in ["\n", "\r", "\t", chr(32), chr(160)]


class Tokenizer:
    """Script tokenizer."""

    def __init__(self, script):
        """Initialize the tokenizer.

        :type script: str
        :param script: The source script.
        """

        self._script = script
        self._cursor = 0

    def get_cursor(self):
        """Get current cursor.

        :rtype : int
        :return: The cursor.
        """

        return self._cursor

    def get_script(self):
        """Get the script.

        :rtype : str
        :return: The script.
        """

        return self._script

    def move_cursor(self, destination):
        """Move cursor to specified destination.

        :type destination: int
        :param destination: The destination.
        :raise IndexError: Raise this exception if the destination is out of range.
        """

        #  Safe check.
        if destination < 0 or destination > len(self.get_script()):
            raise IndexError("Destination unreachable.")

        #  Set the cursor.
        self._cursor = destination

    def move_cursor_by_offset(self, offset):
        """Move cursor by specified offset.

        :type offset: int
        :param offset: The offset.
        """

        self.move_cursor(self.get_cursor() + offset)

    def is_end(self):
        """Get whether the stream is at the end.

        :rtype : bool
        :return: True if so.
        """

        return self.get_cursor() == len(self.get_script())

    def get_current_character(self):
        """Get current character.

        :rtype : str
        :return: The character.
        :raise IndexError: Raise this exception if the stream is a the end.
        """

        #  Safe check.
        if self.is_end():
            raise IndexError("End of script.")

        return self.get_script()[self.get_cursor()]

    def get_next_token(self):
        """Get next token.

        :rtype : Token
        :return: The token.
        :raise _error.ParserError: Raise this exception if some errors occurred.
        """

        while not self.is_end():
            #  Get the initial character of the token.
            initial_char = self.get_current_character()

            if initial_char.isdigit() or initial_char == "-":
                #
                #  Process operands.
                #

                #  Initialize.
                has_decimal_dot = False
                symbol = ""
                position = self.get_cursor()

                #  Read the operand.
                while not self.is_end():
                    #  Get current character.
                    current = self.get_current_character()
                    if current == ".":
                        if has_decimal_dot:
                            raise _error.ParserError("Duplicated decimal dot.")
                        else:
                            #  Append current character to the symbol.
                            symbol += current

                            #  Mark the decimal dot flag.
                            has_decimal_dot = True

                        #  Move the cursor.
                        self.move_cursor_by_offset(1)
                    elif current == "-":
                        if len(symbol) != 0:
                            raise _error.ParserError("Invalid minus operator.")
                        else:
                            #  Append current character to the symbol.
                            symbol += current

                        #  Move the cursor.
                        self.move_cursor_by_offset(1)
                    elif current.isdigit():
                        #  Append current character to the symbol.
                        symbol += current

                        #  Move the cursor.
                        self.move_cursor_by_offset(1)
                    elif current.isalpha():
                        raise _error.ParserError("Invalid operand.")
                    else:
                        break

                #  Create the token.
                if has_decimal_dot:
                    return Token.create_float_operand(symbol, position)
                else:
                    return Token.create_integer_operand(symbol, position)

            elif _is_separator(initial_char):
                #
                #  Process separators.
                #

                #  Read the separators.
                while (not self.is_end()) and _is_separator(self.get_current_character()):
                    self.move_cursor_by_offset(1)
            elif initial_char == "(":
                #
                #  Process left parentheses.
                #

                #  Save the position and move the cursor.
                position = self.get_cursor()
                self.move_cursor_by_offset(1)

                #  Create the token.
                return Token.create_left_parenthesis(position)
            elif initial_char == ")":
                #
                #  Process right parentheses.
                #

                #  Save the position and move the cursor.
                position = self.get_cursor()
                self.move_cursor_by_offset(1)

                #  Create the token.
                return Token.create_right_parenthesis(position)
            elif initial_char.isalpha():
                #
                #  Process symbols.
                #

                #  Initialize.
                symbol = ""
                position = self.get_cursor()

                #  Read the symbol.
                while not self.is_end():
                    #  Get current character.
                    current = self.get_current_character()

                    if current.isalpha() or current.isdigit():
                        #  Move the cursor.
                        self.move_cursor_by_offset(1)

                        #  Append current character to the symbol.
                        symbol += current
                    else:
                        break

                #  Create the token.
                return Token.create_symbol(symbol, position)
            else:
                raise _error.ParserError("Invalid character (code=\"%s\")." % ord(initial_char))

        return None

    def get_all_token(self):
        """Get all tokens.

        :rtype : list[Token]
        :return: The token list.
        """

        #  Initialize.
        tokens = []

        #  Read all tokens.
        while True:
            #  Get next token.
            current = self.get_next_token()
            if current is None:
                break

            #  Append current token to the list.
            tokens.append(current)

        return tokens
