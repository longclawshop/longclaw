---
title: Displaying Products
sidebar_label: Frontend
---

You will see that if you click on `View` for the products or product index, you will taken to a basic product index or product page.
You will find the HTML templates for these pages in `catalog/templates/catalog`.
This basic template uses CSS grid to show the products as a grid of 'cards'.
You can check out the CSS in `longclaw_bakery/static/css/longclaw_bakery.css`.
The CSS is included in `longclaw_bakery/templates/base.html` which our `product_index.html` extends.

> The Wagtail documentation also has some comprehensive documentation on [writing templates for Pages](http://docs.wagtail.io/en/v1.9/topics/writing_templates.html).

For more complex projects, you might want to use Sass and/or other frontend libraries. In this case you might want to look at using Webpack to bundle your static assets. There are some [useful guides](https://owais.lone.pw/blog/webpack-plus-reactjs-and-django/) out there to help you.


## Improving the product page



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
