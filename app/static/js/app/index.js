/**
 * Created by Dmitry Astrikov on 26.02.14.
 */

$(function () {

    /**
     * Check that str is valid date in d.m.y format
     * @param str
     * @returns {boolean}
     */
    function isDate(str) {
        var t = str.match(/^(\d{2})\.(\d{2})\.(\d{4})$/);
        if (t === null)
            return false;
        var d = +t[1], m = +t[2], y = +t[3];
        if (m >= 1 && m <= 12 && d >= 1 && d <= 31) {
            return true;
        }
        return false;
    }

    /**
     * Initialization of controls in datatables.
     */
    var initDataTables = function () {
        $('.data-table td').on('click', function (e) {

            var t = e.target || e.srcElement,
                elm_name = t.tagName.toLowerCase(),
                val = $(this).html().trim();

            if (elm_name == 'input' || $(t).is(':first-child')) {
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
                        if (new_val != val)
                            if (isDate(new_val))
                                sendData(t, new_val);
                            else
                                alert('Введите корректную дату');
                    }
                }).datepicker("show");
            } else {
                $('#edit').focus();
                $('#edit').blur(function () {
                    var new_val = $(this).val().trim();
                    $(this).parent().empty().html(new_val);
                    if (new_val != val)
                        sendData(t, new_val);
                });
            }

        });
    };

    /**
     * Send new data to models.
     * @param el
     * @param new_val
     */
    var sendData = function (el, new_val) {
        var model_name = $(el).parents('table').attr('data-model'),
            model_pk = $(el).attr('data-model-pk'),
            field_index = $(el).attr('data-model-field-index');
        $.ajax({
            type: "POST",
            data: {
                model_name: model_name,
                model_pk: model_pk,
                field_index: field_index,
                value: new_val,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            }
        }).done(function (response) {
            if(response.result == 'error') {
                alert (response.error);
            }
        });
    };

    /**
     * Load model data into table.
     * @param model_name
     */
    var loadTable = function (model_name) {

        $.ajax({
            url: "/get-model/" + model_name + "/"
        }).done(function (response) {
                var table_wrapper = $('.table-wrapper');
                /**
                 * Build table
                 */
                var data_table = $("<table class='data-table' data-model='" + model_name + "'></table>"),
                    table_header = $("<thead><tr></tr></thead>"),
                    table_body = $("<tbody></tbody>");

                for (var i = 0; i < response.fields.length; i++) {
                    table_header.append("<th>" + response.fields[i] + "</th>")
                }

                $.each(response.data, function (data_index, data_value) {
                    var table_row = $("<tr></tr>");
                    $.each(data_value, function (field_index, field_value) {
                        var td_class = "";
                        if (isDate(field_value.toString())) {
                            td_class = "class='date'";
                        }
                        table_row.append("<td " + td_class + " data-model-field-index='" + field_index + "' data-model-pk='" + (data_index + 1) + "'>" + field_value + "</td>")
                    });
                    table_body.append(table_row);
                });

                data_table.append(table_header).append(table_body);
                table_wrapper.html(data_table);
                initDataTables();

                /**
                 * Build form
                 */
                var form = $("<form method='POST' id='id-form'></form>"),
                    model_name_inp = $('<input type="hidden" name="model_name" value="' + model_name + '"/>'),
                    submit_btn = $('<input type="submit"/>');
                form.append(response.form).append(model_name_inp).append(submit_btn);
                table_wrapper.append(form);
                var options = {
                    beforeSubmit: function() {
                        $('p.error').remove();
                    },
                    url: '/create/',
                    data: {
                        csrfmiddlewaretoken: $.cookie('csrftoken'),
                        model_name: model_name
                    },
                    success: function (response) {
                        if(response.result == 'success') {
                            $('.main-menu li.active a').click();
                        } else {
                            $.each(response.errors, function (index, value) {
                                $('#id_' + index).after('<p class="error">' + value + '</p>');
                            });
                        }

                    }
                };
                $('#id-form').ajaxForm(options);
            }
        )
        ;
    };

    /**
     * Tabs initialization
     */
    var initTabs = function () {
        var tabs = $('.main-menu li');
        $('a', tabs).on('click', function (e) {
            e.preventDefault();
            var model = $(this).attr('data-model');
            tabs.removeClass('active');
            $(this).parent().addClass('active');
            loadTable(model);
        });
    };

    /**
     * Start app.
     */
    initTabs();
    $('.main-menu li:first-child a').click();
})
;