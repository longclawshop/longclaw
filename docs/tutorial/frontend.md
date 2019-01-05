---
title: Displaying Products
sidebar_label: Frontend
---

Now we have created products and configured our shipping, we can start thinking about actually displaying the products to our customers.

Since `ProductIndex` and `Product` are Wagtail pages, we write templates for them just like any other page.
The Wagtail documentation already comprehensively covers [writing templates](http://docs.wagtail.io/en/v1.9/topics/writing_templates.html).

Our template project already has some basic templates for `ProductIndex` and `Product`:

- `my_shop/my_shop/templates/products/product_index.html`
- `my_shop/my_shop/templates/products/product.html`

They contain just enough information to demonstrate how to traverse the products and their fields.
For a more complete template, take a look at the [demo project](https://github.com/JamesRamm/longclaw_demo).

### Adding Products to the Basket


Longclaw offers a helpful template tag to create an `Add To Basket` button for your products.
In your template, load the basket tags:

```django
  {% load basket_tags %}
```

You can now use the tag to render a button for each product variant:

```django
  {% add_to_basket_btn variant.id btn_text="Add To Basket" btn_class="btn btn-default" %}
```

If you wish to create a button manually, you can handle the click event by making an AJAX call to the longclaw API.
Situations where you would prefer this over the tempaltetag might be to support non-button elements, such as
dropdown buttons, or for React-based frontends.

Here is an example with a single button whose 'variant id' will change depending on the selection in a dropdown box.
We can acheive the drop down like this:

```django
    <dl>
        <dt>Format</dt>
        <dd>
        <div class="col-md-6">
            <select id="variant-select">
            {% for variant in page.variants.all %}
            <option value="{{variant.id}}">{{variant.music_format}}</option>
            {% endfor %}
            </select>
        </div>
        </dd>
    </dl>
```

Add a button:

```django

  <button id="add-button">Add To Basket</button>
```

We can then write a jquery function to handle the click event:

```javascript

  $('#add-button').click(function () {
    // Selected variant
    var variant_id = $('#variant-select option:selected').val();

    // Add to the basket
    $.post("api/add_to_basket/", { variant_id: variant_id });
  });
```

This is a basic example of integrating with the basket. You will likely need to incorporate more
complex designs such as displaying a count of items in the basket, allowing the user to increase/decrease
quantity and so on. The [basket API](#basket) allows all such interactions and all front end design decisions such as these are left up to the developer.
It is worthwhile looking at the longclaw demo source code to see how e.g. a basket & item count in the page header is implemented.



## Displaying the Basket

Longclaw provides a REST API endpoint for retrieving basket data and a django view. 

To use the django view, we must provide a template titled `basket/basket.html`. 
It is common to provide a link to the basket page in the header. We can use the `url` tag in
our site header to provide the link:

```
{% url 'longclaw-basket' %}
```

In the basket template, we have access to all basket items under the `basket` context:

```
{% for item in basket %}
...
{% endfor %}
```

For the full implementation of the basket template, take a look at the [longclaw demo repository](https://github.com/JamesRamm/longclaw_demo/blob/master/longclaw_demo/templates/basket/basket.html)
