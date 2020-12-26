// Javascript handlers for the register.html page

function jsOnChangeHandler(selection, iRegister, fieldnum, parent_type, parent_name) {
    var postdata = { register: iRegister, field: fieldnum, value: selection.value };
    if (selection.type == 'checkbox') {
        if (selection.checked) {
            postdata['value'] = 1;
        } else {
            postdata['value'] = 0;
        }
    }
    // TODO: server returns the new values of all fields in the register
    //     including hide attribute. Need to use to update the display
    //     with the callback (function below)
    $.post('/submit', postdata, function (data) {
        if (data['failure'] != 0) {
            alert('Field change failed with return: ' + data['failure_message']) ;
        }

        // Reload the register fields
        // Don't force a re-read from the device or it will overwrite field change
        postdata2 = { register: register_name, read: 'false', parent_type: parent_type, parent_name: parent_name };

        $('#content').load('/access_register', postdata2, function () {});
    });
    return false;
}

function jsReadHandler(iRegister, parent_type, parent_name) {
    load_register(iRegister, 'true', parent_type, parent_name);
    return false;
}

function jsWriteHandler(iRegister, parent_type, parent_name) {
    var postdata = { register: iRegister };
    // TODO: server returns the new values of all fields in the register
    //     including hide attribute. Need to use to update the display
    //     with the callback (function below)
    $("#regaccessstatus").html('Register Write In Progress')

    $.post('/write', postdata, function (data) {
        if (data['failure'] != 0) {
            $("#regaccessstatus").html('Register Write FAILURE:\n' + data['failure_message'])
        }

        // Reload the register fields
        // Don't force a re-read from the device or it will overwrite field change
        postdata2 = { register: iRegister, read: 'false', parent_type: parent_type, parent_name: parent_name };

        $('#content').load('/access_register', postdata2, function () {
            $("#regaccessstatus").html('Register Write SUCCESS')
        });
    });
    return false;
}

function clearStatusHandler() {
    $("#regaccessstatus").html('')
}