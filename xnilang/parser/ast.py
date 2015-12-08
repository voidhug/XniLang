#!/usr/bin/env python
#
#  Copyright 2015 XiaoJSoft Studio.
#
#  Use of this source code is governed by a proprietary license. You can not read, change or
#  redistribute this source code unless you have a written authorization from the copyright
#  holder listed above.
#


class Node:
    """Base node class."""

    def __init__(self):
        """Initialize the node."""
        pass


class OperandNode(Node):
    """Operand node."""

    def __init__(self, value):
        """Initialize the operand node.

        :type value: int | float
        :param value: The operand value.
        """

        #  Let the base class to initialize.
        Node.__init__(self)

        #  Save the value.
        self._value = value

    def get_value(self):
        """Get the operand value.

        :rtype : int | float
        :return: The operand value.
        """

        return self._value


class TargetNode(Node):
    """Target node class."""

    def __init__(self, target_name):
        """Initialize the target node.

        :type target_name: str
        :param target_name: The target name.
        """

        #  Let base class to initialize.
        Node.__init__(self)

        #  Save the target name.
        self._target = target_name

    def get_target_name(self):
        """Get the target name.

        :rtype : str
        :return: The name.
        """

        return self._target


class PointNode(Node):
    """Point node."""

    def __init__(self, x, y):
        """Initialize the point node.

        :type x: OperandNode
        :type y: OperandNode
        :param x: The X axis value.
        :param y: The Y axis value.
        """

        #  Let the base class to initialize.
        Node.__init__(self)

        #  Save the axis values.
        self._x = x
        self._y = y

    def get_x(self):
        """Get the X axis value.

        :rtype : OperandNode
        :return: The value.
        """

        return self._x

    def get_y(self):
        """Get the Y axis value.

        :rtype : OperandNode
        :return: The value.
        """

        return self._y


class PointListNode(Node):
    """Point list node."""

    def __init__(self, point_list):
        """Initialize the point list node.

        :type point_list: list[PointNode]
        :param point_list: The point list.
        """

        #  Let base class initialize.
        Node.__init__(self)

        #  Save the point list.
        self._points = point_list

    def is_valid_index(self, idx):
        """Get whether an point index is valid.

        :param idx: The point index.
        :rtype : bool
        :return: True if so.
        """

        return 0 <= idx < self.get_point_count()

    def get_point_count(self):
        """Get the point count.

        :rtype : int
        :return: The count.
        """

        return len(self._points)

    def get_point(self, idx):
        """Get specified point by its index.

        :param idx: The point index.
        :rtype : PointNode
        :return: The point.
        :raise IndexError: Raise this exception if the index is invalid.
        """

        #  Safe check.
        if not self.is_valid_index(idx):
            raise IndexError("Invalid point index.")

        return self._points[idx]


class DirectionNode(Node):
    """Direction node."""

    def __init__(self, indicator):
        """Initialize the direction node.

        :type indicator: str
        :param indicator: The direction indicator.
        """

        #  Let the parent class initialize.
        Node.__init__(self)

        #  Safe check.
        if not DirectionNode.is_valid_indicator(indicator):
            raise ValueError("Invalid indicator.")

        #  Save the indicator.
        self._indicator = indicator

    @staticmethod
    def is_valid_indicator(indicator):
        """Get whether an indicator is valid.

        :type indicator: str
        :param indicator: The indicator.
        :rtype : bool
        :return: True if so.
        """

        return indicator in ["up", "down", "left", "right"]

    def get_indicator(self):
        """Get the direction indicator.

        :rtype : str
        :return: The indicator.
        """

        return self._indicator

    def is_up(self):
        """Get whether the direction is 'up'.

        :rtype : bool
        :return: True if so.
        """

        return self.get_indicator() == "up"

    def is_down(self):
        """Get whether the direction is 'down'.

        :rtype : bool
        :return: True if so.
        """

        return self.get_indicator() == "down"

    def is_left(self):
        """Get whether the direction is 'left'.

        :rtype : bool
        :return: True if so.
        """

        return self.get_indicator() == "left"

    def is_right(self):
        """Get whether the direction is 'right'.

        :rtype : bool
        :return: True if so.
        """

        return self.get_indicator() == "right"


