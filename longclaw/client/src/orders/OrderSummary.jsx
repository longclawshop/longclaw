import React, { PropTypes } from 'react';

const OrderSummary = ({order, shippingAddress}) => (
  <div className="row">
    <div className="col4">
      <dl>
        <dt>Order Date</dt>
        <dd>{order.payment_date}</dd>
      </dl>
      <dl>
        <dt>Shipping Address</dt>
        <dd>
          <address>
            {shippingAddress.name}<br />
            {shippingAddress.line_1}<br />
            {shippingAddress.city}<br />
            {shippingAddress.postcode}<br />
            {shippingAddress.country}<br />
          </address>
        </dd>
      </dl>
    </div>
    <div className="col4">
      <dl>
        <dt>Customer Email</dt>
        <dd>{order.email}</dd>
      </dl>
    </div>
    <div className="col4">
      <dl>
        <dt>Status Note</dt>
        <dt>{order.status_note}</dt>
      </dl>
    </div>
  </div>
);

OrderSummary.propTypes = {
  order: PropTypes.shape({
    payment_date: PropTypes.string,
    email: PropTypes.string,
    status_note: PropTypes.string
  }).isRequired,
  shippingAddress: PropTypes.shape({
    name: PropTypes.string,
    line_1: PropTypes.string,
    city: PropTypes.string,
    postcode: PropTypes.string,
    country: PropTypes.string
  }).isRequired
}

export default OrderSummary;
