#!/usr/bin/env python
#
#  Copyright 2015 XiaoJSoft Studio.
#
#  Use of this source code is governed by a proprietary license. You can not read, change or
#  redistribute this source code unless you have a written authorization from the copyright
#  holder listed above.
#


class FrameEvaluator:
    """Frame evaluator."""

    def __init__(self, canvas):
        """Initialize the evaluator.

        :type canvas: str
        :param canvas: The canvas name.
        """

        #  Initialize the script.
        self._script = ""

        #  Save the canvas name.
        self._canvas = canvas

        #  Emit the startup code.
        self._append_line("var $ctx = %s.getContext(\"2d\");" % canvas)
        self._append_line("$ctx.fillStyle = \"rgb(0, 0, 0)\";")
        self._append_line("$ctx.strokeStyle = \"rgb(0, 0, 0)\";")
        self._append_line("$ctx.lineWidth = 1;")

    def get_canvas(self):
        """Get the canvas name.

        :rtype : str
        :return: The name.
        """

        return self._canvas

    def _append_line(self, line):
        """Append a line to the script.

        :type line: str
        :param line: The line.
        """

        self._script += line
        self._script += "\n"

    def emit_clear(self):
        """Emit codes of clearing the canvas."""

        self._append_line("$ctx.clearRect(0, 0, %s.width, %s.height);" % (self.get_canvas(), self.get_canvas()))

    def emit_draw_line(self, x1, y1, x2, y2):
        """Emit codes of drawing a line.

        :type x1: int | float
        :type y1: int | float
        :type x2: int | float
        :type y2: int | float
        :param x1: The X axis value of the first point.
        :param y1: The Y axis value of the first point.
        :param x2: The X axis value of the second point.
        :param y2: The Y axis value of the second point.
        """

        self._append_line("$ctx.beginPath();")
        self._append_line("$ctx.moveTo(%s, %s);" % (str(x1), str(y1)))
        self._append_line("$ctx.lineTo(%s, %s);" % (str(x2), str(y2)))
        self._append_line("$ctx.closePath();")
        self._append_line("$ctx.stroke();")

    def emit_draw_circle(self, x, y, radius):
        """Emit codes of drawing a circle.

        :type x: int | float
        :type y: int | float
        :type radius: int | float
        :param x: The X axis value of the center point.
        :param y: The Y axis value of the center point.
        :param radius: The radius.
        """

        self._append_line("$ctx.beginPath();")
        self._append_line("$ctx.arc(%s, %s, %s, 0, 2 * Math.PI, false);" % (str(x), str(y), str(radius)))
        self._append_line("$ctx.closePath();")
        self._append_line("$ctx.stroke();")

    def get_script(self):
        """Get the emitted script.

        :rtype : str
        :return: The script.
        """

        return "{\n%s}" % self._script


class AnimationEvaluator:
    """Animation evaluator."""

    def __init__(self, interval, loop):
        """Initialize the animation evaluator.

        :type interval: int
        :type loop: bool
        :param interval: The interval.
        :param loop: Loop flag.
        """

        self._frames = []
        self._interval = interval
        self._loop = loop

    def get_interval(self):
        """Get the interval.

        :rtype : int
        :return: The interval.
        """

        return self._interval

    def is_loop(self):
        """Get whether the animation is looped.

        :rtype : bool
        :return: True if so.
        """

        return self._loop

    def add_frame(self, evaluator):
        """Add a frame.

        :type evaluator: FrameEvaluator
        :param evaluator: The frame evaluator.
        """

        self._frames.append(evaluator)

    def clear_frame(self):
        """Clear all frames."""

        self._frames.clear()

    def get_script(self):
        """Get the emitted script.

        :rtype : str
        :return: The script.
        """

        #  Emit all frames.
        script = "var $frames = [];\n"
        for frame_ev in self._frames:
            script += "$frames.push(function() {%s});\n" % frame_ev.get_script()

        #  Emit configurations.
        script += "var $interval = %d;\n" % self.get_interval()
        if self.is_loop():
            script += "var $loop = true;\n"
        else:
            script += "var $loop = false;\n"

        #  Emit the time-line controller.
        script += "var $current = 0;\n"
        script += "function next_frame() {\n"
        script += "    if ($current == $frames.length) {\n"
        script += "        return false;\n"
        script += "    } else {\n"
        script += "        $frames[$current].call(this);\n"
        script += "        $current++;\n"
        script += "        if ($current == $frames.length) {\n"
        script += "            if ($loop == true) {\n"
        script += "                $current = 0;\n"
        script += "                return true;\n"
        script += "            } else {\n"
        script += "                return false;\n"
        script += "            }\n"
        script += "        } else {\n"
        script += "            return true;\n"
        script += "        }\n"
        script += "    }\n"
        script += "}\n"
        script += "var $animator = setInterval(function() {\n"
        script += "    if (!next_frame()) {\n"
        script += "        clearInterval($animator);\n"
        script += "    }\n"
        script += "}, $interval);\n"

        return "{%s}" % script
