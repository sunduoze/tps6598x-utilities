// Javascript handlers for the register.html page

function jsConfigHandler(selection, confField) {
    var postdata = { confname: confField, value: 0 };

    if (confField != 'update') {
        postdata.value = selection.value;
    }

    // TODO: server returns the new values of all fields in the register
    //     including hide attribute. Need to use to update the display
    //     with the callback (function below)
    $.post('/config_handler', postdata, function (data) {
        if (data['failure'] != 0) {
            alert(data['failure_message']) ;
        }
    });

    return false;
}

