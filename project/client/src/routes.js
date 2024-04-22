login = require('./authorization/login.js');
register = require('./authorization/register.js');
home = require('./dashboard/home_page.js');

exports.initializeRoutes = (app) => {
    app.get('/login', login.login);
    app.post('/submit-login-form', login.submitLoginForm);

    app.get('/register', register.register);
    app.post('/submit-register-form', register.submitRegisterForm);

    app.get('/home', home.homePage);
}
