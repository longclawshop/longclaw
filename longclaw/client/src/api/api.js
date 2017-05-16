/**
 * Client endpoints for interacting with the longclaw API
 */
import { fromJS } from 'immutable';
import {
  composeParams,
  checkStatus,
  parseJSON,
  getRequestHeaders,
  genericState,
  get,
  post,
  put,
  del
} from './helpers'

/*
 * Wraps all logic for:
 *  - calling an api endpoint
 *  - creating a redux action
 *  - creating a redux reducer
 * into a generic interface.
 * Redux 'thunk' actions are automatically created for the given
 * endpoint, with unique actions being dispatched when the
 * endpoint is called, when the request completes or if there is
 * an error.
 * A reducer is provided containing:
 *  - a 'loading' property
 *  - an 'error' property and 'errorData' property
 *  - a 'data' property. This will contain all data returned from the API.
 *
 * The advantages of this class are:
 *
 *  - Provides a consistent interface for redux actions & reducers
 *  - Only a single object (the class instance) needs to be passed around, rather
 *  than seperate functions for api, actions, reducers & action constants - makes it
 *  easier to trace logic/data flow.
 */
class ApiEndpoint {

  /*
   * @param {string} endpoint - the API url endpoint. It should not include the
   *  prefix (e.g. '/api/v1/'). It may include replacement values (url parameters)
   *  surrounded by braces, e.g.: 'bookings/booking/{id}/'
   *
   * @param {func} requestFunction - the request function to call from './request.js'
   *  e.g. `get` or `post`
   *
   * @param {object} config - Optional configuration object
   * @param {bool} config.form - Whether the endpoint expects form data
   * @param {bool} config.json - Whether the endpoint returns json data
   *  (only applies to post/put/patch/del)
   * @param {string} config.prefix - A prefix to attach to all endpoints.
   *  Defaults to '/api/v1/'
   * @param {func} config.actionFilter - Function to filter data (successfully)
   *  returned from the api in the `action` method.
   * @param {object} config.initialState - immutableJS object to use as the initial
   *  state for the reducer. Defaults to { loading: true,
                                           error: false,
                                           errorData: {},
                                           data: {},
                                           config: {} }
   */
  constructor(endpoint, config = {}) {
    // Default configuration
    this.config = {
      form: false, // true if the endpoint expects form data
      json: false, // true if the endpoint returns json
      prefix: '',
      actionFilter: data => data,
      initialState: fromJS(genericState),
      ...config
    };
    this.endpoint = endpoint;

   // Bind methods so they can be passed around
    this.get = this.get.bind(this);
    this.post = this.post.bind(this);
    this.del = this.del.bind(this);
    this.put = this.put.bind(this);
    this.action = this.action.bind(this);
    this.reducer = this.makeReducer(this.config.initialState);
  }

 composeUrl(config = {}) {
    // Url can be overridden in the config
    let url = config.url || `${this.config.prefix}${this.endpoint}`;
    if (config.prefix) {
      url = `${config.prefix}${url}`;
    }
    if (config.urlParams) {
      Object.keys(config.urlParams).map((key) => {
        url = url.replace(`{${key}}`, config.urlParams[key]);
      });
    }
    if (config.queryParams) {
      url = `${url}?${composeParams(config.queryParams)}`;
    }
    return url
  }

   /*
   * Make a GET request.
   * Returns a Promise
   *
   * @param {object} config - Configuration object
   * @param {string} config.url - Completely override the URL to use
   * @param {string} config.prefix - Use a different prefix or host for calling the endpoint.
   * @param {object} config.urlParams - replacement parameters for the endpoint.
   *  for example, if the endpoint is specified as `booking/{id}/`, urlParams should
   *  be an object containing an `id` key and the string to replace it with, e.g:
   *  { id: '123' } would result in the endpoint being modified to `booking/123/`
   *
   * @param {object} config.queryParams - An object containing key-value pairs which
   *  will be mapped to a query string. E.g.
   *  {
   *    first_name: 'John',
   *    last_name: 'Smith'
   *  }
   *  would result in the endpoint being modified to `booking/123/?first_name=John&last_name=Smith`
   *
   * @param {object} config.data - Data to send with the POST/PUT request. Will be converted to JSON.
   */
  get(config = {}) {
    const url = this.composeUrl(config);
    return get(url);
  }

