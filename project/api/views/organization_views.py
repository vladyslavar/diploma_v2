from aiohttp import web

# ORGANIZATIONS
async def get_organization(request):
    try:
        data = await request.json()
        organization_id = data['organization_id']
        organization = await request.app['db_connection'].fetchrow('''
            SELECT * FROM organization WHERE id = $1
        ''', organization_id)

        if organization is None:
            return web.Response(text="Organization is not found", status=400)
        
        json_response = dict(organization)
        datetime = json_response['created_at']
        json_response['created_at'] = datetime.strftime('%Y-%m-%d %H:%M:%S')
        return web.json_response(json_response)
    except KeyError:
        return web.Response(text="Missing organization_name", status=400)
    

async def create_organization(request):
    try:
        data = await request.json()
        organization_name = data['organization_name']
        owner_id = data['owner_id']
        # if data['created_at'] == 'now':  # PAY ATTENTION TO THIS LINE
        #     await request.app['db_connection'].execute('''
        #     INSERT INTO organization (name, owner_id)
        #     VALUES ($1, $2)
        # ''', organization_name, owner_id)
        # else:
        #created_at = data['created_at']
        await request.app['db_connection'].execute('''
        INSERT INTO organization (name, owner_id, created_at)
        VALUES ($1, $2, CURRENT_TIMESTAMP)
        ''', organization_name, owner_id)        
        return web.json_response({'status': 'success',
                                  'organization_name': organization_name,
                                  'owner_id': owner_id})
    except KeyError as e:
        return web.Response(text=f"Missing {e.args[0]}", status=400)
    

async def update_organization_name(request):
    try:
        data = await request.json()
        organization_name = data['organization_name']
        new_organization_name = data['new_organization_name']
        user_id = data['user_id']
        organization_id = data['organization_id']

        organization = await request.app['db_connection'].fetchrow('''
            SELECT * FROM organization WHERE id = $1
        ''', organization_id)
        if organization is None:
            return web.Response(text="Organization is not found", status=400)

        actual_owner_id = await request.app['db_connection'].fetchval('''
            SELECT owner_id FROM organization WHERE id = $1
        ''', organization_id)
        if user_id != actual_owner_id:
            return web.Response(text="User is not authorized for the action", status=403)
        await request.app['db_connection'].execute('''
            UPDATE organization
            SET name = $1
            WHERE id = $2
        ''', new_organization_name, organization_id)

        return web.json_response({'status': 'success',
                                  'old_organization_name': organization_name,
                                  'new_organization_name': new_organization_name})
    except KeyError:
        return web.Response(text="Missing organization_name or new_organization_name", status=400)
    

async def update_organization_owner(request):
    try:
        data = await request.json()
        organization_id = data['organization_id']
        user_id = data['user_id']
        new_owner_id = data['new_owner_id']

        organization = await request.app['db_connection'].fetchrow('''
            SELECT * FROM organization WHERE id = $1
        ''', organization_id)
        if organization is None:
            return web.Response(text="Organization is not found", status=400)
        
        actual_owner_id = await request.app['db_connection'].fetchval('''
            SELECT owner_id FROM organization WHERE id = $1
        ''', organization_id)
        if user_id != actual_owner_id:
            return web.Response(text="User is not authorized for the action", status=403)
        
        await request.app['db_connection'].execute('''
            UPDATE organization
            SET owner_id = $1
            WHERE id = $2
        ''', new_owner_id, organization_id)

        await request.app['db_connection'].execute('''
            UPDATE user_organization_access
            SET user_id = $1
            WHERE organization_id = $2
        ''', new_owner_id, organization_id)
        
                                                   
        return web.json_response({'status': 'success',
                                  'new_owner_id': new_owner_id})
    except KeyError:
        return web.Response(text="Missing organization_id or new_owner_id", status=400)
    

async def delete_organization(request):
    try:
        data = await request.json()
        organization_id = data['organization_id']
        user_id = data['user_id']

        organization = await request.app['db_connection'].fetchrow('''
            SELECT * FROM organization WHERE id = $1
        ''', organization_id)
        if organization is None:
            return web.Response(text="Organization is not found", status=400)

        actual_owner_id = await request.app['db_connection'].fetchval('''
            SELECT owner_id FROM organization WHERE id = $1
        ''', organization_id)
        if user_id != actual_owner_id:
            return web.Response(text="User is not authorized for the action", status=403)

        await request.app['db_connection'].execute('''
            DELETE FROM organization
            WHERE id = $1
        ''', organization_id)
        return web.json_response({'status': 'success'})
    except KeyError:
        return web.Response(text="Missing organization_name", status=400)
    