class CommandNode(Node):
    """Base command node."""

    def __init__(self, cmd, args):
        """Initialize the command node.

        :type cmd: str
        :type args: list[Node]
        :param cmd: The command.
        :param args: The arguments.
        """

        #  Let the base class to initialize.
        Node.__init__(self)

        #  Save the command and the arguments.
        self._cmd = cmd
        self._args = args

    def get_command(self):
        """Get the command.

        :rtype : str
        :return: The command.
        """

        return self._cmd

    def get_argument_count(self):
        """Get the argument count.

        :rtype : int
        :return: The count.
        """

        return len(self._args)

    def is_valid_argument_index(self, idx):
        """Get whether an argument index is valid.

        :type idx: int
        :param idx:
        :rtype : bool
        :return: True if valid.
        """

        return 0 <= idx < self.get_argument_count()

    def get_argument(self, idx):
        """Get argument by index.

        :type idx: int
        :param idx: The index.
        :rtype : Node
        :return: The argument value.
        :raise IndexError: Raise this error if the index is invalid.
        """

        #  Safe check.
        if not self.is_valid_argument_index(idx):
            raise IndexError("Invalid argument index.")

        return self._args[idx]


class DrawCommand(CommandNode):
    """Base draw command node."""

    def __init__(self, cmd, args):
        """Initialize the draw command node.

        :type cmd: str
        :type args: list[Node]
        :param cmd: The command.
        :param args: The arguments.
        """

        CommandNode.__init__(self, cmd, args)


class MoveCommand(CommandNode):
    """Base move command node."""

    def __init__(self, cmd, args):
        """Initialize the move command node.

        :type cmd: str
        :type args: list[Node]
        :param cmd: The command.
        :param args: The arguments.
        """

        CommandNode.__init__(self, cmd, args)


class CircleCommand(DrawCommand):
    """Circle command node."""

    def __init__(self, center, radius):
        """Initialize the circle command node.

        :type center: PointNode
        :type radius: OperandNode
        :param center: The center of the circle.
        :param radius: The radius of the circle.
        """

        DrawCommand.__init__(self, "circle", [center, radius])

    def get_center(self):
        """Get the center of the circle.

        :rtype : PointNode
        :return: The center.
        """

        return self.get_argument(0)

    def get_radius(self):
        """Get the radius of the circle.

        :rtype : OperandNode
        :return: The radius.
        """

        return self.get_argument(1)


class LineCommand(DrawCommand):
    """Line command node."""

    def __init__(self, p1, p2):
        """Initialize the line command node.

        :type p1: PointNode
        :type p2: PointNode
        :param p1: The first point.
        :param p2: The second point.
        """

        DrawCommand.__init__(self, "line", [p1, p2])

    def get_point1(self):
        """Get the first point.

        :rtype : PointNode
        :return: The point.
        """

        return self.get_argument(0)

    def get_point2(self):
        """Get the second point.

        :rtype : PointNode
        :return: The point.
        """

        return self.get_argument(1)


class ClosedPathCommand(DrawCommand):
    """Closed path command node."""

    def __init__(self, point_list):
        """Initialize the closed path command node.

        :type point_list: PointListNode
        :param point_list: The point list.
        """

        #  Let the base class initialize.
        DrawCommand.__init__(self, "path", [point_list])

    def get_path(self):
        """Get the point list.

        :rtype : PointListNode
        :return: The point list.
        """

        return self.get_argument(0)


class CircleAreaCommand(DrawCommand):
    """Circle area command node."""

    def __init__(self, center, radius):
        """Initialize the circle area command node.

        :type center: PointNode
        :type radius: OperandNode
        :param center: The center point of the circle area.
        :param radius: The radius of the circle area.
        """

        #  Let base class initialize.
        DrawCommand.__init__(self, "area.circle", [center, radius])

    def get_center(self):
        """Get the center point of the circle area.

        :rtype : PointNode
        :return: The point.
        """

        return self.get_argument(0)

    def get_radius(self):
        """Get the radius of the circle area.

        :rtype : OperandNode
        :return: The radius.
        """

        return self.get_argument(1)


class SquareAreaCommand(DrawCommand):
    """Square area command node."""

    def __init__(self, center, width, height):
        """Initialize the square area command node.

        :type center: PointNode
        :type width: OperandNode
        :type height: OperandNode
        :param center: The center point of the square area.
        :param width: The width of the square area.
        :param height: The height of the square area.
        """

        #  Let the base class initialize.
        DrawCommand.__init__(self, "area.square", [center, width, height])

    def get_center(self):
        """Get the center point of the square area.

        :rtype : PointNode
        :return: The point.
        """

        return self.get_argument(0)

    def get_width(self):
        """Get the width of the square area.

        :rtype : OperandNode
        :return: The width.
        """

        return self.get_argument(1)

    def get_height(self):
        """Get the height of the square area.

        :rtype : OperandNode
        :return: The height.
        """

        return self.get_argument(2)


class ClosedPathAreaCommand(DrawCommand):
    """Closed path area command node."""

    def __init__(self, path):
        """Initialize the closed path area command.

        :type path: PointListNode
        :param path: The path.
        """

        #  Let the base class initialize.
        DrawCommand.__init__(self, "area.path", [path])

    def get_path(self):
        """Get the path.

        :rtype : PointListNode
        :return: The path.
        """

        return self.get_argument(0)