  /*
   * Make a POST request.
   * See docs for `this.get` dor param description
   * 
   */ 
  post(config = {}) {
    const url = this.composeUrl(config);
    const json = config.json !== undefined ? config.json : this.config.json;
    const form = config.form !== undefined ? config.form : this.config.form;
    return post(url, config.data, form, json);
  }

  put(config = {}) {
    const url = this.composeUrl(config);
    const json = config.json !== undefined ? config.json : this.config.json;
    const form = config.form !== undefined ? config.form : this.config.form;
    return put(url, config.data, form, json);
  }

  del(config = {}) {
    const url = this.composeUrl(config);
    return del(url);
  }

  /***************************
   * Following methods are for
   * working with Redux
   ***************************/
  setReduxConstants(requestFunction) {
    // Generate constant names for redux actions.
    const formatted = this.endpoint.replace(/\//g, '_').replace(/({.*?})/g, '').toUpperCase();
    const nameForRedux = `${requestFunction.name.toUpperCase()}_${formatted}`;
    this.requestConst = `REQUEST_${nameForRedux}`;
    this.receiveConst = `RECEIVE_${nameForRedux}`;
    this.errorConst = `ERROR_${nameForRedux}`;
  }

  /*
  * Make a general, consistent redux action for the endpoint.
  * All returned data is dispatched in the `data` property.
  * Data can be filtered with the `actionFilter` function specified in the
  * `config` object passed to the class constructor
  */
  action(config, method) {
    this.setReduxConstants(method);
    return (dispatch) => {
      dispatch({ type: this.requestConst, config });
      return method(config)
        .then(data => dispatch({ type: this.receiveConst, data: this.config.actionFilter(data) }))
        .catch(data => dispatch({ type: this.errorConst, data }));
    };
  }

  /*
  * Creates a redux reducer for the api endpoint based on the initial state
  * configured in the class constructor.
  * This function should not be called directly; instead access the
  * `reducer` instance property.
  * Initial state can be provided by passing a `config`
  * object to the class constructor with an `initialState` property.
  * The initialState *must* use immutableJS. The reducer will
  * explicitly set the following properties in the state:
  * `loading`: bool
  * `error`: bool
  * `errorData`: object
  * `data`: object
  * Therefore it is reccomended to supply custom state using the `genericState`
  * object:
  *
  * const myInitialState = { ...genericState, data: { *initial state here* } };
  */
  makeReducer(initialState) {
    // we wrap the reducer function so initialState can be
    // set from a class property (this.config.initialState).
    // The actual reducer function is instantiated in the constructor
    return (state = initialState, action) => {
      switch (action.type) {
        case this.requestConst:
          return state.merge({
            loading: true,
            config: action.config
          });
        case this.receiveConst:
          return state.merge({
            loading: false,
            data: fromJS(action.data)
          });
        case this.errorConst:
          return state.merge({
            loading: false,
            error: true,
            errorData: fromJS(action.data)
          });
        default:
          return state;
      }
    };
  }
}

// Get a single order  
export const orderDetail = new ApiEndpoint('order/{id}/');
// Mark an order as fulfilled
export const fulfillOrder = new ApiEndpoint('order/{id}/fulfill/');
// Create an order
export const checkout = new ApiEndpoint('checkout/');
// Get a payment gateway token
export const checkoutToken = new ApiEndpoint('checkout/token/');
// Get all items in basket/post an item to the basket/delete item from basket
export const basketList = new ApiEndpoint('basket/');
// get number of items in basket
export const basketListCount = new ApiEndpoint('basket/count/');
// get number of single item in basket
export const basketDetailCount = new ApiEndpoint('basket/{id}/count/');
// delete an item in the basket
export const basketDetail = new ApiEndpoint('basket/{id}/');
// Get the shipping cost for a country (include country_code in query params and optionally shipping_rate_name)
export const shippingCost = new ApiEndpoint('shipping/cost/');
// Get a list of valid shipping countries
export const shippingCountries = new ApiEndpoint('shipping/countries/');
// Get list of addresses/post a new address
export const addressList = new ApiEndpoint('addresses/');
// get/update/delete address
export const addressDetail = new ApiEndpoint('addresses/{id}/');


export default {
  orderDetail, fulfillOrder, checkout, 
  checkoutToken, basketList, basketListCount,
  basketDetailCount, basketDetail, shippingCost,
  shippingCountries, addressList, addressDetail
}
