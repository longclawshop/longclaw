webpackJsonp([0],[
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

	module.exports = __webpack_require__(1);


/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(global) {"use strict";
	
	module.exports = global["longclawclient"] = __webpack_require__(2);
	/* WEBPACK VAR INJECTION */}.call(exports, (function() { return this; }())))

/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	exports.requestVariantList = exports.requestsList = exports.addressDetail = exports.addressList = exports.shippingCountryOptions = exports.shippingCountries = exports.shippingCost = exports.basketDetail = exports.basketDetailCount = exports.basketListCount = exports.basketList = exports.checkoutToken = exports.checkout = exports.refundOrder = exports.fulfillOrder = exports.orderDetail = undefined;
	
	var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };
	
	var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }(); /**
	                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      * Client endpoints for interacting with the longclaw API
	                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      */
	
	
	var _immutable = __webpack_require__(3);
	
	var _helpers = __webpack_require__(4);
	
	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }
	
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
	var ApiEndpoint = function () {
	
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
	  function ApiEndpoint(endpoint) {
	    var config = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
	
	    _classCallCheck(this, ApiEndpoint);
	
	    // Default configuration
	    this.config = _extends({
	      form: false, // true if the endpoint expects form data
	      json: false, // true if the endpoint returns json
	      prefix: '',
	      actionFilter: function actionFilter(data) {
	        return data;
	      },
	      initialState: (0, _immutable.fromJS)(_helpers.genericState)
	    }, config);
	    this.endpoint = endpoint;
	
	    // Bind methods so they can be passed around
	    this.get = this.get.bind(this);
	    this.post = this.post.bind(this);
	    this.del = this.del.bind(this);
	    this.put = this.put.bind(this);
	    this.action = this.action.bind(this);
	    this.reducer = this.makeReducer(this.config.initialState);
	  }
	
	  _createClass(ApiEndpoint, [{
	    key: 'composeUrl',
	    value: function composeUrl() {
	      var config = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	
	      // Url can be overridden in the config
	      var url = config.url || '' + this.config.prefix + this.endpoint;
	      if (config.prefix) {
	        url = '' + config.prefix + url;
	      }
	      if (config.urlParams) {
	        Object.keys(config.urlParams).map(function (key) {
	          url = url.replace('{' + key + '}', config.urlParams[key]);
	        });
	      }
	      if (config.queryParams) {
	        url = url + '?' + (0, _helpers.composeParams)(config.queryParams);
	      }
	      return url;
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
	
	  }, {
	    key: 'get',
	    value: function get() {
	      var config = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	
	      var url = this.composeUrl(config);
	      return (0, _helpers.get)(url);
	    }
	
	    /*
	     * Make a POST request.
	     * See docs for `this.get` dor param description
	     *
	     */
	
	  }, {
	    key: 'post',
	    value: function post() {
	      var config = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	
	      var url = this.composeUrl(config);
	      var json = config.json !== undefined ? config.json : this.config.json;
	      var form = config.form !== undefined ? config.form : this.config.form;
	      return (0, _helpers.post)(url, config.data, form, json);
	    }
	  }, {
	    key: 'put',
	    value: function put() {
	      var config = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	
	      var url = this.composeUrl(config);
	      var json = config.json !== undefined ? config.json : this.config.json;
	      var form = config.form !== undefined ? config.form : this.config.form;
	      return (0, _helpers.put)(url, config.data, form, json);
	    }
	  }, {
	    key: 'del',
	    value: function del() {
	      var config = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	
	      var url = this.composeUrl(config);
	      return (0, _helpers.del)(url);
	    }
	
	    /***************************
	     * Following methods are for
	     * working with Redux
	     ***************************/
	
	  }, {
	    key: 'setReduxConstants',
	    value: function setReduxConstants(requestFunction) {
	      // Generate constant names for redux actions.
	      var formatted = this.endpoint.replace(/\//g, '_').replace(/({.*?})/g, '').toUpperCase();
	      var nameForRedux = requestFunction.name.toUpperCase() + '_' + formatted;
	      this.requestConst = 'REQUEST_' + nameForRedux;
	      this.receiveConst = 'RECEIVE_' + nameForRedux;
	      this.errorConst = 'ERROR_' + nameForRedux;
	    }
	
	    /*
	    * Make a general, consistent redux action for the endpoint.
	    * All returned data is dispatched in the `data` property.
	    * Data can be filtered with the `actionFilter` function specified in the
	    * `config` object passed to the class constructor
	    */
	
	  }, {
	    key: 'action',
	    value: function action(config, method) {
	      var _this = this;
	
	      this.setReduxConstants(method);
	      return function (dispatch) {
	        dispatch({ type: _this.requestConst, config: config });
	        return method(config).then(function (data) {
	          return dispatch({ type: _this.receiveConst, data: _this.config.actionFilter(data) });
	        }).catch(function (data) {
	          return dispatch({ type: _this.errorConst, data: data });
	        });
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
	
	  }, {
	    key: 'makeReducer',
	    value: function makeReducer(initialState) {
	      var _this2 = this;
	
	      // we wrap the reducer function so initialState can be
	      // set from a class property (this.config.initialState).
	      // The actual reducer function is instantiated in the constructor
	      return function () {
	        var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : initialState;
	        var action = arguments[1];
	
	        switch (action.type) {
	          case _this2.requestConst:
	            return state.merge({
	              loading: true,
	              config: action.config
	            });
	          case _this2.receiveConst:
	            return state.merge({
	              loading: false,
	              data: (0, _immutable.fromJS)(action.data)
	            });
	          case _this2.errorConst:
	            return state.merge({
	              loading: false,
	              error: true,
	              errorData: (0, _immutable.fromJS)(action.data)
	            });
	          default:
	            return state;
	        }
	      };
	    }
	  }]);
	
	  return ApiEndpoint;
	}();
	
	// Get a single order
	
	
	var orderDetail = exports.orderDetail = new ApiEndpoint('order/{id}/');
	// Mark an order as fulfilled
	var fulfillOrder = exports.fulfillOrder = new ApiEndpoint('order/{id}/fulfill/');
	// Refund an order
	var refundOrder = exports.refundOrder = new ApiEndpoint('order/{id}/refund/');
	// Create an order
	var checkout = exports.checkout = new ApiEndpoint('checkout/');
	// Get a payment gateway token
	var checkoutToken = exports.checkoutToken = new ApiEndpoint('checkout/token/');
	// Get all items in basket/post an item to the basket/delete item from basket
	var basketList = exports.basketList = new ApiEndpoint('basket/');
	// get number of items in basket
	var basketListCount = exports.basketListCount = new ApiEndpoint('basket/count/');
	// get number of single item in basket
	var basketDetailCount = exports.basketDetailCount = new ApiEndpoint('basket/{id}/count/');
	// delete an item in the basket
	var basketDetail = exports.basketDetail = new ApiEndpoint('basket/{id}/');
	// Get the shipping cost for a country (include country_code in query params and optionally shipping_rate_name)
	var shippingCost = exports.shippingCost = new ApiEndpoint('shipping/cost/');
	// Get a list of valid shipping countries
	var shippingCountries = exports.shippingCountries = new ApiEndpoint('shipping/countries/');
	// Get a list of shipping options for a country
	var shippingCountryOptions = exports.shippingCountryOptions = new ApiEndpoint('shipping/countries/{country}/');
	// Get list of addresses/post a new address
	var addressList = exports.addressList = new ApiEndpoint('addresses/');
	// get/update/delete address
	var addressDetail = exports.addressDetail = new ApiEndpoint('addresses/{id}/');
	//List/Post new product request
	var requestsList = exports.requestsList = new ApiEndpoint('requests/');
	//List product requests for a single variant
	var requestVariantList = exports.requestVariantList = new ApiEndpoint('requests/variant/{id}/');
	
	exports.default = {
	  orderDetail: orderDetail, fulfillOrder: fulfillOrder, refundOrder: refundOrder, checkout: checkout,
	  checkoutToken: checkoutToken, basketList: basketList, basketListCount: basketListCount,
	  basketDetailCount: basketDetailCount, basketDetail: basketDetail, shippingCost: shippingCost,
	  shippingCountries: shippingCountries, shippingCountryOptions: shippingCountryOptions,
	  addressList: addressList, addressDetail: addressDetail, requestsList: requestsList, requestVariantList: requestVariantList
	};

/***/ }),
/* 3 */,
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	exports.del = exports.put = exports.post = exports.get = exports.genericState = exports.getRequestHeaders = exports.parseJSON = exports.checkStatus = exports.composeParams = undefined;
	
	var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };
	
	var _jsCookie = __webpack_require__(5);
	
	var _jsCookie2 = _interopRequireDefault(_jsCookie);
	
	var _isomorphicFetch = __webpack_require__(6);
	
	var _isomorphicFetch2 = _interopRequireDefault(_isomorphicFetch);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * Convert an object of query parameters into a url query string.
	 * e.g.
	 * {
	 *    param1: 10,
	 *    param2: 20
	 * }
	 *
	 * becomes
	 *
	 * 'param1=10&param2=20&'
	 *
	 */
	function composeParams(params) {
	  return Object.keys(params).map(function (key) {
	    if (params[key]) return [key, params[key]].map(encodeURIComponent).join('=');
	  }).join('&');
	}
	
	/**
	 * Check the response status and raise an error if it's no good.
	 * @param {object} response - the http response object as provided by fetch
	 * @returns {object} - the http rsponse object or throws an error
	 */
	function checkStatus(response) {
	  if (response.ok) {
	    return response;
	  }
	  return response.json().then(function (json) {
	    var error = new Error(response.statusText);
	    throw Object.assign(error, { response: response, json: json });
	  });
	}
	
	/**
	 * Return an object given an http json response
	 * @param {object} response - json encoded response object as provided by fetch
	 * @returns {object} - The parsed json
	 */
	function parseJSON(response) {
	  return response.json();
	}
	
	/**
	 * Return the headers needed for put, post and delete requests
	 * @returns {{Accept: string, Content-Type: string, X-CSRFToken: *}}
	 */
	function getRequestHeaders() {
	  var form = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : false;
	
	  var contentType = 'application/json';
	  var headers = {
	    Accept: 'application/json, application/json, application/coreapi+json'
	  };
	  if (!form) headers['Content-Type'] = contentType;
	  var csrf = _jsCookie2.default.get('csrftoken');
	  if (csrf) headers['X-CSRFToken'] = csrf;
	  return headers;
	}
	
	function get(url) {
	  return (0, _isomorphicFetch2.default)(url, {
	    method: 'GET',
	    headers: getRequestHeaders(),
	    credentials: 'include'
	  }).then(checkStatus).then(parseJSON);
	}
	
	function post(url, data) {
	  var isForm = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
	  var json = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
	
	  var response = (0, _isomorphicFetch2.default)(url, {
	    method: 'POST',
	    headers: getRequestHeaders(isForm),
	    credentials: 'include',
	    body: isForm ? data : JSON.stringify(data)
	  }).then(checkStatus);
	
	  if (json) {
	    return response.then(parseJSON);
	  }
	  return response;
	}
	
	function put(url, data) {
	  var isForm = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
	  var json = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
	
	  var response = (0, _isomorphicFetch2.default)(url, {
	    method: 'PUT',
	    headers: getRequestHeaders(isForm),
	    credentials: 'include',
	    body: isForm ? data : JSON.stringify(data)
	  }).then(checkStatus);
	
	  return json ? response.then(parseJSON) : response;
	}
	
	function del(url, data) {
	  return (0, _isomorphicFetch2.default)(url, {
	    method: 'DELETE',
	    headers: getRequestHeaders(false),
	    credentials: 'include',
	    body: JSON.stringify(_extends({ quantity: 1 }, data))
	  }).then(checkStatus);
	}
	
	var genericState = {
	  loading: true,
	  error: false,
	  errorData: {},
	  data: {},
	  config: {}
	};
	
	exports.composeParams = composeParams;
	exports.checkStatus = checkStatus;
	exports.parseJSON = parseJSON;
	exports.getRequestHeaders = getRequestHeaders;
	exports.genericState = genericState;
	exports.get = get;
	exports.post = post;
	exports.put = put;
	exports.del = del;

/***/ }),
/* 5 */
/***/ (function(module, exports, __webpack_require__) {

	var __WEBPACK_AMD_DEFINE_FACTORY__, __WEBPACK_AMD_DEFINE_RESULT__;/*!
	 * JavaScript Cookie v2.2.1
	 * https://github.com/js-cookie/js-cookie
	 *
	 * Copyright 2006, 2015 Klaus Hartl & Fagner Brack
	 * Released under the MIT license
	 */
	;(function (factory) {
		var registeredInModuleLoader;
		if (true) {
			!(__WEBPACK_AMD_DEFINE_FACTORY__ = (factory), __WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ? (__WEBPACK_AMD_DEFINE_FACTORY__.call(exports, __webpack_require__, exports, module)) : __WEBPACK_AMD_DEFINE_FACTORY__), __WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
			registeredInModuleLoader = true;
		}
		if (true) {
			module.exports = factory();
			registeredInModuleLoader = true;
		}
		if (!registeredInModuleLoader) {
			var OldCookies = window.Cookies;
			var api = window.Cookies = factory();
			api.noConflict = function () {
				window.Cookies = OldCookies;
				return api;
			};
		}
	}(function () {
		function extend () {
			var i = 0;
			var result = {};
			for (; i < arguments.length; i++) {
				var attributes = arguments[ i ];
				for (var key in attributes) {
					result[key] = attributes[key];
				}
			}
			return result;
		}
	
		function decode (s) {
			return s.replace(/(%[0-9A-Z]{2})+/g, decodeURIComponent);
		}
	
		function init (converter) {
			function api() {}
	
			function set (key, value, attributes) {
				if (typeof document === 'undefined') {
					return;
				}
	
				attributes = extend({
					path: '/'
				}, api.defaults, attributes);
	
				if (typeof attributes.expires === 'number') {
					attributes.expires = new Date(new Date() * 1 + attributes.expires * 864e+5);
				}
	
				// We're using "expires" because "max-age" is not supported by IE
				attributes.expires = attributes.expires ? attributes.expires.toUTCString() : '';
	
				try {
					var result = JSON.stringify(value);
					if (/^[\{\[]/.test(result)) {
						value = result;
					}
				} catch (e) {}
	
				value = converter.write ?
					converter.write(value, key) :
					encodeURIComponent(String(value))
						.replace(/%(23|24|26|2B|3A|3C|3E|3D|2F|3F|40|5B|5D|5E|60|7B|7D|7C)/g, decodeURIComponent);
	
				key = encodeURIComponent(String(key))
					.replace(/%(23|24|26|2B|5E|60|7C)/g, decodeURIComponent)
					.replace(/[\(\)]/g, escape);
	
				var stringifiedAttributes = '';
				for (var attributeName in attributes) {
					if (!attributes[attributeName]) {
						continue;
					}
					stringifiedAttributes += '; ' + attributeName;
					if (attributes[attributeName] === true) {
						continue;
					}
	
					// Considers RFC 6265 section 5.2:
					// ...
					// 3.  If the remaining unparsed-attributes contains a %x3B (";")
					//     character:
					// Consume the characters of the unparsed-attributes up to,
					// not including, the first %x3B (";") character.
					// ...
					stringifiedAttributes += '=' + attributes[attributeName].split(';')[0];
				}
	
				return (document.cookie = key + '=' + value + stringifiedAttributes);
			}
	
			function get (key, json) {
				if (typeof document === 'undefined') {
					return;
				}
	
				var jar = {};
				// To prevent the for loop in the first place assign an empty array
				// in case there are no cookies at all.
				var cookies = document.cookie ? document.cookie.split('; ') : [];
				var i = 0;
	
				for (; i < cookies.length; i++) {
					var parts = cookies[i].split('=');
					var cookie = parts.slice(1).join('=');
	
					if (!json && cookie.charAt(0) === '"') {
						cookie = cookie.slice(1, -1);
					}
	
					try {
						var name = decode(parts[0]);
						cookie = (converter.read || converter)(cookie, name) ||
							decode(cookie);
	
						if (json) {
							try {
								cookie = JSON.parse(cookie);
							} catch (e) {}
						}
	
						jar[name] = cookie;
	
						if (key === name) {
							break;
						}
					} catch (e) {}
				}
	
				return key ? jar[key] : jar;
			}
	
			api.set = set;
			api.get = function (key) {
				return get(key, false /* read as raw */);
			};
			api.getJSON = function (key) {
				return get(key, true /* read as json */);
			};
			api.remove = function (key, attributes) {
				set(key, '', extend(attributes, {
					expires: -1
				}));
			};
	
			api.defaults = {};
	
			api.withConverter = init;
	
			return api;
		}
	
		return init(function () {});
	}));


/***/ })
]);
//# sourceMappingURL=http://127.0.0.1:3001/dist/js/bundle.js.map