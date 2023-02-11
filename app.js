/*
cd "Path to repo"
mkdir "name of repo"
cd "name of repo"
mkdir views
mkdir public
mkdir public/css
mkdir public/js
mkdir public/img
touch index.html app.js .env
npm init
npm i express body-parser ejs mongoose       # basic packages
npm i mongoose-encryption       # used for encryption
npm i dotenv         # used for the .env file (process.env.SECRET)
npm i [md5 | bcrypt]     # used for hashing, bcrypt is safer and has salt rounds
npm i passport passport-local passport-local-mongoose express-session     # used for cookies, sessions, and OAuth
*/

require('dotenv').config();
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