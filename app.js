const express = require('express');
const parser = require('body-parser');

const app = express();
app.set('view engine', 'ejs');
app.use(parser.urlencoded({ extended: true }));
app.use("*/css", express.static("public/css"));
app.use("*/img", express.static("public/img"));
app.use("*/js", express.static("public/js"));

app.get('/', (req, res) => {
    res.sendFile(__dirname + "/index.html");
});

app.listen(3000, () => {
    console.log("Server set up to listen on port 3000.");
});