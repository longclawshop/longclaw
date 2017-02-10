import React, { PropTypes } from 'react';

const propTypes = {
  items: PropTypes.array.isRequired,
  subTotal: PropTypes.number.isRequired,
  shippingRate: PropTypes.number.isRequired
};

const OrderItems = ({items, subTotal, shippingRate}) => (
  <table className="listing">
    <thead>
      <tr>
        <th>Product</th>
        <th>Variant Ref</th>
        <th>Item Price</th>
        <th>Quantity</th>
        <th>Total</th>
      </tr>
    </thead>
    <tbody>
    {items.map(item => (
      <tr key={item.id}>
        <td>
          <a href={`/admin/pages/${item.product.product.id}/edit/`}>
            {item.product.product.title}
          </a>
        </td>
        <td>{item.product.ref}</td>
        <td>{item.product.price}</td>
        <td>{item.quantity}</td>
        <td>{item.total}</td>
      </tr>
    ))}
    </tbody>
    <tfoot>
      <tr>
          <td></td>
          <td></td>
          <td></td>
          <td>Subtotal</td>
          <td>{subTotal}</td>
      </tr>
      <tr>
          <td></td>
          <td></td>
          <td></td>
          <td>Shipping</td>
          <td>{shippingRate}</td>
      </tr>
      <tr>
          <td></td>
          <td></td>
          <td></td>
          <td><strong>Total</strong></td>
          <td><strong>{subTotal+shippingRate}</strong></td>
      </tr>
      </tfoot>   
  </table>
);

OrderItems.propTypes = propTypes;

export default OrderItems;
