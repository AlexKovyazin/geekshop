window.onload = function () {
    let _quantity, _price, order_item_num, delta_quantity, order_item_quantity, delta_cost;
    let quantity_arr = [];
    let price_arr = [];
    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val());
    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_price = parseFloat($('order_total_cost').text().replace(',', '.')) || 0;
    for (let i = 0; i < total_forms; i++) {
        _quantity = parseInt($('input[name=order_items-' + i + '-quantity]').val());
        _price = parseFloat($('.order_items-' + i + '-price').text().replace(',', '.'));
        quantity_arr = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
    }
    if (!order_total_quantity) {
        for (let i = 0; i < total_forms; i++) {
            order_total_quantity += quantity_arr[i];
            order_total_price += quantity_arr[i] * price_arr[i];
        }
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(order_total_price.toFixed(2).toString());
    }
    $('order_form').on('click', 'input[type=number]', function () {
        let target = event.target;
        order_item_num = parseInt(target.name.replace('order_items-', '').replace('-quantity', ''));
        if (price_arr[order_item_num]) {
            order_item_quantity = parseInt(target.value);
            delta_quantity = order_item_quantity - quantity_arr[order_item_num];
            quantity_arr[order_item_num] = order_item_quantity;
            orderSummaryUpdate(price_arr[order_item_num], delta_quantity);
        }
    });
    $('.order_form').on('click', 'input[type="checkbox"]', function () {
       let target = event.target;
       order_item_num = parseInt(target.name.replace('order_items-', '').replace('-DELETE', ''));
       if (target.checked) {
           delta_quantity = -quantity_arr[order_item_num];
       } else {
           delta_quantity = quantity_arr[order_item_num];
       }
       orderSummaryUpdate(price_arr[order_item_num], delta_quantity);
    });
    function orderSummaryUpdate(order_item_price, delta_quantity) {
        delta_cost = order_item_price * delta_quantity;
        order_total_price = Number((order_total_price + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(order_total_price.toString() + ',00');
    }
    function deleteOrderItem(row) {
        let target_name = row[0].querySelector('input[type="number"]').name;
        order_item_num = parseInt(target_name.replace('order_items-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[order_item_num];
        quantity_arr[order_item_num] = 0;
        if (!isNaN(price_arr[order_item_num]) && !isNaN(delta_quantity)) {
            orderSummaryUpdate(price_arr[order_item_num], delta_quantity);
        }
    }
    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'order_items',
        remove: deleteOrderItem
    });

}