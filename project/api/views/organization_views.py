from aiohttp import web

# ORGANIZATIONS
async def get_organization(request):
    try:
        data = await request.json()
        organization_name = data['organization_name']
        organization = await request.app['db_connection'].fetchrow('''
            SELECT * FROM organization WHERE name = $1
        ''', organization_name)
        return web.json_response(organization)
    except KeyError:
        return web.Response(text="Missing organization_name", status=400)
    

async def create_organization(request):
    try:
        data = await request.json()
        organization_name = data['organization_name']
        owner_id = data['owner_id']
        created_at = data['created_at']
        await request.app['db_connection'].execute('''
            INSERT INTO organization (name, owner_id, created_at)
            VALUES ($1, $2, $3)
        ''', organization_name, owner_id, created_at)
        return web.json_response({'status': 'success',
                                  'organization_name': organization_name,
                                  'owner_id': owner_id,
                                  'created_at': created_at})
    except KeyError:
        return web.Response(text="Missing organization_name, owner_id, or created_at", status=400)
    

async def update_organization_name(request):
    try:
        data = await request.json()
        organization_name = data['organization_name']
        new_organization_name = data['new_organization_name']
        await request.app['db_connection'].execute('''
            UPDATE organization
            SET name = $1
            WHERE name = $2
        ''', new_organization_name, organization_name)
        return web.json_response({'status': 'success',
                                  'old_organization_name': organization_name,
                                  'new_organization_name': new_organization_name})
    except KeyError:
        return web.Response(text="Missing organization_name or new_organization_name", status=400)
    

async def update_organization_owner(request):
    try:
        data = await request.json()
        organization_name = data['organization_name']
        new_owner_id = data['new_owner_id']
        await request.app['db_connection'].execute('''
            UPDATE organization
            SET owner_id = $1
            WHERE name = $2
        ''', new_owner_id, organization_name)
        return web.json_response({'status': 'success',
                                  'organization_name': organization_name,
                                  'new_owner_id': new_owner_id})
    except KeyError:
        return web.Response(text="Missing organization_name or new_owner_id", status=400)
    

async def delete_organization(request):
    try:
        data = await request.json()
        organization_name = data['organization_name']
        await request.app['db_connection'].execute('''
            DELETE FROM organization
            WHERE name = $1
        ''', organization_name)
        return web.json_response({'status': 'success',
                                  'organization_name': organization_name})
    except KeyError:
        return web.Response(text="Missing organization_name", status=400)
    