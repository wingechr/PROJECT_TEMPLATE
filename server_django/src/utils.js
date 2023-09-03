/**
 *
 * @param {*} name
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
 * @returns {function}
 */
function getApiClient() {
  let auth = new coreapi.auth.SessionAuthentication({
    csrfCookieName: 'csrftoken',
    csrfHeaderName: 'X-CSRFToken',
  });
  return new coreapi.Client({auth: auth});
};

module.exports = {getApiClient, getCsrftoken, getCookie};
