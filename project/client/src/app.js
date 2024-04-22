const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const path = require('path');
const session = require('express-session');

const routes = require('./routes');

const app = express();
const PORT = process.env.PORT || 3000;

app.set('view engine', 'ejs');
app.set('views', './public/pages');
app.use(express.static(path.join(__dirname, '../public')));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use(session({
    secret: 'frsdscfscscsdcsd',
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }
}));

routes.initializeRoutes(app);

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
}
);

//module.exports = app;


