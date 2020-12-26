// Javascript handlers for the register.html page

function jsExecHandler(iFunction, parent_type, parent_name) {
    var postdata = { function_name: iFunction, parent_type : parent_type, parent_name : parent_name };

    $('#content').load('/execute_function_inprocess', postdata, function () {
        $.ajax({
            type: 'POST',
            url: '/execute_function_complete',
            data: postdata,
            success: function (retHtml) {
                $('#content').html(retHtml);
                $('#connected_status').load('/test_connect');
            },
            dataType: "html",
            async: true
        });
    });

    return false;
}

function jsFuncChangeHandler(selection, iFunction, fieldnum, parent_type, parent_name) {
    var postdata = { func: iFunction, field: fieldnum, value: selection.value };
    if (selection.type == 'checkbox') {
        if (selection.checked) {
            postdata['value'] = 1;
        } else {
            postdata['value'] = 0;
        }
    }

    $.post('/infunc', postdata, function (data) {
        if (data['failure'] != 0) {
            alert('Field change failed with return: ' + data['failure_message']);
        }

        // Reload the function fields to display output
        load_hifunction(iFunction, false, parent_type, parent_name);
    });
    return false;
}
