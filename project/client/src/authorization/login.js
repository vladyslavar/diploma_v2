const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const routes = require('../routes');


exports.login = (req, res) => {
    res.render('login.ejs');
};

exports.submitLoginForm = async (req, res) => {
    const { username, password } = req.body;
    console.log(req.body);
    console.log(username + ' ' + password);
    await axios.get('http://error_handler_api:8080/login', {
        params: {
            username,
            password
        }
    })
    .then((response) => {
        user_id = response.data.user_account.id;
        req.session.user_id = user_id;
        res.redirect('/home');
    })
    .catch((error) => {
        console.log(error);
    });
};
