const axios = require('axios');

exports.homePage = async (req, res) => {
    const user_id = req.session.user_id;

    if (user_id === undefined) {
        res.redirect('/login');
        return;
    }

    try {
        const responseOrg = await axios.get('http://error_handler_api:8080/users_organization', {
            params: {
                user_id
            }
        });

        let available_organizations = responseOrg.data || [];
        
        if (available_organizations.length === 0) {
            res.render('home.ejs', {
                available_organizations: [],
                available_apps: []
            });
            return;
        }
        
        if (available_organizations.length > 5) {
            available_organizations = available_organizations.slice(0, 5);
        }

        const appRequests = available_organizations.map(org => {
            return axios.get('http://error_handler_api:8080/apps', {
                params: {
                    organization_id: org.id,
                    user_id
                }
            });
        });

        const responsesApps = await Promise.all(appRequests);

        const available_apps = responsesApps.map(response => response.data);

        console.log("available apps: ", available_apps);
        console.log("available orgs: ", available_organizations);

        res.render('home.ejs', {
            available_organizations,
            available_apps
        });
    } catch (error) {
        console.log(error);
        res.status(500).send('Internal Server Error');
    }
};
