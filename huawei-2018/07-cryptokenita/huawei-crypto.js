var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var crypto = require('crypto');
var config = require('./config.js');

var app = express();

var session = require('express-session');
var fs = require('fs');
var _ = require('lodash');

var title = "Adivina el token !";

function tokenGen() {
    return crypto.randomBytes(8).toString();
}

var source = fs.readFileSync(__filename,{encoding:'utf-8'});

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use(session({
    secret: config.secret,
    resave: false,
    saveUninitialized: false,
    maxAge: 120,
    cookie: {}
}));

app.get('/', function (req, res, next) {
    if (!req.session.token) {
        req.session.token = tokenGen();
        req.session.save();
    }
    res.render('index', {title: title});
});

app.get('/source', function (req, res, next) {
    res.setHeader('Content-Type', 'text/javascript');
    res.send(source);
});
app.post('/guess', function (req, res, next) {
    var token = req.body.token;
    // No hack
    if(!_.isString(token) || !_.isBuffer(Buffer.from(token, 'base64')) || !_.isString(Buffer.from(token, 'base64').toString('utf8'))) {
        res.render('hacker', {title: title});
        return;
    }

    token = Buffer.from(token, 'base64').toString('utf8');
    if(req.session && req.session.token && req.session.token === token) {
        res.render('flag', {title: title, flag: config.flag});
        return;
    }

    res.render('no_flag', {title: title});
});

// No hack
app.use(function (req, res, next) {
    res.render('hacker',{title: title});
});

module.exports = app;