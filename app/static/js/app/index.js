/**
 * Created by Dmitry Astrikov on 26.02.14.
 */

$(function () {
    /**
     * Initialization of controls in datatables.
     */
    var initDataTables = function () {
        $('.data-table td').on('click', function (e) {

            var t = e.target || e.srcElement,
                elm_name = t.tagName.toLowerCase(),
                val = $(this).html().trim();

            if (elm_name == 'input') {
                return false;
            }

            var code = '<input type="text" id="edit" value="' + val + '" />';
            $(this).empty().append(code);
            if ($(this).hasClass('date')) {
                $('#edit').datepicker({
                    dateFormat: "dd.mm.yy",
                    onClose: function () {
                        var new_val = $('#edit').val().trim();
                        $(this).parent().empty().html(new_val);
                        if(new_val != val)
                            sendRequest(t, new_val);
                    }
                }).datepicker("show");
            } else {
                $('#edit').focus();
                $('#edit').blur(function () {
                    var new_val = $(this).val().trim();
                    $(this).parent().empty().html(new_val);
                    if(new_val != val)
                        sendRequest(t, new_val);
                });
            }

        });
    };

    var sendRequest = function(el, new_val) {
        var model_name = $(el).parents('table').attr('data-model'),
            field_name = $(el).attr('data-model-field');
        $.ajax({
            type: "POST",
            data: {
                model_name: model_name,
                field_name: field_name,
                value: new_val,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            }
        }).done(function (response) {

        });
    };

    initDataTables();
});