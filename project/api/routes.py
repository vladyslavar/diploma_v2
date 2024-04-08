from views.test import *
from views.user_views import *
from views.organization_views import *


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