from views.test import *
from views.user_views import *
from views.organization_views import *
from views.app_views import *
from views.user_organization_access_views import *


def setup_routes(app):
    #test
    app.router.add_get('/', index)
    app.router.add_post('/post', post)
    app.router.add_post('/data_structure', data_structure)
    #user
    app.router.add_get('/login', get_user_account)
    app.router.add_post('/create_account', create_user_account)
    app.router.add_put('/update_account_password', update_user_account_password)
    app.router.add_delete('/delete_account', delete_user_account)
    #organization
    app.router.add_get('/organization', get_organization)
    app.router.add_post('/create_organization', create_organization)
    app.router.add_put('/update_organization_name', update_organization_name)
    app.router.add_put('/update_organization_owner', update_organization_owner)
    app.router.add_delete('/delete_organization', delete_organization)
    #user_organization_access
    app.router.add_get('/users_organization', get_user_organization_access)
    app.router.add_get('/organization_users', get_organization_users)
    app.router.add_post('/grant_access', grant_user_organization_access)
    app.router.add_delete('/revoke_access', revoke_user_organization_access)
    #app
    app.router.add_get('/apps', get_available_apps)
    app.router.add_post('/register_app', register_app)
    app.router.add_put('/update_app_name', update_app_name)
    app.router.add_put('/update_app_key', update_app_api_key)
    app.router.add_delete('/delete_app', delete_app)

