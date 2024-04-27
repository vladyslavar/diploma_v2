from aiohttp import web

# APPS
async def get_available_apps(request):
    try:
        organization_id = int(request.query.get('organization_id'))
        user_id = int(request.query.get('user_id'))

        organization = await request.app['db_connection'].fetchrow('''
            SELECT * FROM organization WHERE id = $1
        ''', organization_id)
        if organization is None:
            return web.Response(text="Organization is not found", status=400)
        
        organizations_for_user = await request.app['db_connection'].fetch('''
            SELECT organization_id FROM user_organization_access WHERE user_id = $1
        ''', user_id)
        if organization_id not in [org['organization_id'] for org in organizations_for_user]:
            return web.Response(text="User is not authorized for the action", status=403)
        
        apps = await request.app['db_connection'].fetch('''
            SELECT * FROM app WHERE organization_id = $1
        ''', organization_id)
        
        json_response = [dict(app) for app in apps]
        for app in json_response:
            del app['api_key']
            datetime = app['created_at']
            app['created_at'] = datetime.strftime("%Y-%m-%d %H:%M:%S")
        return web.json_response(json_response)
    except KeyError:
        return web.Response(text="Missing organization_name or user_id", status=400)
    

async def register_app(request):
    try:
        data = await request.json()

        organization_id = int(data['organization_id'])
        user_id = int(data['user_id'])
        app_name = data['app_name']
        api_key = data['api_key']

        organization = await request.app['db_connection'].fetchrow('''
            SELECT * FROM organization WHERE id = $1
        ''', organization_id)
        if organization is None:
            return web.Response(text="Organization is not found", status=400)
        
        orgonazation_owner_id = await request.app['db_connection'].fetchval('''
            SELECT owner_id FROM organization WHERE id = $1
        ''', organization_id)
        if user_id != orgonazation_owner_id:
            return web.Response(text="User is not authorized for the action", status=403)
        
        existing_app = await request.app['db_connection'].fetchval('''
            SELECT name FROM app WHERE name = $1
        ''', app_name)
        if existing_app is not None:
            return web.Response(text="App with the same name already exists", status=400)
        
        await request.app['db_connection'].execute('''
            INSERT INTO app (name, created_at, api_key, organization_id)
            VALUES ($1, CURRENT_TIMESTAMP, $2, $3)
        ''', app_name, api_key, organization_id)
        return web.json_response({'status': 'success',
                                  'app_name': app_name,
                                  'api_key': api_key})
    except KeyError as e:
        return web.Response(text=f"Missing {e.args[0]}", status=400)
    

async def update_app_name(request):
    try:
        data = await request.json()

        app_name = data['app_name']
        new_app_name = data['new_app_name']
        user_id = int(data['user_id'])
        organization_id = int(data['organization_id'])

        organization = await request.app['db_connection'].fetchrow('''
            SELECT * FROM organization WHERE id = $1
        ''', organization_id)
        if organization is None:
            return web.Response(text="Organization is not found", status=400)

        app = await request.app['db_connection'].fetchrow('''
            SELECT * FROM app WHERE name = $1
        ''', app_name)
        if app is None:
            return web.Response(text="App is not found", status=400)
        
        orgonazation_owner_id = await request.app['db_connection'].fetchval('''
            SELECT owner_id FROM organization WHERE id = $1
        ''', organization_id)
        if user_id != orgonazation_owner_id:
            return web.Response(text="User is not authorized for the action", status=403)
        
        names_of_apps_in_organization = await request.app['db_connection'].fetch('''
            SELECT name FROM app WHERE organization_id = $1
        ''', organization_id)
        if new_app_name in [app['name'] for app in names_of_apps_in_organization]:
            return web.Response(text="App with the new name already exists", status=400)
        
        await request.app['db_connection'].execute('''
            UPDATE app
            SET name = $1
            WHERE name = $2
        ''', new_app_name, app_name)
        return web.json_response({'status': 'success',
                                  'old_app_name': app_name,
                                  'new_app_name': new_app_name})
    except KeyError:
        return web.Response(text="Missing app_name or new_app_name", status=400)
    

async def update_app_api_key(request):
    try:
        data = await request.json()

        app_name = data['app_name']
        new_api_key = data['new_api_key']
        user_id = int(data['user_id'])
        organization_id = int(data['organization_id'])

        organization = await request.app['db_connection'].fetchrow('''
            SELECT * FROM organization WHERE id = $1
        ''', organization_id)
        if organization is None:
            return web.Response(text="Organization is not found", status=400)

        app = await request.app['db_connection'].fetchrow('''SELECT * FROM app WHERE name = $1 AND organization_id = $2''', app_name, organization_id)
        if app is None:
            return web.Response(text="App is not found", status=400)
        
        orgonazation_owner_id = await request.app['db_connection'].fetchval('''
            SELECT owner_id FROM organization WHERE id = $1
        ''', organization_id)
        if user_id != orgonazation_owner_id:
            return web.Response(text="User is not authorized for the action", status=403)
        
        await request.app['db_connection'].execute('''
            UPDATE app
            SET api_key = $1
            WHERE name = $2 AND organization_id = $3
        ''', new_api_key, app_name, organization_id)
        return web.json_response({'status': 'success',
                                  'app_name': app_name})
    except KeyError:
        return web.Response(text="Missing app_name or new_api_key", status=400)
    

async def delete_app(request):
    try:
        data = await request.json()

        app_id = int(data['app_id'])
        user_id = int(data['user_id'])
        organization_id = int(data['organization_id'])

        organization = await request.app['db_connection'].fetchrow('''
            SELECT * FROM organization WHERE id = $1
        ''', organization_id)
        if organization is None:
            return web.Response(text="Organization is not found", status=400)

        app = await request.app['db_connection'].fetchrow('''
            SELECT * FROM app WHERE id = $1
        ''', app_id)
        if app is None:
            return web.Response(text="App is not found", status=400)
        
        orgonazation_owner_id = await request.app['db_connection'].fetchval('''
            SELECT owner_id FROM organization WHERE id = $1
        ''', organization_id)
        if user_id != orgonazation_owner_id:
            return web.Response(text="User is not authorized for the action", status=403)
        
        await request.app['db_connection'].execute('''
            DELETE FROM app
            WHERE id = $1
        ''', app_id)
        return web.json_response({'status': 'success'})
    except KeyError:
        return web.Response(text="Missing app_name", status=400)
    

