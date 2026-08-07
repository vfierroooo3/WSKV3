//base url for the api

const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

//shared api function
async function sharedApi(endpoint, method, body = null) {
    const options = {
        method: method,
        headers: {
            "Content-Type": "application/json"
        }
    };

    if (method !== "GET" && body !== null) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(BASE_URL + endpoint, options);

    const result = await response.json();
    return result;
}

export default sharedApi;


