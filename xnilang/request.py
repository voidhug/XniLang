#!/usr/bin/env python
#
#  Copyright 2015 XiaoJSoft Studio.
#
#  Use of this source code is governed by a proprietary license. You can not read, change or
#  redistribute this source code unless you have a written authorization from the copyright
#  holder listed above.
#

#  Import other modules.
import django.http as _http
import xnilang.compiler.compiler as _cp_compiler
import xnilang.compiler.evaluator as _cp_evaluator
import xnilang.compiler.error as _cp_error
import xnilang.parser.error as _ps_error
import xnilang.parser.interpreter as _ps_ipt
import xnilang.parser.token as _ps_token


def index_page(request):
    """View of index page.

    :type request: _http.HttpRequest
    :param request: The request.
    :return: The response.
    """

    return _http.HttpResponseRedirect("/app/index.html")


def code_evaluate(request):
    """View of evaluating code.

    :type request: _http.HttpRequest
    :param request: The request.
    :return: The response.
    """

    #  Check the request method.
    if request.method != "POST":
        return _http.HttpResponseBadRequest("Invalid request.", content_type="text/plain")

    #  Check "script" section.
    if "script" not in request.POST:
        return _http.HttpResponseBadRequest("No \"script\" section.", content_type="text/plain")

    #  Parse and interpret.
    try:
        interpreter = _ps_ipt.Interpreter(_ps_token.Tokenizer(request.POST["script"]))
        evaluator = _cp_evaluator.AnimationEvaluator(20, True)
        compiler = _cp_compiler.Compiler(evaluator, "main")
        while not interpreter.is_end():
            compiler.compile_command(interpreter.interpret_command())
    except _ps_error.ParserError as err:
        return _http.HttpResponse(str(err), content_type="text/plain")
    except _cp_error.CompilationError as err:
        return _http.HttpResponse(str(err), content_type="text/plain")
    except Exception as err:
        return _http.HttpResponse(str(err), content_type="text/plain")

    #  Generate the reply.
    reply = "<html>\n"
    reply += "<head>\n"
    reply += "<link href=\"/app/styles/preview.css\" type=\"text/css\" rel=\"stylesheet\">"
    reply += "<script type=\"text/javascript\" src=\"/app/libraries/jquery/jquery-2.1.4.min.js\"></script>\n"
    reply += "<script type=\"text/javascript\">\n"
    reply += "function StartAnimation() {\n"
    reply += "var main = $(\"#main\")[0];"
    reply += evaluator.get_script() + "\n"
    reply += "}\n"
    reply += "</script>\n"
    reply += "<script type=\"text/javascript\" src=\"/app/scripts/preview.js\"></script>\n"
    reply += "</head>\n"
    reply += "<body>\n"
    reply += "<canvas id=\"main\" width=\"100px\" height=\"100px\"></canvas>"
    reply += "</body>\n"
    reply += "</html>\n"

    return _http.HttpResponse(reply, content_type="text/html")
