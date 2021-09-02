window.onload = function () {
  var _quantity, _price, order_item_num, delta_quantity, order_item_quantity, delta_cost;
  var quantity_arr = [];
  var price_arr = [];
  var total_forms = parseInt($('input[name=order_items-TOTAL_FORMS]').val());
  var order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
  var order_total_price = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;
  for (var i = 0; i < total_forms; i++) {
      _quantity = parseInt($('input[name=order_items-' + i + '-quantity]').val());
      _price = parseFloat($('.order_items-' + i + '-price').text().replace(',', '.'));
      quantity_arr[i] = _quantity;
      if (_price) {
          price_arr[i] = _price;
      } else {
          price_arr[i] = 0;
      }
  }
  if (!order_total_quantity) {
      for (var i = 0; i < total_forms; i++) {
          order_total_quantity += quantity_arr[i];
          order_total_price += quantity_arr[i] * price_arr[i];
      }
      $('.order_total_quantity').html(order_total_quantity.toString());
      $('.order_total_cost').html(Number(order_total_price.toFixed(2)).toString());
  }
  $('.order_form').on('click', 'input[type=number]', function () {
      var target = event.target;
      order_item_num = parseInt(target.name.replace('order_items-', '').replace('-quantity', ''));
      if (price_arr[order_item_num]) {
          order_item_quantity = parseInt(target.value);
          delta_quantity = order_item_quantity - quantity_arr[order_item_num];
          quantity_arr[order_item_num] = order_item_quantity;
          orderSummaryUpdate(price_arr[order_item_num], delta_quantity);
      }
  });
  function orderSummaryUpdate(order_item_price, delta_quantity) {
      delta_cost = order_item_price * delta_quantity;
      order_total_price = Number((order_total_price + delta_cost).toFixed(2));
      order_total_quantity = order_total_quantity + delta_quantity;
      $('.order_total_quantity').html(order_total_quantity.toString());
      $('.order_total_cost').html(order_total_price.toString() + ',00');
  }
  function deleteOrderItem(row) {
      var target_name = row[0].querySelector('input[type="number"]').name;
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
      removed: deleteOrderItem
  });
  if (!order_total_quantity) {
      orderSummaryRecalc();
  }
  function orderSummaryRecalc() {
      order_total_quantity = 0;
      order_total_price = 0;
      total_forms = parseInt($('input[name=order_items-TOTAL_FORMS]').val());
      for (var i = 0; i < total_forms; i++) {
          order_total_quantity += quantity_arr[i];
          order_total_price += quantity_arr[i] * price_arr[i];
      }
      $('.order_total_quantity').html(order_total_quantity.toString());
      $('.order_total_cost').html(Number(order_total_price.toFixed(2).toString()));
  }
  $('.order_form').on("change", "select", function () {
      var target = event.target;
      order_item_num = parseInt(target.name.replace('order_items-', '').replace('-product', ''));
      var order_item_product_pk = target.options[target.selectedIndex].value;
      if (order_item_product_pk) {
          $.ajax({
              url: '/orders/product/' + order_item_product_pk + '/price/',
              success: function (data) {
                  if (data.price) {
                      price_arr[order_item_num] = parseFloat(data.price);
                      if (isNaN(quantity_arr[order_item_num])) {
                          quantity_arr[order_item_num] = 0;
                      }
                      var price_html = '<span>' +  data.price.toString().replace('.', ',') +'</span> руб.';
                      var current_tr = $('.order_form table').find('tr:eq(' + (order_item_num + 1) + ')');
                      current_tr.find('td:eq(2)').html(price_html);
                      if (isNaN(current_tr.find('input[type="number"]').val())) {
                          current_tr.find('input[type="number"]').val(0);
                      }
                      orderSummaryRecalc();
                  }
              }
          });
      }
  });


}