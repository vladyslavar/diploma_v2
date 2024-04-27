const axios = require('axios');

exports.availableOrganizations = async (req, res) => {
    const user_id = req.session.user_id;

    if (user_id === undefined) {
        res.redirect('/login');
        return;
    }

    try {
        const all_organization_for_user_responce = await axios.get('http://error_handler_api:8080/users_organization', {
            params: {
                user_id
            }
        });

        let available_organizations = all_organization_for_user_responce.data || [];

        const all_owned_organizations_responce = await axios.get('http://error_handler_api:8080/organization_owner', {
            params: {
                user_id
            }
        });

        let owned_organizations = all_owned_organizations_responce.data || [];

        console.log("owned_organizations");
        console.log(owned_organizations);

        let member_organizations = [];
        // include only organizations that are not owned by the user
        for (let i = 0; i < available_organizations.length; i++) {
            const org = available_organizations[i];
            if (!owned_organizations.some(owned_org => owned_org.id === org.organization_id)) {
                member_organizations.push(org);
            }
        }
        
        
        for (let i = 0; i < member_organizations.length; i++) {
            const org = member_organizations[i];
            const response = await axios.get('http://error_handler_api:8080/organization', {
                params: {
                    organization_id: org.organization_id
                }
            });
            org.name = response.data;
            member_organizations[i] = org;
        }

        console.log("member_organizations");
        console.log(member_organizations);


        res.render('general_organization_configure.ejs', {
            member_organizations,
            owned_organizations
        });

    } catch (error) {
        console.log(error);
        res.status(500).send('Internal Server Error');
    }
}

exports.createOrganization = async (req, res) => {
    const owner_id = req.session.user_id;
    const { organization_name } = req.body;

    console.log(organization_name + ' ' + owner_id);

    try {
        await axios.post('http://error_handler_api:8080/create_organization', {
            organization_name,
            owner_id
        });

        res.redirect('/all_organizations');

    } catch (error) {
        console.log(error);
        res.status(500).send('Internal Server Error');
    }
}

exports.deleteOrganization = async (req, res) => {
    const user_id = req.session.user_id;
    const { organization_id } = req.body;

    try {
        await axios.post('http://error_handler_api:8080/delete_organization', {
            user_id,
            organization_id
        });

        res.redirect('/organization_configure');

    } catch (error) {
        console.log(error);
        res.status(500).send('Internal Server Error');
    }
}