//base url for the api

const BASE_URL = "http://127.0.0.1:5000";

//shared api function

async function sharedApi(endpoint, method, body) {
    const response = await fetch(BASE_URL + endpoint, {
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });

    const result = await response.json();
    return result;


}

export default sharedApi;


