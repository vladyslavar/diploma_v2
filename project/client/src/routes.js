login = require('./authorization/login.js');
register = require('./authorization/register.js');
home = require('./dashboard/home_page.js');
organization_configure = require('./configure/general_organization_configure.js');
app_configure = require('./configure/general_apps_configure.js');
single_organization_configure = require('./configure/single_organization_configure.js');
single_app_configure = require('./configure/single_app_configure.js');
user_profile = require('./user_profile/user_profile.js');

exports.initializeRoutes = (app) => {
    app.get('/login', login.login);
    app.post('/submit-login-form', login.submitLoginForm);

    app.get('/register', register.register);
    app.post('/submit-register-form', register.submitRegisterForm);

    app.get('/home', home.homePage);

    app.get('/all_organizations', organization_configure.availableOrganizations);
    app.post('/create_organization', organization_configure.createOrganizationPage);
    app.post('/create_organization_form', organization_configure.createOrganizationForm);
    app.post('/delete_organization', organization_configure.deleteOrganization);

    app.get('/configure/organization/:organization_id', single_organization_configure.getOrganization);

    app.get('/configure/apps', app_configure.availableApps);
    app.post('/create_app', app_configure.createApp);
    app.post('/create_app_form', app_configure.createAppForm);
    app.post('/delete_app', app_configure.deleteApp);

    app.get('/configure/app/:appId', single_app_configure.getApp);

    app.get('/user_profile', user_profile.getUserProfile);
    app.post('/update_user_password', user_profile.updateProfilePassword);
    app.post('/delete_user_profile', user_profile.deleteProfile);
    app.get('/logout', user_profile.logout);
}
