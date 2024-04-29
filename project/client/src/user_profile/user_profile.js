const axios = require('axios');

exports.getUserProfile = async (req, res) => {
    const user_id = req.session.user_id;
    if (user_id === undefined) {
        res.redirect('/login');
        return;
    }

    const user_response = await axios.get('http://error_handler_api:8080/user_info', {
        params: {
            user_id
        }
    });
    const user = user_response.data.user_account || {};

    console.log(user);

    res.render('user_profile.ejs', {
        user
    });
}


exports.updateProfilePassword = async (req, res) => {
    const user_id = req.session.user_id;
    if (user_id === undefined) {
        res.redirect('/login');
        return;
    }

    const { old_password, new_password, repeat_new_password } = req.body;
    console.log(req.body);

    if (new_password !== repeat_new_password) {
        res.redirect('/user_profile?message=Passwords do not match');
        return;
    }

    await axios.post('http://error_handler_api:8080/update_account_password', {
        user_id,
        old_password,
        new_password
    })
    .then((response) => {
        res.redirect('/user_profile?message=Password updated');
    })
    .catch((error) => {
        console.log(error);
    });
}


exports.logout = async (req, res) => {
    req.session.user_id = undefined;
    res.redirect('/login');
}


exports.deleteProfile = async (req, res) => {
    const user_id = req.session.user_id;
    const { password } = req.body;

    if (user_id === undefined) {
        res.redirect('/login');
        return;
    }

    await axios.post('http://error_handler_api:8080/delete_account', {
        user_id,
        password
    })
    .then((response) => {
        req.session.user_id = undefined;
        res.redirect('/login');
    })
    .catch((error) => {
        console.log(error);
    });
}