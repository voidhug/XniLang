#!/usr/bin/env python
#
#  Copyright 2015 XiaoJSoft Studio.
#
#  Use of this source code is governed by a proprietary license. You can not read, change or
#  redistribute this source code unless you have a written authorization from the copyright
#  holder listed above.
#

#  Import other modules.
import xnilang.parser.ast as _ast
import xnilang.parser.token as _token
import xnilang.parser.error as _error


class Interpreter:
    """Tokens interpreter."""

    def __init__(self, tokenizer):
        """Initialize the interpreter.

        :type tokenizer: _token.Tokenizer
        :param tokenizer: The tokenizer.
        """

        self._tokens = tokenizer.get_all_token()
        self._cursor = 0

    def is_end(self):
        """Get whether the stream is at the end.

        :rtype : bool
        :return: True if so.
        """

        return self._cursor == len(self._tokens)

    def move_cursor(self, destination):
        """Move the cursor to specified destination.

        :type destination: int
        :param destination: The destination.
        :raise ValueError: Raise this exception if the destination is invalid.
        """

        #  Safe check.
        if destination < 0 or destination > len(self._tokens):
            raise ValueError("Invalid destination.")

        #  Set the cursor.
        self._cursor = destination

    def move_cursor_by_offset(self, offset):
        """Move the cursor by specified offset.

        :type offset: int
        :param offset: The offset.
        """

        self.move_cursor(self._cursor + offset)

    def get_current_token(self):
        """Get current token.

        :rtype : _token.Token
        :return: The token.
        :raise IndexError: Raise this exception if the stream is at the end.
        """

        #  Safe check.
        if self.is_end():
            raise IndexError("End of stream.")

        return self._tokens[self._cursor]

    def _interpret_operand(self):
        """Interpret an operand.

        :rtype : _ast.OperandNode
        :return: The operand.
        :raise _error.ParserError: Raise this exception if some errors occurred.
        """

        #  Safe check.
        if self.is_end():
            raise _error.ParserError("Missing operand.")

        #  Read an operand.
        operand = self.get_current_token()
        self.move_cursor_by_offset(1)

        #  Create the operand node.
        if operand.is_float_operand():
            return _ast.OperandNode(float(operand.get_symbol()))
        else:
            return _ast.OperandNode(int(operand.get_symbol()))

    def _interpret_left_parenthesis(self):
        """Interpret a left parenthesis.

        :raise _error.ParserError: Raise this exception if some errors occurred.
        """

        #  Safe check.
        if self.is_end():
            raise _error.ParserError("Missing parenthesis.")

        #  Read a parenthesis.
        parenthesis = self.get_current_token()
        self.move_cursor_by_offset(1)

        #  Check the operand type.
        if not parenthesis.is_left_parenthesis():
            raise _error.ParserError("Not a left parenthesis.")

    def _interpret_right_parenthesis(self):
        """Interpret a right parenthesis.

        :raise _error.ParserError: Raise this exception if some errors occurred.
        """

        #  Safe check.
        if self.is_end():
            raise _error.ParserError("Missing parenthesis.")

        #  Read a parenthesis.
        parenthesis = self.get_current_token()
        self.move_cursor_by_offset(1)

        #  Check the operand type.
        if not parenthesis.is_right_parenthesis():
            raise _error.ParserError("Not a right parenthesis.")

    def _interpret_point(self):
        """Interpret a point node.

        :rtype : _ast.PointNode
        :return: The point node.
        """

        #  Read the left parenthesis.
        self._interpret_left_parenthesis()

        #  Read the X and Y axis value.
        x = self._interpret_operand()
        y = self._interpret_operand()

        #  Read the right parenthesis.
        self._interpret_right_parenthesis()

        #  Create the node.
        return _ast.PointNode(x, y)

    def _interpret_symbol(self):
        """Interpret a symbol.

        :rtype : str
        :return: The symbol.
        :raise _error.ParserError: Raise this exception if some errors occurred.
        """

        #  Safe check.
        if self.is_end():
            raise _error.ParserError("Missing symbol.")

        #  Read a symbol.
        symbol = self.get_current_token()
        self.move_cursor_by_offset(1)

        if symbol.is_symbol():
            return symbol.get_symbol()
        else:
            raise _error.ParserError("Not a symbol.")

    def _interpret_target(self):
        """Interpret a target.

        :rtype : _ast.TargetNode
        :return: The target node.
        """

        return _ast.TargetNode(self._interpret_symbol())

    def _interpret_direction(self):
        """Interpret a direction.

        :rtype : _ast.DirectionNode
        :return: The direction node.
        :raise _error.ParserError: Raise this exception if some errors occurred.
        """

        #  Interpret the direction symbol.
        direction = self._interpret_symbol()

        #  Create the AST node.
        if direction in ["up", "down", "left", "right"]:
            return _ast.DirectionNode(direction)
        else:
            raise _error.ParserError("Invalid direction descriptor.")

    def interpret_command(self):
        """Interpret a command.

        :rtype : _ast.CommandNode
        :return: The command node.
        :raise _error.ParserError: Raise this exception if some errors occurred.
        """

        #  Read the left parenthesis.
        self._interpret_left_parenthesis()

        #  Read the command.
        cmd = self._interpret_symbol()

        if cmd == "line":
            #  Interpret two points.
            p1 = self._interpret_point()
            p2 = self._interpret_point()

            #  Read the right parenthesis.
            self._interpret_right_parenthesis()

            #  Create the AST node.
            return _ast.LineCommand(p1, p2)
        elif cmd == "circle":
            #  Read the center point.
            center = self._interpret_point()

            #  Read the circle radius.
            radius = self._interpret_operand()

            #  Read the right parenthesis.
            self._interpret_right_parenthesis()

            #  Create the AST node.
            return _ast.CircleCommand(center, radius)
        elif cmd == "define":
            #  Read the target.
            target = self._interpret_target()

            #  Read the draw list.
            draw_list = self._interpret_draw_list()

            #  Read the right parenthesis.
            self._interpret_right_parenthesis()

            #  Create the AST node.
            return _ast.ObjectDefineCommand(target, draw_list)
        elif cmd == "place":
            #  Read the target.
            target = self._interpret_target()

            #  Read the position.
            position = self._interpret_point()

            #  Read the right parenthesis.
            self._interpret_right_parenthesis()

            #  Create the AST node.
            return _ast.PlaceCommand(target, position)
        elif cmd == "shift":
            #  Read the target.
            target = self._interpret_target()

            #  Read the direction descriptor.
            direction = self._interpret_direction()

            #  Read the right parenthesis.
            self._interpret_right_parenthesis()

            #  Create the AST node.
            return _ast.ShiftCommand(target, direction)
        elif cmd == "erase":
            #  Read the target.
            target = self._interpret_target()

            #  Read the right parenthesis.
            self._interpret_right_parenthesis()

            #  Create the AST node.
            return _ast.EraseCommand(target)
        elif cmd == "loop":
            #  Read the loop times.
            times = self._interpret_operand()

            #  Read the move list.
            move_list = self._interpret_move_list()

            #  Read the right parenthesis.
            self._interpret_right_parenthesis()

            #  Create the AST node.
            return _ast.LoopCommand(times, move_list)
        else:
            raise _error.ParserError("Invalid command.")

    def _interpret_draw_list(self):
        """Interpret a draw list.

        :rtype : _ast.DrawList
        :return: The draw list.
        :raise _error.ParserError: Raise this exception if some errors occurred.
        """

        #  Read the left parenthesis.
        self._interpret_left_parenthesis()

        #  Initialize the command list.
        cmd_list = []

        while True:
            #  Safe check.
            if self.is_end():
                raise _error.ParserError("Missing list end.")

            if self.get_current_token().is_right_parenthesis():
                #  Stop interpreting if current token is a right parenthesis.
                break
            else:
                #  Read a draw command.
                draw_cmd = self.interpret_command()

                #  Type check.
                if not isinstance(draw_cmd, _ast.DrawCommand):
                    raise _error.ParserError("Not a draw command.")

                #  Append the command to the list.
                cmd_list.append(draw_cmd)

        #  Read the right parenthesis.
        self._interpret_right_parenthesis()

        #  Create the AST node.
        return _ast.DrawList(cmd_list)

    def _interpret_move_list(self):
        """Interpret a move list.

        :rtype : _ast.MoveList
        :return: The move list.
        :raise _error.ParserError: Raise this exception if some errors occurred.
        """

        #  Read the left parenthesis.
        self._interpret_left_parenthesis()

        #  Initialize the command list.
        cmd_list = []

        while True:
            #  Safe check.
            if self.is_end():
                raise _error.ParserError("Missing list end.")

            if self.get_current_token().is_right_parenthesis():
                #  Stop interpreting if current token is a right parenthesis.
                break
            else:
                #  Read a move command.
                move_cmd = self.interpret_command()

                #  Type check.
                if not isinstance(move_cmd, _ast.MoveCommand):
                    raise _error.ParserError("Not a move command.")

                #  Append the command to the list.
                cmd_list.append(move_cmd)

        #  Read the right parenthesis.
        self._interpret_right_parenthesis()

        #  Create the AST node.
        return _ast.MoveList(cmd_list)
