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

        for (let i = 0; i < available_organizations.length; i++) {
            const org = available_organizations[i];
            const response = await axios.get('http://error_handler_api:8080/organization', {
                params: {
                    organization_id: org.organization_id
                }
            });
            org.name = response.data;
            available_organizations[i] = org;
        }

        let available_apps = [];
        const events_num = 5;
        for (let i = 0; i < available_organizations.length; i++) {
            const org = available_organizations[i];
            const responseApps = await axios.get('http://error_handler_api:8080/apps', {
                params: {
                    organization_id: org.organization_id,
                    user_id
                }
            });
            const apps = responseApps.data || [];

            for (let j = 0; j < apps.length; j++) {
                const app = apps[j];
                const responseEvents = await axios.get('http://error_handler_api:8080/last_events', {
                    params: {
                        app_id: app.id,
                        n: events_num
                    }
                });
                const events = responseEvents.data || [];
                app.events = events;
                apps[j] = app;
            }
            available_apps.push(apps);
        }

        
        res.render('home.ejs', {
            available_organizations,
            available_apps
        });
    } catch (error) {
        console.log(error);
        res.status(500).send('Internal Server Error');
    }
};
