import React, { Component, PropTypes } from 'react';
import OrderSummary from './OrderSummary';
import OrderItems from './OrderItems';
import api from '../api/api';

class OrderDetail extends Component {

  constructor(props) {
    super(props)

    this.state = {
      loading: true,
      order: null
    }

  }

  handleFulfill() {
    api.fulfillOrder({ prefix: this.props.urlPrefix, 
                       urlParams: { id: this.props.orderId }})
      .then(this.fetchOrder())
  }

  handleRefund() {
    console.log("Refund clicked!")
  }

  fetchOrder() {
    this.setState({ loading: true })
    api.getOrder({
      prefix: this.props.urlPrefix,
      urlParams: { id: this.props.orderId }})
      .then(json => this.setState({ loading: false, order: json }))
  }

  componentDidMount() {
    this.fetchOrder()
  }

  render() {
    if (this.state.loading) {
      return (
        <span>
          <i className="icon icon-spinner"></i>
        </span>
      );
    }
    const order = this.state.order;
    let status = <span className="icon icon-warning">UNKNOWN&nbsp;</span>;
    let refundBtn = (
      <button
        onClick={() => this.handleRefund()}
        className="button button-secondary"
        disabled
      >
        Refund
      </button>
    );

    if (order.status == 1) {
      status = (
        <div>
          <span className="icon icon-warning">
            UNFULFILLED&nbsp;
                  </span>
          <button onClick={() => this.handleFulfill()} className="button yes">Fulfill</button>
          {refundBtn}
        </div>
      );
    }
    else if (order.status == 2) {
      status = (
        <div>
          <span className="icon icon-warning">
            FULFILLED&nbsp;
                  </span>
          {refundBtn}
        </div>
      );
    }
    else if (order.status == 3) {
      status = <span className="icon icon-bin">CANCELLED</span>;
    };

    return (
      <div className="row">
        <h2>Order Summary</h2>
        <div className="row">
          {status}
        </div>
        <OrderSummary
          order={order}
          shippingAddress={order.shipping_address}
        />
        <h2>Order Items</h2>
        <OrderItems
          items={order.items}
          subTotal={order.total}
          shippingRate={parseFloat(order.shipping_rate)}
        />
      </div>
    );
  }
}

OrderDetail.propTypes = {

};

export default OrderDetail;
