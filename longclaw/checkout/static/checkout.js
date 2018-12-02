
function initShippingOption(
  prefix,
  shippingCountrySelectId='id_shipping-country',
  shippingOptionSelectId='id_shipping_option') {
    var select = $('#' + shippingOptionSelectId);
    var countrySelect = $('#'+shippingCountrySelectId);
    countrySelect.unbind('change');
    countrySelect.change(function(e) {
      select.find('option').remove();
      longclawclient.shippingCountryOptions.get({
        prefix,
        urlParams: {
          country: countrySelect.val()
        }
      }).then((data) => {
          for (let i = 0; i < data.length; ++i) {
            var shippingRate = data[i];
            select.append($('<option />', {value: shippingRate.name, text: shippingRate.name}));
          }
      });
    });
}
