//
//  Copyright 2015 XiaoJSoft Studio.
//
//  Use of this source code is governed by a proprietary license. You can not read, change or
//  redistribute this source code unless you have a written authorization from the copyright
//  holder listed above.
//

$(document).ready(function() {
    //
    //  Resize part.
    //
    function OnResize() {
        var canvas = $("#main")[0];
        canvas.height = $(window).height();
        canvas.width = $(window).width();
    }

    //  Call OnResize() manually to let the canvas fit the window.
    OnResize();

    //  Bind resize event.
    $(window).resize(OnResize);

    //
    //  Animation part.
    //
    StartAnimation();
});