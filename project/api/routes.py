from views.test import *
from views.user_views import *
from views.organization_views import *
from views.app_views import *
from views.user_organization_access_views import *
from views.common_event_views import *
from views.event_views import *
from views.event_parameter_views import *


def setup_routes(app):
    #test
    app.router.add_get('/', index)
    app.router.add_post('/post', post)
    app.router.add_post('/data_structure', data_structure)
    app.router.add_get('/error', error)
    #user
    app.router.add_get('/login', get_user_account)
    app.router.add_post('/create_account', create_user_account)
    app.router.add_post('/update_account_password', update_user_account_password)
    app.router.add_post('/delete_account', delete_user_account)
    #organization
    app.router.add_get('/organization', get_organization)
    app.router.add_post('/create_organization', create_organization)
    app.router.add_post('/update_organization_name', update_organization_name)
    app.router.add_post('/update_organization_owner', update_organization_owner)
    app.router.add_post('/delete_organization', delete_organization)
    #user_organization_access
    app.router.add_get('/users_organization', get_user_organization_access)
    app.router.add_get('/organization_owner', get_user_organization_owner_access)
    app.router.add_get('/organization_users', get_organization_users)
    app.router.add_post('/grant_access', grant_user_organization_access)
    app.router.add_post('/revoke_access', revoke_user_organization_access)
    #app
    app.router.add_get('/apps', get_available_apps)
    app.router.add_post('/register_app', register_app)
    app.router.add_post('/update_app_name', update_app_name)
    app.router.add_post('/update_app_key', update_app_api_key)
    app.router.add_post('/delete_app', delete_app)
    #common events
    app.router.add_get('/common_events', get_common_events)
    app.router.add_post('/create_common_event', create_common_event)
    app.router.add_post('/update_common_event', update_common_event)
    app.router.add_post('/delete_common_event', delete_common_event)
    #custom events
    app.router.add_get('/events', get_all_events)
    app.router.add_get('/event', get_event)
    app.router.add_post('/add_custom_events', add_custom_event)
    app.router.add_post('/delete_custom_event', delete_custom_event)
    #event parameters
    app.router.add_get('/event_parameters', get_event_parameters)
    app.router.add_post('/add_event_parameter', add_event_parameter)
    app.router.add_post('/update_event_parameter', update_event_parameter_value)
    app.router.add_post('/delete_event_parameter', delete_event_parameter)



