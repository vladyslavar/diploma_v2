from aiohttp import web

# USER ORGANIZATION ACCESS
async def get_user_organization_access(request):
    try:
        data = await request.json()
        user_id = data['user_id']
        organizations = await request.app['db_connection'].fetch('''
            SELECT * FROM user_organization_access WHERE user_id = $1
        ''', user_id)
        
        json_response = [dict(org) for org in organizations]
        return web.json_response(json_response)
    except KeyError:
        return web.Response(text="Missing user_id", status=400)
    

async def get_organization_users(request):
    try:
        data = await request.json()
        organization_id = data['organization_id']
        users = await request.app['db_connection'].fetch('''
            SELECT * FROM user_organization_access WHERE organization_id = $1
        ''', organization_id)
        
        json_response = [dict(user) for user in users]
        return web.json_response(json_response)
    except KeyError:
        return web.Response(text="Missing organization_id", status=400)
    

async def grant_user_organization_access(request):
    try:
        data = await request.json()
        organization_id = data['organization_id']
        user_to_grant_id = data['user_to_grant_id']
        current_user_id = data['current_user_id']
        
        organization = await request.app['db_connection'].fetchrow('''
            SELECT * FROM organization WHERE id = $1
        ''', organization_id)
        if organization is None:
            return web.Response(text="Organization is not found", status=400)
        
        actual_owner_id = await request.app['db_connection'].fetchval('''
            SELECT owner_id FROM organization WHERE id = $1
        ''', organization_id)
        if current_user_id != actual_owner_id:
            return web.Response(text="User is not authorized for the action", status=403)
        
        is_user_already_granted = await request.app['db_connection'].fetchval('''
            SELECT user_id FROM user_organization_access
            WHERE organization_id = $1 AND user_id = $2
        ''', organization_id, user_to_grant_id)
        if is_user_already_granted is not None:
            return web.Response(text="User is already granted access to the organization", status=400)
        
        await request.app['db_connection'].execute('''
            INSERT INTO user_organization_access (organization_id, user_id)
            VALUES ($1, $2)
        ''', organization_id, user_to_grant_id)
        return web.json_response({'status': 'success',
                                  'organization_id': organization_id,
                                  'user_to_grant_id': user_to_grant_id})
    except KeyError:
        return web.Response(text="Missing organization_id or user_id", status=400)
    

async def revoke_user_organization_access(request):
    try:
        data = await request.json()
        organization_id = data['organization_id']
        user_to_revoke_id = data['user_to_revoke_id']
        current_user_id = data['current_user_id']
        
        organization = await request.app['db_connection'].fetchrow('''
            SELECT * FROM organization WHERE id = $1
        ''', organization_id)
        if organization is None:
            return web.Response(text="Organization is not found", status=400)
        
        actual_owner_id = await request.app['db_connection'].fetchval('''
            SELECT owner_id FROM organization WHERE id = $1
        ''', organization_id)
        if current_user_id != actual_owner_id:
            return web.Response(text="User is not authorized for the action", status=403)
        
        does_user_have_access = await request.app['db_connection'].fetchval('''
            SELECT user_id FROM user_organization_access
            WHERE organization_id = $1 AND user_id = $2
        ''', organization_id, user_to_revoke_id)
        if does_user_have_access is None:
            return web.Response(text="User is not granted access to the organization", status=400)
        
        await request.app['db_connection'].execute('''
            DELETE FROM user_organization_access
            WHERE organization_id = $1 AND user_id = $2
        ''', organization_id, user_to_revoke_id)
        return web.json_response({'status': 'success',
                                  'organization_id': organization_id,
                                  'user_to_revoke_id': user_to_revoke_id})
    except KeyError:
        return web.Response(text="Missing organization_id or user_id", status=400)