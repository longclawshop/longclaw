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
The basic product page is missing a few things:

1. The fields we added to the model (vegetarian, gluten free) are not shown
2. Its not possible to add the product to the basket!
3. We can't see any information about the different variants

Lets deal with the most pressing first...

### Adding Products to the Basket

When a product has different variations, there are usually various different ways to display those variations and allow a customer to add one to their basket. 
For this reason, the longclaw project template doesn't include any markup for this.

We will cover a few options here, starting with what I am going to include in the bakery website.

#### Table display
Adding a product to the basket requires a HTTP request to be made to longclaw.
Longclaw makes this a bit easier for you by offering a helpful template tag to create an `Add To Basket` button for your product variants, which takes care of the javascript for you.
In your template, load the basket tags:

```django
  {% load basket_tags %}
```

You can now use the tag to render a button for each product variant:

```django
  {% add_to_basket_btn variant.id btn_text="Add To Basket" btn_class="btn btn-default" %}
```

In my bakery site, I am going to display these buttons along with more information about each variation in a table:

```django
<table>
    <thead>
        <tr>
        <th>Type</th>
        <th>Price</th>
        </tr>
    </thead>
    <tbody>
{% for variant in page.variants.all %}
<tr>
    <td><p>{{variant.ref}}</p></td>
    <td><p>&euro;{{variant.price}}</p></td>
    <td>
        {% if variant.stock > 0 %}
        {% add_to_basket_btn variant.id btn_text="Add To Basket" %}
        {% else %}
        <span class="label label-danger">Sold out</span>
        {% endif %}
    </td>
</tr>
{% endfor %}
</tbody>
</table>

```

#### Dropdown Selection

The idea here is to provide a dropdown to select a variant and a separate 'Add to Basket' button, such as this:

![Dropdown button](assets/dropdown-select.png)

The dropdown can be achieved with a simple `select` elemt:

```django
<select id="variant-select">
{% for variant in page.variants.all %}
  <option value="{{variant.id}}">{{variant.ref}}</option>
{% endfor %}
</select>      
```

We also need a button:
```django
  <button id="add-to-basket-btn">Add To Basket</button>
```

We then need to intercept the click event of the button to make the HTTP request:

```javascript
const btn = document.getElementById('add-to-basket-btn');
const select = document.getElementById('variant-select');

btn.addEventListener("click", (e) => {
  e.preventDefault();
  const variant_id = select.options[select.selectedIndex].value;
  longclawclient.basketList.post({
    prefix: "{% longclaw_api_url_prefix %}",
    data: { variant_id }
  });
});
```

Note two things in the javascript above - the use of `longclaw_api_url_prefix` and `longclawclient`. These require you to load the core template tags and the client javascript in your template. You can do this with the following lines in your django template:

```django
{% load longclawcore_tags %}

/* ...HTML */

{% longclaw_vendors_bundle %}
{% longclaw_client_bundle %}
```

The [Basket API](../guide/basket.md) also allows you to specify the quantity of an item to add.

#### Amazon style selection

## Navbar Basket Link

One other thing I want to have in my shop is the common 'basket' link in the nav bar. This would be easy enough, but I also want to show the number of items in my basket:

![Basket Link](assets/basket-link.png)

In `base.html` you will see that the project template already provided you with a basic top header bar:

```html
<div class="header">
</div>
```

I'm going to flesh it out to add my logo and links on the left and a basket icon on the right:

```html
<div class="header">
  <div class="nav-left">
    <a class="nav-brand" href="/">Longclaw Bakery</a>
    <a href="/products">Products</a>
  </div>

  <div class="nav-right">
    <a href="{% url 'longclaw_basket' %}"><span id="basket-item-count"> </span><i class="fas fa-shopping-basket fa-lg" aria-hidden="true"></i></a>
  </div>
</div>
```

Now some CSS:

```css
.header {
    grid-area: header;
    display: flex;
    flex-direction: row;
    justify-content: center;
    padding: 5px;
    background-color: var(--brand-primary)
}

.header-brand {
    flex: 1;
}
```


## Displaying the Basket

Now my online bakery is starting to really take shop. I can add new products, customers can browse them and add them to their basket.

So next, I have to allow our customers to actually see whats in their basket, edit it and proceed to checkout.

Longclaw provides a REST API endpoint for retrieving basket data and a django view. 

To use the django view, you must provide a template titled `basket/basket.html`. 
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
