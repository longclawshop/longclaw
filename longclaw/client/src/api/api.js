/**
 * Client endpoints for interacting with the longclaw API
 */
import JsCookie from 'js-cookie';
import fetch from 'isomorphic-fetch';

export default {

  // Get a single order  
  getOrder: makeApiFunction('/api/order/{id}/', get),

  // Mark an order as fulfilled
  fulfillOrder: makeApiFunction('/api/order/{id}/fulfill/', post, false, false)

}

/*
 * Generate a function which can perform a get/post/put/del etc request
 * at the given endpoint.
 *
 * @param {string} endpoint - The URL endpoint for the request. e.g. /api/v1/my/endpoint/
 * @param {func} requestFunction - The request function to user. i.e. get, post, put or del
 * @param {bool} form - Whether the user input is form data
 * @param {bool} json - Whether there is a JSON response from post/put operations
 *  (all get operations are expected to be json)
 * @param {string} urlSuffix - Optional suffix to append *after* the callers urlSuffix has been
 *  appended. This allows endpoints such as /api/v1/requests/request/{id}/decline/ to be composed
 *  where /api/v1/requests/request/ is the endpoint, {id}/ is the user-supplied, dynamic suffix
 *  (when then generated function is called) and decline/ is the fixed suffix.
 *
 * The returned function can be called with the following parameters
 *
 * @param {string} host - Optional hostname, to be used if the API call is not from the same origin
 * @param {Object} options - Configuration for the request
 * @param {Object} options.urlParams - Optional params to format the endpoint url with.
 *  params in the url are replaced by the keys specified here, similar to a python format string
 * @param {Object} options.queryParams - Optional object of query parameters,
 *   which will be converted into a query string. Keys should be the name of the param and
 *   values the value.
 * @param {Object} options.data - Optional object containing data for the post/put request. Will be
 *  converted to JSON if appropriate (i.e. if form == false)
 *
 */
function makeApiFunction(endpoint, requestFunction, form = false, json = false) {
  return (options = {}) => {
    let url = endpoint;
    if (options.urlParams) {
      Object.keys(options.urlParams).map((key) => {
        url = url.replace(`{${key}}`, options.urlParams[key]);
      });
    }
    if (options.queryParams) {
      url = `${url}?${composeParams(options.queryParams)}`;
    }

    if (!options.data) {
      return requestFunction(url);
    }
    return requestFunction(url, options.data, form, json);
  };
}

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
  return Object.keys(params).map((key) => {
    if (params[key]) return [key, params[key]].map(encodeURIComponent).join('=');
  }
  ).join('&');
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
  return response.json().then(json => {
    const error = new Error(response.statusText)
    throw Object.assign(error, { response, json })
  })
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
function getRequestHeaders(form = false) {
  const contentType = 'application/json';
  const headers = {
    Accept: 'application/json, application/json, application/coreapi+json'
  };
  if (!form) headers['Content-Type'] = contentType;
  const csrf = JsCookie.get('csrftoken');
  if (csrf) headers['X-CSRFToken'] = csrf;
  return headers;
}

function get(url) {
  return fetch(
    url,
    {
      method: 'GET',
      headers: getRequestHeaders(),
      credentials: 'include'
    }
  )
    .then(checkStatus)
    .then(parseJSON);
}

function post(url, data, isForm = false, json = true) {
  const response = fetch(
    url,
    {
      method: 'POST',
      headers: getRequestHeaders(isForm),
      credentials: 'include',
      body: isForm ? data : JSON.stringify(data)
    }
  )
    .then(checkStatus);

  if (json) {
    return response.then(parseJSON);
  }
  return response;
}

function put(url, data, isForm = false, json = true) {
  const response = fetch(
    url,
    {
      method: 'PUT',
      headers: getRequestHeaders(isForm),
      credentials: 'include',
      body: isForm ? data : JSON.stringify(data)
    }
  )
    .then(checkStatus);

  return json ? response.then(parseJSON) : response;
}

function del(url) {
  return fetch(
    url,
    {
      method: 'DELETE',
      headers: getRequestHeaders(false),
      credentials: 'include'
    }
  )
    .then(checkStatus);
}
