import React, { Component, PropTypes } from 'react';
import OrderSummary from './OrderSummary';
import OrderItems from './OrderItems';
import api from '../api/api';

class OrderDetail extends Component {

  handleFulfill() {
    console.log("Fulfill clicked!")
  }

  handleRefund() {
    console.log("Refund clicked!")
  }

  render() {
    let status = <span className="icon icon-warning">UNKNOWN&nbsp;</span>;
    let refundBtn = (
      <button
        onClick={() => this.handleRefund()}
        className="button button-secondary"
      >
        Refund
      </button>
    );

    if (this.props.order.status == 1) {
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
    else if (this.props.order.status == 2) {
      status = (
        <div>
          <span className="icon icon-warning">
            FULFILLED&nbsp;
                  </span>
          {refundBtn}
        </div>
      );
    }
    else if (this.props.order.status == 3) {
      status = <span className="icon icon-bin">CANCELLED</span>;
    };

    return (
      <div className="row">
        <h2>Order Summary</h2>
        <div className="row">
          {status}
        </div>
        <OrderSummary
          order={this.props.order}
          shippingAddress={this.props.order.shipping_address}
        />
        <h2>Order Items</h2>
        <OrderItems
          items={this.props.order.items}
          subTotal={this.props.order.total}
          shippingRate={parseFloat(this.props.order.shipping_rate)}
        />
      </div>
    );
  }
}

OrderDetail.propTypes = {

};

export default OrderDetail;
