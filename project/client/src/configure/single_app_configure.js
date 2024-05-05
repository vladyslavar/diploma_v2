const axios = require('axios');
const uuid = require('uuid');

exports.getApp = async (req, res) => { 

    console.log("getApp");
    console.log(req.session.user_id);

    const user_id = req.session.user_id;
    if (user_id === undefined) {
        res.redirect('/login');
        return;
    }
    const app_id = req.params.app_id;

    console.log(app_id);

    const app_response = await axios.get('http://error_handler_api:8080/app', {
        params: {
            app_id
        }
    });
    const app = app_response.data || {};

    console.log(app);

    const app_in_organization = app.organization_id;
    const organization_response = await axios.get('http://error_handler_api:8080/organization', {
        params: {
            organization_id: app_in_organization
        }
    });
    const organization = organization_response.data || {};

    console.log(organization);

    if (organization.owner_id === user_id) {
        res.render('single_app_configure.ejs', {
            app,
            organization
        });
    }
    else{
        res.redirect('/login');
        return;
    }

};

exports.updateAppName = async (req, res) => {
    const user_id = req.session.user_id;
    if (user_id === undefined) {
        res.redirect('/login');
        return;
    }
    const {app_id, new_name} = req.body;

    await axios.post('http://error_handler_api:8080/update_app_name', {
        app_id,
        new_name,
        user_id
    })
    .then((response) => {
        res.redirect('/configure/app/' + app_id);
    })
    .catch((error) => {
        console.log(error);
    });
}

exports.updateAppKey = async (req, res) => {
    const user_id = req.session.user_id;
    if (user_id === undefined) {
        res.redirect('/login');
        return;
    }
    const {app_id} = req.body;
    new_api_key = uuid.v4();

    await axios.post('http://error_handler_api:8080/update_app_key', {
        app_id,
        new_api_key,
        user_id
    })
    .then((response) => {
        new_api_key = response.data;
        res.redirect('/configure/app/' + app_id + '?message=New API Key: ' + new_api_key);
    })
    .catch((error) => {
        console.log(error);
    });
}

exports.deleteApp = async (req, res) => {
    const user_id = req.session.user_id;
    if (user_id === undefined) {
        res.redirect('/login');
        return;
    }
    const {app_id} = req.body;

    await axios.post('http://error_handler_api:8080/delete_app', {
        app_id,
        user_id
    })
    .then((response) => {
        res.redirect('/configure/apps');
    })
    .catch((error) => {
        console.log(error);
    });
}