const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');

const app = require('../app');

exports.register = (req, res) => {
    
    const { message } = req.query;
    console.log('message: ' + message);
    res.render('register.ejs', {
        message
    });
};

exports.submitRegisterForm = async (req, res) => {
    const { username, password, repeat_password } = req.body;
    console.log(req.body);
    
    if (password !== repeat_password) {
        res.redirect('/register?message=Passwords do not match');
        return;
    }

    await axios.get('http://error_handler_api:8080/registration', {
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