class PlaceCommand(MoveCommand):
    """Place command node."""

    def __init__(self, target, position):
        """Initialize the place command node.

        :type target: TargetNode
        :type position: PointNode
        :param target: The target.
        :param position: The position.
        """

        MoveCommand.__init__(self, "move", [target, position])

    def get_target(self):
        """Get the target.

        :rtype : TargetNode
        :return: The target.
        """

        return self.get_argument(0)

    def get_position(self):
        """Get the position.

        :rtype : PointNode
        :return: The position.
        """

        return self.get_argument(1)


class ShiftCommand(MoveCommand):
    """Shift command node."""

    def __init__(self, target, direction):
        """Initialize the shift command node.

        :type target: TargetNode
        :type direction: DirectionNode
        :param target: The target.
        :param direction: The direction.
        """
        
        MoveCommand.__init__(self, "shift", [target, direction])

    def get_target(self):
        """Get the target.

        :rtype : TargetNode
        :return: The target.
        """

        return self.get_argument(0)

    def get_direction(self):
        """Get the target.

        :rtype : DirectionNode
        :return: The target.
        """

        return self.get_argument(1)


class EraseCommand(MoveCommand):
    """Erase command node."""

    def __init__(self, target):
        """Initialize the erase command node.

        :type target: TargetNode
        :param target:
        """

        MoveCommand.__init__(self, "erase", [target])

    def get_target(self):
        """Get the target.

        :rtype : TargetNode
        :return: The target.
        """

        return self.get_argument(0)


class DrawList(Node):
    """Draw list node."""

    def __init__(self, commands):
        """Initialize the draw list node.

        :type commands: list[DrawCommand]
        :param commands: The commands.
        """

        #  Let the base class initialize.
        Node.__init__(self)

        #  Save the commands list.
        self._commands = commands

    def get_command_count(self):
        """Get the command count.

        :rtype : int
        :return: The count.
        """

        return len(self._commands)

    def is_valid_command_index(self, idx):
        """Get whether a command index is valid.

        :type idx: int
        :param idx: The index.
        :rtype : bool
        :return: True if so.
        """

        return 0 <= idx < self.get_command_count()

    def get_command(self, idx):
        """Get the command by the index.

        :type idx: int
        :param idx: The index.
        :rtype : DrawCommand
        :return: The command.
        :raise IndexError: Raise this exception if the index is invalid.
        """

        #  Safe check.
        if not self.is_valid_command_index(idx):
            raise IndexError("Invalid command index.")

        return self._commands[idx]


class MoveList(Node):
    """Move list node."""

    def __init__(self, commands):
        """Initialize the move list node.

        :type commands: list[MoveCommand]
        :param commands: The commands.
        """

        #  Let the base class initialize.
        Node.__init__(self)

        #  Save the commands list.
        self._commands = commands

    def get_command_count(self):
        """Get the command count.

        :rtype : int
        :return: The count.
        """

        return len(self._commands)

    def is_valid_command_index(self, idx):
        """Get whether a command index is valid.

        :type idx: int
        :param idx: The index.
        :rtype : bool
        :return: True if so.
        """

        return 0 <= idx < self.get_command_count()

    def get_command(self, idx):
        """Get the command by the index.

        :type idx: int
        :param idx: The index.
        :rtype : MoveCommand
        :return: The command.
        :raise IndexError: Raise this exception if the index is invalid.
        """

        #  Safe check.
        if not self.is_valid_command_index(idx):
            raise IndexError("Invalid command index.")

        return self._commands[idx]


class LoopCommand(MoveCommand):
    """Loop command node."""

    def __init__(self, times, move_list):
        """Initialize the loop command node.

        :type times: OperandNode
        :type move_list: MoveList
        :param times: The loop times.
        :param move_list: The move list.
        """

        MoveCommand.__init__(self, "loop", [times, move_list])

    def get_times(self):
        """Get loop times.

        :rtype : OperandNode
        :return: The times.
        """

        return self.get_argument(0)

    def get_move_list(self):
        """Get the move list.

        :rtype : MoveList
        :return: The list.
        """

        return self.get_argument(1)


class ObjectDefineCommand(CommandNode):
    """Object define command node."""

    def __init__(self, target, draw_list):
        """Initialize the object define command node.

        :type target: TargetNode
        :type draw_list: DrawList
        :param target: The target.
        :param draw_list: The draw list.
        """

        CommandNode.__init__(self, "define", [target, draw_list])

    def get_target(self):
        """Get the target.

        :rtype : TargetNode
        :return: The target.
        """

        return self.get_argument(0)

    def get_draw_list(self):
        """Get the draw list.

        :rtype : DrawList
        :return: The list.
        """

        return self.get_argument(1)
