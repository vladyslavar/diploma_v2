const axios = require('axios');

exports.monitorAppPage = async (req, res) => {
    const user_id = req.session.user_id;

    if (user_id === undefined) {
        res.redirect('/login');
        return;
    }

    const app_id = req.params.app_id;

    try {
        const app_response = await axios.get('http://error_handler_api:8080/app', {
            params: {
                app_id
            }
        });
        const app = app_response.data || {};

        const app_in_organization = app.organization_id;
        const organization_response = await axios.get('http://error_handler_api:8080/organization', {
            params: {
                organization_id: app_in_organization
            }
        });
        const organization = organization_response.data || {};

        if (organization.owner_id !== user_id) {
            res.redirect('/login');
            return;
        }

        const responseEvents = await axios.get('http://error_handler_api:8080/events', {
            params: {
                app_id
            }
        });
        const events = responseEvents.data || [];

        let all_params = [];
        const responseParams = await axios.get('http://error_handler_api:8080/app_all_parameters', {
            params: {
                app_id
            }
        });
        all_params = responseParams.data || [];

        const paramCounts = all_params.reduce((acc, item) => {
            const found = acc.find(element => element.parameter_name === item.parameter_name && element.parameter_value === item.parameter_value);
            if (found) {
                found.count += 1;
            } else {
                acc.push({ parameter_name: item.parameter_name, parameter_value: item.parameter_value, count: 1 });
            }
            return acc;
        }, []);

        paramCounts.sort((a, b) => b.count - a.count);
        console.log(paramCounts);

        res.render('monitor_app.ejs', {
            app,
            organization,
            events,
            paramCounts
        });

    } catch (error) {
        console.log(error);
        res.status(500).send('Internal Server Error');
    }
}