const express = require('express');
const parser = require('body-parser');
const axios = require('axios');

const app = express();
app.set('view engine', 'ejs');
app.use(parser.urlencoded({ extended: true }));
app.use("*/css", express.static("assets/css"));
app.use("*/img", express.static("assets/img"));
app.use("*/js", express.static("assets/js"));

// ---- Utility Functions ----
const baseURL = 'http://127.0.0.1:4002';

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
    return res['best_crops'];
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
    arr = res['timeseries_data'];
    while(arr.length > 12) {
        arr.pop();
    }
    return arr;
}

async function crop_price_by_state_data(state) {
    let res = await apiCall(baseURL + '/crop_price_by_state_data', {
        state: state
    });
    return res['price_data'];
}

function split(arr) {
    a1 = []
    a2 = []
    for (let i = 0; i < arr.length; i++) {
        elt = arr[i]
        a1.push(elt[0])
        a2.push(elt[1])
    }
    return [a1, a2];
}

async function get_everything(N, P, K, pH, state, crop) {
    let best_crops = await get_crop_suggestion(N, P, K, pH, state)
    best_crops.sort(function (x, y) {
        if (x[1] < y[1]) {
            return 1;
        }
        if (x[1] > y[1]) {
            return -1;
        }
        return 0;
    });
    let [cropNames, pValues] = split(best_crops)
    while (cropNames.length > 6) {
        cropNames.pop()
        pValues.pop()
    }
    let soilParams = await get_soil_suggestion(crop, state)
    let rain_data = {
        "JAN": await get_rainfall_timeseries_data(0, state),
        "FEB": await get_rainfall_timeseries_data(1, state),
        "MAR": await get_rainfall_timeseries_data(2, state),
        "APR": await get_rainfall_timeseries_data(3, state),
        "MAY": await get_rainfall_timeseries_data(4, state),
        "JUN": await get_rainfall_timeseries_data(5, state),
        "JUL": await get_rainfall_timeseries_data(6, state),
        "AUG": await get_rainfall_timeseries_data(7, state),
        "SEP": await get_rainfall_timeseries_data(8, state),
        "OCT": await get_rainfall_timeseries_data(9, state),
        "NOV": await get_rainfall_timeseries_data(10, state),
        "DEC": await get_rainfall_timeseries_data(11, state)
    }
    let crop_price = await crop_price_by_state_data(state)
    while (crop_price.length > 7) {
        crop_price.pop()
    }
    while (crop_price.length < 7) {
        crop_price.push(['', 0])
    }
    paramsDict = {
        "chartBig1": {
            "data": rain_data
        },
        "NPKData": [soilParams['N'], soilParams['P'], soilParams['K']],
        "pHData": soilParams['pH'],
        "Top6Crops": cropNames,
        "Top6CropsProbs": pValues,
        "bestCrop": cropNames[0],
        "years": [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021],
        "Top7BestsellingCrops": crop_price
    }
    return paramsDict;
}

// ---- Endpoints ----
app.get('/', (req, res) => {
    res.sendFile(__dirname + "/examples/dashboard.html");
});

app.get('/get_everything', async (req, res) => {
    let N = req.query.N;
    let P = req.query.P;
    let K = req.query.K;
    let pH = req.query.pH;
    let state = req.query.state;
    let crop = req.query.crop;
    // console.log(N, P, K, pH, month, state); 1 2 3 4 0 tamil nadu maize
    obj = await get_everything(N, P, K, pH, state, crop)
    console.log(obj);
    res.send(JSON.stringify(obj));
});

app.listen(3000, () => {
    console.log("Server set up to listen on port 3000.");
});