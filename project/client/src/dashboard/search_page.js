const axios = require('axios');

exports.searchPage = async (req, res) => {
    const user_id = req.session.user_id;

    if (user_id === undefined) {
        res.redirect('/login');
        return;
    }

    available_organizations = [];
    available_apps = [];
    common_params = [];

    try {
        const responseOrg = await axios.get('http://error_handler_api:8080/users_organization', {
            params: {
                user_id
            }
        });

        available_organizations = responseOrg.data || [];

        if (available_organizations.length === 0) {
            res.render('search.ejs', {
                available_organizations: [],
                available_apps: []
            });
            return;
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
                available_apps.push(app);
            }
        }

        const responceParams = await axios.get('http://error_handler_api:8080/common_parameters', {
            params: {
                user_id
            }
        });
        common_params = responceParams.data || [];

        console.log('searchPage orgs');
        console.log(available_organizations);
        console.log('searchPage apps');
        console.log(available_apps);
        console.log('searchPage common_params');
        console.log(common_params);

        res.render('search.ejs', {
            available_organizations,
            available_apps,
            common_params
        });
    }
    catch (error) {
        console.log(error);
        res.status(500).send('Internal Server Error');
    }
}

exports.search = async (req, res) => {
    const user_id = req.session.user_id;
    const { selected_organizations, selected_apps, search_line } = req.body;

    console.log('search');
    console.log(selected_organizations);
    console.log(selected_apps);
    console.log(search_line);
    console.log('search');
    console.log(req.body);
    console.log('search');

    if (user_id === undefined) {
        res.redirect('/login');
        return;
    }

    console.log('search LINE ' + search_line);

    const param = search_line.split(':');
    const parameter_name = param[0];
    const parameter_value = param[1];

    console.log('search PARAMS');
    console.log(parameter_name);
    console.log(parameter_value);

    let eventsList = [];
    const eventsResponse = await axios.get('http://error_handler_api:8080/event_by_params', {
        params: {
            user_id,
            parameter_name,
            parameter_value
        }
    });
    eventsList = eventsResponse.data || [];

    console.log('search EVENTS');
    console.log(eventsList);

    appsList = [];
    if(selected_organizations.length > 0){
        if(selected_apps.length > 0){
            console.log('search selected_apps');
            apps_of_org = [];
            for (let i = 0; i < selected_organizations.length; i++) {
                const org = selected_organizations[i];
                const responseApps = await axios.get('http://error_handler_api:8080/apps', {
                    params: {
                        organization_id: org,
                        user_id
                    }
                });
                const apps = responseApps.data || [];
                apps_of_org.push(apps);
            }
            for (let i = 0; i < apps_of_org.length; i++) {
                for (let j = 0; j < selected_apps.length; j++) {
                    if(apps_of_org[i].id == selected_apps[j]){
                        appsList.push(apps_of_org[i]);
                    }
                }
            }
        }
        else{
            console.log('search selected_organizations only');
            for (let i = 0; i < selected_organizations.length; i++) {
                const org = selected_organizations[i];
                const responseApps = await axios.get('http://error_handler_api:8080/apps', {
                    params: {
                        organization_id: org,
                        user_id
                    }
                });
                const apps = responseApps.data || [];
                appsList.push(apps);
            }
        }
    }
    else{
        if(selected_apps.length > 0){
            console.log('search selected_apps only');
            for (let i = 0; i < selected_apps.length; i++) {
                const application = selected_apps[i];
                const responseApp = await axios.get('http://error_handler_api:8080/app', {
                    params: {
                        app_id: application
                    }
                });
                const app = responseApp.data || [];
                appsList.push(app);
            }
        }
    }

    events_of_apps = [];
    eventsList.forEach(event => {
        for (let i = 0; i < appsList.length; i++) {
            if(event.app_id == appsList[i].id){
                events_of_apps.push(event);
            }
        }
    });

    console.log("APPS LIST");
    console.log(appsList);

    console.log('search EVENTS');
    console.log(events_of_apps);

    res.render('search_results.ejs', {
        appsList,
        events_of_apps
    });
     
}

exports.detailedResult = async (req, res) => {
    const user_id = req.session.user_id;
    const event = JSON.parse(req.body.event);
    
    if (user_id === undefined) {
        res.redirect('/login');
        return;
    }

    console.log('detailedResult!!!!');
    console.log(req.body);
    console.log('detailedResult');
    console.log(event);

    const eventParamsResponse = await axios.get('http://error_handler_api:8080/event_parameters', {
        params: {
            event_id: event.id
        }
    });
    eventParams = eventParamsResponse.data || [];

    console.log('detailedResult EVENT');
    console.log(event);
    console.log('detailedResult EVENT PARAMS');
    console.log(eventParams);

    res.render('detailed_search_result.ejs', {
        event,
        eventParams
    });
}