import React from 'react';
import ReactDOM from 'react-dom';

import OrderDetail from './OrderDetail'

const target = document.getElementById('order-app');
ReactDOM.render(
    <OrderDetail
      orderId={target.dataset.orderId}
    />,
  target
);
