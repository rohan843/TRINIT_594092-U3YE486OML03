const express = require('express');
const parser = require('body-parser');
const axios = require('axios');

const app = express();
app.set('view engine', 'ejs');
app.use(parser.urlencoded({ extended: true }));
app.use("*/css", express.static("public/css"));
app.use("*/img", express.static("public/img"));
app.use("*/js", express.static("public/js"));

// ---- Utility Functions ----
const baseURL = '';

async function apiCall(url, params) {
    let res = await axios.get(url, {
        params: params
    });
    return res.data;
}

async function get_crop_suggestion(N, P, K, pH, state) {
    let res = await apiCall(baseURL + '/crop_suggestion', {
        N: N,
        P: P,
        K: K,
        pH: pH,
        state: state
    });
    return res['best_crop'];
}

async function get_soil_suggestion(crop, state) {
    let res = await apiCall(baseURL + '/soil_suggestion', {
        crop: crop,
        state: state
    });
    return {
        'N': res['N'],
        'P': res['P'],
        'K': res['K'],
        'pH': res['pH']
    };
}

async function get_rainfall_timeseries_data(month, state) {
    let res = await apiCall(baseURL + '/rainfall_timeseries_data', {
        month: month,
        state: state
    });
    return res['timeseries_data'];
}

async function crop_price_by_state_data(state) {
    let res = await apiCall(baseURL + '/crop_price_by_state_data', {
        state: state
    });
    return res['price_data'];
}

// ---- Endpoints ----
app.get('/', (req, res) => {
    res.sendFile(__dirname + "/index.html");
});

app.listen(3000, () => {
    console.log("Server set up to listen on port 3000.");
});