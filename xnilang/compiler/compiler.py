#!/usr/bin/env python
#
#  Copyright 2015 XiaoJSoft Studio.
#
#  Use of this source code is governed by a proprietary license. You can not read, change or
#  redistribute this source code unless you have a written authorization from the copyright
#  holder listed above.
#

#  Import other modules.
import xnilang.compiler.error as _error
import xnilang.compiler.evaluator as _ev
import xnilang.parser.ast as _ast


class Compiler:
    """AST compiler class."""

    def __init__(self, evaluator, canvas):
        """Initialize the compiler.

        :type canvas: str
        :type evaluator: _ev.AnimationEvaluator
        :param evaluator: The animation evaluator.
        :param canvas: The canvas.
        """

        #  Clear all frames.
        evaluator.clear_frame()

        #  Save the evaluator.
        self._evaluator = evaluator

        #  Save the canvas.
        self._canvas = canvas

        #  Initialize the object manager.
        self._objects = {}

        #  Initialize the display list.
        self._display_list = []

        #  Initialize current frame.
        self._frame = None

    def get_canvas(self):
        """Get the canvas name.

        :rtype : str
        :return: The name.
        """

        return self._canvas

    @staticmethod
    def _compile_draw_command(base_x, base_y, cmd, frame):
        """Compile a draw command to a frame.

        :type base_x: int
        :type base_y: int
        :type cmd: _ast.DrawCommand
        :type frame: _ev.FrameEvaluator
        :param base_x: The base X axis value.
        :param base_y: The base Y axis value.
        :param cmd: The command.
        :param frame: The frame evaluator.
        """

        if isinstance(cmd, _ast.LineCommand):
            p1 = cmd.get_point1()
            p2 = cmd.get_point2()
            frame.emit_draw_line(base_x + p1.get_x().get_value(), base_y + p1.get_y().get_value(),
                                 base_x + p2.get_x().get_value(), base_y + p2.get_y().get_value())
        elif isinstance(cmd, _ast.CircleCommand):
            center = cmd.get_center()
            radius = cmd.get_radius().get_value()
            frame.emit_draw_circle(base_x + center.get_x().get_value(),
                                   base_y + center.get_y().get_value(),
                                   radius)
        elif isinstance(cmd, _ast.ClosedPathCommand):
            #  Convert.
            origin = cmd.get_path()
            path = []
            for point_id in range(0, origin.get_point_count()):
                point = origin.get_point(point_id)
                path.append((base_x + point.get_x().get_value(),
                             base_y + point.get_y().get_value()))

            #  Safe check.
            if len(path) < 3:
                raise _error.CompilationError("A path should contains at least 3 points.")

            #  Emit.
            frame.emit_draw_path(path)
        elif isinstance(cmd, _ast.CircleAreaCommand):
            center = cmd.get_center()
            radius = cmd.get_radius().get_value()
            frame.emit_draw_circle_area(base_x + center.get_x().get_value(),
                                        base_y + center.get_y().get_value(),
                                        radius)
        elif isinstance(cmd, _ast.SquareAreaCommand):
            center = cmd.get_center()
            width = cmd.get_width().get_value()
            height = cmd.get_height().get_value()
            frame.emit_draw_square_area(base_x + center.get_x().get_value(),
                                        base_y + center.get_y().get_value(),
                                        width,
                                        height)
        elif isinstance(cmd, _ast.ClosedPathAreaCommand):
            #  Convert.
            origin = cmd.get_path()
            path = []
            for point_id in range(0, origin.get_point_count()):
                point = origin.get_point(point_id)
                path.append((base_x + point.get_x().get_value(),
                             base_y + point.get_y().get_value()))

            #  Safe check.
            if len(path) < 3:
                raise _error.CompilationError("A path should contains at least 3 points.")

            #  Emit.
            frame.emit_draw_path_area(path)
        else:
            raise RuntimeError("Invalid command.")

    def _compile_object_define_command(self, cmd):
        """Compile an object-define command.

        :type cmd: _ast.ObjectDefineCommand
        :param cmd: The command.
        """

        #  Save the object.
        self._objects[cmd.get_target().get_target_name()] = {
            "Visible": False,
            "BaseX": 0,
            "BaseY": 0,
            "DrawList": cmd.get_draw_list()
        }

    def _redraw_to_frame(self, frame):
        """Redraw visible objects to a frame.

        :type frame: _ev.FrameEvaluator
        :param frame: The frame evaluator.
        """

        #  Clear the frame.
        frame.emit_clear()

        #  Draw objects.
        for disp_id in range(0, len(self._display_list)):
            #  Get the information.
            obj_info = self._objects[self._display_list[disp_id]]

            #  Do all draw commands.
            dw_list = obj_info["DrawList"]
            for dw_id in range(0, dw_list.get_command_count()):
                self._compile_draw_command(obj_info["BaseX"], obj_info["BaseY"], dw_list.get_command(dw_id), frame)

    def _macro_redraw(self):
        """(Macro) Redraw visible objects to a new animation frame."""

        #  Create the frame.
        frame = _ev.FrameEvaluator(self.get_canvas())

        #  Draw objects.
        self._redraw_to_frame(frame)

        #  Add the frame.
        self._evaluator.add_frame(frame)

    def _compile_move_command(self, cmd):
        """Compile a move command.

        :type cmd: _ast.MoveCommand
        :param cmd: The command.
        :raise _error.CompilationError: Raise this exception if an error occurred.
        """

        if isinstance(cmd, _ast.PlaceCommand):
            #  Get target and its position.
            target_name = cmd.get_target().get_target_name()
            position = cmd.get_position()

            #  Check target existence.
            if target_name not in self._objects:
                raise _error.CompilationError("No such target.")

            #  Remove the existed display object.
            if self._objects[target_name]["Visible"]:
                self._display_list.remove(target_name)

            #  Place the object to specified position.
            self._objects[target_name]["BaseX"] = position.get_x().get_value()
            self._objects[target_name]["BaseY"] = position.get_y().get_value()
            self._objects[target_name]["Visible"] = True

            #  Append the object onto the top of the list.
            self._display_list.append(target_name)

            #  Redraw.
            self._macro_redraw()
        elif isinstance(cmd, _ast.ShiftCommand):
            #  Get the target and its moving direction.
            target_name = cmd.get_target().get_target_name()
            direction = cmd.get_direction()

            #  Check target existence.
            if target_name not in self._objects:
                raise _error.CompilationError("No such target.")

            #  Check target visibility.
            if not self._objects[target_name]["Visible"]:
                raise _error.CompilationError("Target hasn't been placed.")

            #  Calculate the new X and Y axis values.
            x = self._objects[target_name]["BaseX"]
            y = self._objects[target_name]["BaseY"]
            if direction.is_up():
                y -= 1
            elif direction.is_down():
                y += 1
            elif direction.is_left():
                x -= 1
            elif direction.is_right():
                x += 1
            else:
                raise _error.CompilationError("Invalid direction.")

            #  Set the new X and Y axis values.
            self._objects[target_name]["BaseX"] = x
            self._objects[target_name]["BaseY"] = y

            #  Redraw.
            self._macro_redraw()
        elif isinstance(cmd, _ast.EraseCommand):
            #  Get the target.
            target_name = cmd.get_target().get_target_name()

            #  Check target existence.
            if target_name not in self._objects:
                raise _error.CompilationError("No such target.")

            #  Check target visibility.
            if not self._objects[target_name]["Visible"]:
                raise _error.CompilationError("Target hasn't been placed.")

            #  Mark the object as 'Invisible'.
            self._objects[target_name]["Visible"] = False

            #  Remove the object from the display list.
            self._display_list.remove(target_name)

            #  Redraw.
            self._macro_redraw()
        elif isinstance(cmd, _ast.LoopCommand):
            #  Get repeat times and the move-command list.
            times = int(cmd.get_times().get_value())
            move_list = cmd.get_move_list()

            #  Do repeating.
            for i in range(0, times):
                for mv_id in range(0, move_list.get_command_count()):
                    self._compile_move_command(move_list.get_command(mv_id))
        else:
            raise _error.CompilationError("Invalid command.")

    def compile_command(self, cmd):
        """Compile a command.

        :type cmd: _ast.CommandNode
        :param cmd: The command.
        :raise _error.CompilationError: Raise this exception if an error occurred.
        """

        if isinstance(cmd, _ast.ObjectDefineCommand):
            self._compile_object_define_command(cmd)
        elif isinstance(cmd, _ast.MoveCommand):
            self._compile_move_command(cmd)
        else:
            raise _error.CompilationError("Invalid command.")
