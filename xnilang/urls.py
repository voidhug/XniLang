#!/usr/bin/env python
#
#  Copyright 2015 XiaoJSoft Studio.
#
#  Use of this source code is governed by a proprietary license. You can not read, change or
#  redistribute this source code unless you have a written authorization from the copyright
#  holder listed above.
#

#  Import other modules.
from django.conf.urls import patterns, url
import xnilang.request as _request

urlpatterns = patterns(
    "",
    url(r"^$", _request.index_page),
    url(r"^request/evaluate$", _request.code_evaluate)
)
