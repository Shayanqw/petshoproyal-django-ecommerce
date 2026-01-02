$('.ui.dropdown').dropdown({
    forceSelection: false
});

const provincesDataBox = document.getElementById('provinces-data-box')
const provinceInput = document.getElementById('provinces')

const citiesDataBox = document.getElementById('cities-data-box')
const cityInput = document.getElementById('cities')

const cityText = document.getElementById('city-text')

//provinces-json
$.ajax({
    type: 'GET',
    url: '{% url "cart:provinces-json" %}',
    success: function (responce) {
        console.log(responce.data)
        const provincesData = responce.data
        provincesData.map(item => {
            const option = document.createElement('div')
            option.textContent = item.name
            option.setAttribute('class', 'item')
            option.setAttribute('data-value', item.id)
            provincesDataBox.appendChild(option)
        })
    },
    error: function (error) {
        console.log(error)
    }
})

provinceInput.addEventListener('change', e => {
    console.log(e.target.value)
    const selectedProvince = e.target.value

    citiesDataBox.innerHTML = ''
    cityText.textContent = 'شهر'
    cityText.classList.add('default')


    $.ajax({
        type: 'GET',
        url: `city-json/${selectedProvince}/`,
        success: function (responce) {
            console.log(responce.data)
            const citiesData = responce.data
            citiesData.map(item => {
                const option = document.createElement('div')
                option.textContent = item.name
                option.setAttribute('class', 'item')
                option.setAttribute('data-value', item.id)
                citiesDataBox.appendChild(option)
            })
        },
        error: function (error) {
            console.log(error)
        }
    })
})

(function ($) {
    $.fn.niceNumber = function (options) {
        var defaults = {
            autoSize: true,
            autoSizeBuffer: 1,
            buttonDecrement: '-',
            buttonIncrement: '+',
            buttonPosition: 'around',

            /**
             callbackFunction
             @param {$input} currentInput - the input running the callback
             @param {number} amount - the amount after increase/decrease
             @param {object} settings - the passed niceNumber settings
             **/
            onDecrement: false,
            onIncrement: false,
        };
        var settings = $.extend(defaults, options);

        return this.each(function () {
            var currentInput = this,
                $currentInput = $(currentInput),
                maxValue = $currentInput.attr('max'),
                minValue = $currentInput.attr('min'),
                attrMax = null,
                attrMin = null;

            // Skip already initialized input
            if ($currentInput.attr('data-nice-number-initialized')) return;

            // Handle max and min values
            if (
                maxValue !== undefined &&
                maxValue !== false
            ) {
                attrMax = parseFloat(maxValue);
            }

            if (
                minValue !== undefined &&
                minValue !== false
            ) {
                attrMin = parseFloat(minValue);
            }

            // Fix issue with initial value being < min
            if (attrMin && !currentInput.value) {
                $currentInput.val(attrMin);
            }

            // Generate container
            var $inputContainer = $('<div/>', {
                class: 'nice-number',
            }).insertAfter(currentInput);

            // Generate interval (object so it is passed by reference)
            var interval = {};

            // Generate buttons
            var $minusButton = $('<button/>')
                .attr('type', 'button').attr('class', 'changeQuantity btn btn-hover-primary p-2 ')
                .html(settings.buttonDecrement)
                .on('mousedown mouseup mouseleave', function (event) {
                    changeInterval(event.type, interval, function () {
                        var currentValue = parseFloat($currentInput.val() || 0);
                        if (
                            attrMin == null ||
                            attrMin < currentValue
                        ) {
                            var newValue = currentValue - 1;
                            $currentInput.val(newValue);
                            if (settings.onDecrement) {
                                settings.onDecrement(
                                    $currentInput,
                                    newValue,
                                    settings
                                );
                            }
                        }
                    });

                    // Trigger the input event here to avoid event spam
                    if (event.type == 'mouseup' || event.type == 'mouseleave') {
                        $currentInput.trigger('input');
                    }
                });

            var $plusButton = $('<button/>')
                .attr('type', 'button').attr('class', 'changeQuantity btn btn-hover-primary p-2 ')
                .html(settings.buttonIncrement)
                .on('mousedown mouseup mouseleave', function (event) {
                    changeInterval(event.type, interval, function () {
                        var currentValue = parseFloat($currentInput.val() || 0);
                        if (
                            attrMax == null ||
                            attrMax > currentValue
                        ) {
                            var newValue = currentValue + 1;
                            $currentInput.val(newValue);
                            if (settings.onIncrement) {
                                settings.onIncrement(
                                    $currentInput,
                                    newValue,
                                    settings
                                );
                            }
                        }
                    });

                    // Trigger the input event here to avoid event spam
                    if (event.type == 'mouseup' || event.type == 'mouseleave') {
                        $currentInput.trigger('input');
                    }
                });

            // Remember that we have initialized this input
            $currentInput.attr('data-nice-number-initialized', true);

            // Append elements
            switch (settings.buttonPosition) {
                case 'left':
                    $minusButton.appendTo($inputContainer);
                    $plusButton.appendTo($inputContainer);
                    $currentInput.appendTo($inputContainer);
                    break;
                case 'right':
                    $currentInput.appendTo($inputContainer);
                    $minusButton.appendTo($inputContainer);
                    $plusButton.appendTo($inputContainer);
                    break;
                case 'around':
                default:
                    $plusButton.appendTo($inputContainer);
                    $currentInput.appendTo($inputContainer);
                    $minusButton.appendTo($inputContainer);

                    break;
            }

            // Nicely size input
            if (settings.autoSize) {
                $currentInput.width(
                    $currentInput.val().length + settings.autoSizeBuffer + 'ch'
                );
                $currentInput.on('keyup input', function () {
                    $currentInput.animate(
                        {
                            width:
                                $currentInput.val().length +
                                settings.autoSizeBuffer +
                                'ch'
                        },
                        200
                    );
                });
            }
        });
    };

    function changeInterval(eventType, interval, callback) {
        if (eventType == 'mousedown') {
            interval.timeout = setTimeout(function () {
                interval.actualInterval = setInterval(function () {
                    callback();
                }, 100);
            }, 200);
            callback();
        } else {
            if (interval.timeout) {
                clearTimeout(interval.timeout);
            }
            if (interval.actualInterval) {
                clearInterval(interval.actualInterval);
            }
        }
    }
})(jQuery);

$('.qty-input').niceNumber({
    autoSize: false,

});

$('.changeQuantity').click(function (e) {
    e.preventDefault()

    let product_id = $(this).closest('.product_data').find('.prod_id').val()
    let product_qty = $(this).closest('.product_data').find('.qty-input').val();
    let token = $('input[name=csrfmiddlewaretoken]').val();

    let total_price = $(this).closest('.product_data').find('.total_price').text()
    var total = parseFloat(total_price) * parseFloat(product_qty)
    $(this).closest('.product_data').find('.final_price').html(total)

    console.log(total_price)


    $.ajax({
        method: "POST",
        url: "{% url 'cart:updatecart' %}",
        data: {
            'product_id': product_id,
            'product_qty': product_qty,
            csrfmiddlewaretoken: token
        },
        success: function (response) {
            console.log('ok')
        }
    })
})