//
//  Copyright 2015 XiaoJSoft Studio.
//
//  Use of this source code is governed by a proprietary license. You can not read, change or
//  redistribute this source code unless you have a written authorization from the copyright
//  holder listed above.
//

$(document).ready(function() {
    //
    //  Window resize part.
    //
    function OnResize() {
        $(".container").css({
            "top": $(window).height() / 2 - 200,
            "left": $(window).width() / 2 - 320
        });
    }
    $(window).resize(OnResize);
    OnResize();

    //
    //  Page controller.
    //
    function ShowCodePage() {
        $("#code_page").show();
        $("#preview_page").hide();
    }

    function ShowPreviewPage() {
        $("#code_page").hide();
        $("#preview_page").show();
    }

    //  Show code page by default.
    ShowCodePage();

    //
    //  Button events.
    //
    $("#eval_button").kendoButton({
        "click": function() {
            $("#submit_form_script")[0].value = $("#code_box")[0].value;
            $("#submit_form").submit();
            ShowPreviewPage();
        }
    });
    $("#back_button").kendoButton({
        "click": function() {
            ShowCodePage();
        }
    });
});