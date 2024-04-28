const axios = require('axios');

exports.getOrganization = async (req, res) => {

    const user_id = req.session.user_id;
    if (user_id === undefined) {
        res.redirect('/login');
        return;
    }
    const organization_id = req.params.organization_id;

    const organization_response = await axios.get('http://error_handler_api:8080/organization', {
        params: {
            organization_id
        }
    });
    const organization = organization_response.data || {};

    console.log(organization);

    const organization_owner_response = await axios.get('http://error_handler_api:8080/user_info', {
        params: {
            user_id: organization.owner_id
        }
    });
    organization.owner = organization_owner_response.data.user_account;

    console.log(organization);

    const organization_members = await axios.get('http://error_handler_api:8080/organization_users', {
        params: {
            organization_id
        }
    }); 
    const members_id_data = organization_members.data || [];

    console.log(members_id_data);

    let members = [];
    for (let i = 0; i < members_id_data.length; i++) {
        console.log(members_id_data[i]);
        const member_id = members_id_data[i].user_id;
        const member_response = await axios.get('http://error_handler_api:8080/user_info', {
            params: {
                user_id: member_id
            }
        });
        members.push(member_response.data.user_account);
    }

    console.log(members);

    const organization_apps = await axios.get('http://error_handler_api:8080/apps', {
        params: {
            organization_id,
            user_id
        }
    });
    const apps = organization_apps.data || [];

    console.log(apps);  

    res.render('single_organization_configure.ejs', {
        organization,
        members,
        apps
    });

 };