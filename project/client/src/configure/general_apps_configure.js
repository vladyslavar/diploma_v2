const axios = require('axios');
const uuid = require('uuid');

exports.availableApps = async (req, res) => {
    const user_id = req.session.user_id;

    if (user_id === undefined) {
        res.redirect('/login');
        return;
    }

    try{
        const all_owned_organizations_responce = await axios.get('http://error_handler_api:8080/organization_owner', {
            params: {
                user_id
            }
        });

        let owned_organizations = all_owned_organizations_responce.data || [];

        let empty_orgs = [];
        for (let i = 0; i < owned_organizations.length; i++) {
            let current_organization = owned_organizations[i];
            const apps = await axios.get('http://error_handler_api:8080/apps', {
                params: {
                    organization_id: current_organization.id,
                    user_id
                }
            });
            owned_organizations[i].apps = apps.data;
        }

        owned_organizations_with_apps = owned_organizations.filter(org => org.apps.length > 0);

        res.render('general_apps_configure.ejs', {
            owned_organizations,
            owned_organizations_with_apps
        });

    }
    catch (error) {
        console.log(error);
        res.status(500).send('Internal Server Error');
    }
}


exports.createApp = async (req, res) => {
    const user_id = req.session.user_id;

    if (user_id === undefined) {
        res.redirect('/login');
        return;
    }

    let {organizations} = req.body;

    organizations = JSON.parse(organizations);

    res.render('create_app.ejs', {
        organizations
    });
}

exports.createAppForm = async (req, res) => {
    const user_id = req.session.user_id;

    if (user_id === undefined) {
        res.redirect('/login');
        return;
    }

    const { organization_id, app_name } = req.body;

    console.log("data from form to create app")
    console.log(organization_id + ' ' + app_name);

    api_key = uuid.v4();

    try{
        await axios.post('http://error_handler_api:8080/register_app', {
            organization_id,
            user_id,
            app_name,
            api_key
        });

        res.redirect('/configure/apps');
    }
    catch (error) {
        console.log(error);
        res.status(500).send('Internal Server Error');
    }
}


exports.deleteApp = async (req, res) => {
    const user_id = req.session.user_id;

    if (user_id === undefined) {
        res.redirect('/login');
        return;
    }

    const { organization_id, app_id } = req.body;

    try{
        await axios.post('http://error_handler_api:8080/delete_app', {
            app_id,
            user_id,
            organization_id
        });

        res.redirect('/configure/apps');
    }
    catch (error) {
        console.log(error);
        res.status(500).send('Internal Server Error');
    }
}