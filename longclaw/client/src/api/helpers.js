import JsCookie from 'js-cookie';
import fetch from 'isomorphic-fetch';

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

const genericState = {
  loading: true,
  error: false,
  errorData: {},
  data: {},
  config: {}
};

export {
  composeParams,
  checkStatus,
  parseJSON,
  getRequestHeaders,
  genericState,
  get,
  post,
  put,
  del
}