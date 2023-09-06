/**
 *
 * @param {string} name
 * @returns {string}
 */
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

/**
 *
 * @returns {string}
 */
function getCsrftoken() {
  return getCookie('csrftoken');
};

/**
 *
 * @param {*} url
 * @param {*} data
 * @param {*} method
 * @returns {object}
 */
function api(url, data, method) {
  let token = getCsrftoken();

  if (!data) {
    data = JSON.stringify(data);
    method = method || "POST";
  } else {
    method = method || "GET";
  }

  return fetch(url, {
    method: method,
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': token,
    },
    body: data,
  })
      .then((response) => {
        if (!response.ok) {
          throw new Error("HTTP error, status = " + response.status);
        } else if (response.headers.get("Content-Type") == "application/json") {
          return response.json();
        }
        return Promise.resolve();
      });
}

/**
 * get and update settings from and to url parameters
 * @param {*} defaults
 * @param {*} onchange
 * @returns {null}
 */
function querySettings(defaults, onchange) {
  let state = {};

  /**
   * update the current state (including the url)
   * @param {*} data
   */
  function update(data) {
    console.log("new data", data);

    // update state with new data
    Object.keys(data).map((k)=>{
      state[k] = data[k];
    });

    console.log("state", state);

    // Build the new query string
    let data2 = {};
    Object.keys(state).map((k)=>{
      data2[k] = JSON.stringify(state[k]);
    });

    const queryString = new URLSearchParams(data2).toString();
    console.log("queryString", queryString);

    // Get the current URL without the query string
    const baseUrl = window.location.href.split('?')[0];
    const newUrl = baseUrl + "?" + queryString;

    history.pushState({}, '', newUrl);

    // callback
    onchange(state);
  }

  /* set initial state from url */

  /**
   *
   */
  function init() {
    // Get the current URL
    const url = new URL(window.location.href);

    let data = {};
    // get and parse values from url, or use defaults
    Object.keys(defaults).map((k)=>{
      let v = url.searchParams.get(k);
      if (v == undefined) {
        // use deafultt
        v = defaults[k];
      } else {
        try {
          v = JSON.parse(v);
        } catch (error) {
          /* leave as string */
        }
      }
      data[k] = v;
    });

    // update state
    update(data);
  }

  init();

  return {
    update: update,
  };
};

module.exports = {api, getCsrftoken, getCookie, querySettings};
