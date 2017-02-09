import React from 'react';
import ReactDOM from 'react-dom';

import OrderDetail from './OrderDetail'

const target = document.getElementById('order-app');
const order = window.initialData;
ReactDOM.render(
    <OrderDetail
      order={order}
    />,
  target
);
