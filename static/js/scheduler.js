$(function () {
// Submit scheduler on submit
    $('#scheds_form').on('submit', function (event) {
        event.preventDefault();

        var $validator = $('.wizard-card form').validate({
            rules: {
                username: {
                    required: true,
                    minlength: 3
                },
                telephone: {
                    required: true,
                    minlength: 7,
                    maxlength: 15,
                },
                address: {
                    required: true,
                    minlength: 6
                },
                // times: {
                //     required: true
                // }

            },
        });
        // Code for the Validator
        var $valid = $('.wizard-card form').valid();
        if (!$valid) {
            $validator.focusInvalid();
            return false;
        }
        create_scheduler();
        console.log("form submitted!");  // sanity check
    });


//Buttons


    $(document).on('click', '#wizard-radio', function (event) {
        $("#errors-modal").children().remove();
        var wizard = $(this).closest('.wizard-card');
        wizard.find('[data-toggle="wizard-radio"]').removeClass('active');
        $(this).addClass('active');
        wizard.find('[type="radio"]').removeAttr('checked');
        $(this).find('[type="radio"]').attr('checked', 'true');
    });

    var $tabShown = $('a[data-toggle="tab"]');

    $tabShown.on('show.bs.tab', function (e) {

        var $target = $(e.currentTarget);
        var $tab = $target.text().trim();
        var calenarBox = $("#calendar-box");
        if ($tab === 'Дата') {

            if (calenarBox.children().length === 0) {
                get_schedulers();
            }
        }

        if ($tab === 'Готово') {

            $('a[data-toggle="tab"]').addClass('hiden');
            $('.progress-bar').css({width: '100%'});
        }
    });

    $tabShown.on('click.bs.tab', function (e) {

        console.log('Click');
        var $target = $(e.currentTarget);
        var $tab = $target.text().trim();
        // var calenarBox = $("#calendar-box");

        if ($target.hasClass("hiden")) {
            e.preventDefault();
            return false;
        }

        if ($tab === 'Готово') {
            var $radioCheck = $('.wizard-card').find('#wizard-radio.active').is('.active');
            var $valid = $('.wizard-card form').valid();


            if (!$valid) {
                $('#wizard').bootstrapWizard('show', 0);
                return false;
            }
            if (!$radioCheck) {
                $("#errors-modal").html("<div class='alert alert-danger'>Выберите дату и время ремонта</div>");
                $('#wizard').bootstrapWizard('show', 1);
                return false;
            }

            create_scheduler();
            $('#wizard').bootstrapWizard('show', 2);

        }
    });


// AJAX for busy scheduler get
    function get_schedulers() {

        var urlBad = document.URL.split('/');
        var urlClean = urlBad[0] + "/" + urlBad[1] + "/" + urlBad[2] + "/";
        $.ajax({
            url: urlClean + "scheduler/get_scheds/", // the endpoint
            type: "POST", // http method
            data: {
                post_username: $('#username_input').val(),
            }, // data sent with the post request

            // handle a successful response
            success: function (data) {

                console.log("success"); // another sanity check

                // Получение свободных заявок
                var calendar_box = $("#calendar-box");
                calendar_box.empty();

                function sortObject(o) {
                    return Object.keys(o).sort().reduce((r, k) => (r[k] = o[k], r), {});
                }

                var sched_data = sortObject(data.busy_times);


                for (dates in sched_data) {
                    if (sched_data.hasOwnProperty(dates)) {

                        // Дата в номральном виде
                        var dateParsed = dates.match(/(\d{1,2})-(\d{1,2})-(\d{2,4})/);
                        var hum_date = new Date(dateParsed[3], dateParsed[2] - 1, dateParsed[1]).toLocaleString('ru', {
                            weekday: 'long',
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric'
                        });

                        console.log("Ключ = " + dates);
                        $("#calendar-box").append("<li class='calendar-day'>" + "<p class='calendar-day-header'>" + hum_date + "</p>" + "<div id='calendar-times-" + dates + "' class='btn-group btn-group-toggle' data-toggle='buttons'></div>" + "</li>");
                        var sched_times = sortObject(sched_data[dates]);
                        for (times in sched_times) {
                            if (sched_times.hasOwnProperty(times)) {
                                console.log("Значение = " + sched_times[times]);
                                $("#calendar-times-" + dates).append("<div id='wizard-radio' class='btn btn-secondary' data-toggle='wizard-radio'>" + "<input id='' name='times' value='" + times + "' data-date='" + dates + "' class='' type='radio' autocomplete='off'>" + sched_times[times] + "</div>");

                            }
                        }

                    }
                }
                // $('input[type = radio]:first').attr('checked', 'checked').parent().addClass('active')

            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        })
    }


// AJAX for scheduler add
    function create_scheduler() {

        var $checked_input = $('input[type = radio]:checked');
        var $sched_data = $checked_input.attr('data-date').split('-');
        var $clear_sched_data = $sched_data[2] + "-" + $sched_data[1] + "-" + $sched_data[0];
        var $sched_time = $checked_input.attr('value');

        var urlBad = document.URL.split('/');
        var urlClean = urlBad[0] + "/" + urlBad[1] + "/" + urlBad[2] + "/";

        $.ajax({
            url: urlClean + "scheduler/add/", // the endpoint
            type: "POST", // http method
            data: {
                post_username: $('#username_input').val(),
                post_address: $('#address_input').val(),
                post_telephone: $('#telephone_input').cleanVal(),
                post_comment: $('#comment_input').val(),
                post_repair_date: $clear_sched_data,
                post_repair_time: $sched_time,
                post_un_id: Math.random().toString(36).substr(2, 10),
            }, // data sent with the post request

            // handle a successful response
            success: function (data) {
                if (data['result'] === 'success') {
                    $("#errors-modal").children().remove();
                    $('#wizard').bootstrapWizard('show', 2);
                }
                if (data['result'] === 'has_send') {
                    $('#wizard').bootstrapWizard('show', 2);
                    $("#errors-modal").html("<div class='alert alert-danger'>" +
                        data['response'] + "</div>");
                }
                if (data['result'] === 'error') {
                    $("#errors-modal").html("<div class='alert alert-danger'>" +
                        data['response'] + "</div>");
                }
            },

            // handle a non-successful response
            error: function (request, status, error) {
                // console.log(err, xhr, errmsg);
                console.log(request.status + ": " + request.responseText); // provide a bit more info about the error to the console
            }
        });
    }
});

$(function () {

    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url === origin || url.slice(0, origin.length + 1) === origin + '/') ||
            (url === sr_origin || url.slice(0, sr_origin.length + 1) === sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});

jQuery.extend(jQuery.validator.messages, {
    required: "Это поле необходимо заполнить",
    remote: "Исправьте это поле чтобы продолжить",
    email: "Введите правильный email адрес.",
    url: "Введите верный URL.",
    date: "Введите правильную дату.",
    dateISO: "Введите правильную дату (ISO).",
    number: "Введите число.",
    digits: "Введите только цифры.",
    creditcard: "Введите правильный номер вашей кредитной карты.",
    equalTo: "Повторите ввод значения еще раз.",
    accept: "Пожалуйста, введите значение с правильным расширением.",
    maxlength: jQuery.validator.format("Нельзя вводить более {0} символов."),
    minlength: jQuery.validator.format("Должно быть не менее {0} символов."),
    rangelength: jQuery.validator.format("Введите от {0} до {1} символов."),
    range: jQuery.validator.format("Введите число от {0} до {1}."),
    max: jQuery.validator.format("Введите число меньше или равное {0}."),
    min: jQuery.validator.format("Введите число больше или равное {0}.")
});


$(document).ready(function ($) {

    $("#telephone_input").mask("(999) 999-99-99");

    $("#phone").on("blur", function () {
        var last = $(this).val().substr($(this).val().indexOf("-") + 1);

        if (last.length === 3) {
            var move = $(this).val().substr($(this).val().indexOf("-") - 1, 1);
            var lastfour = move + last;
            var first = $(this).val().substr(0, 9);

            $(this).val(first + '-' + lastfour);
        }
    });
});