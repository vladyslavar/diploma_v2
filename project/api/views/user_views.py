from aiohttp import web

# USER ACCOUNTS
async def get_user_account(request):
    try:
        username = request.query.get('username')
        password = request.query.get('password')
        actual_password = await request.app['db_connection'].fetchval('''
            SELECT password FROM user_account WHERE username = $1
        ''', username)

        if actual_password is None:
            return web.Response(text="User is not found", status=400)
        if password == actual_password:
            response = await request.app['db_connection'].fetchrow('''
                SELECT * FROM user_account WHERE username = $1
            ''', username)
            json_response = dict(response)
            return web.json_response({'status': 'success',
                                      'user_account': json_response})
        else:
            return web.Response(text="Incorrect password", status=400)
    except KeyError:
        return web.Response(text="Bad Request", status=400)
    


async def get_user_by_id(request):
    user_id = int(request.query.get('user_id'))
    response = await request.app['db_connection'].fetchrow('''
            SELECT * FROM user_account WHERE id = $1
        ''', user_id)
    if response is None:
        return web.json_response({'status': 'error',
                                    'message': 'User is not found',
                                    'user_account': {}})
    json_response = dict(response)
    return web.json_response({'status': 'success',
                              'user_id': user_id,
                              'user_account': json_response})


async def create_user_account(request):
    try:
        data = await request.json()

        username = data['username']
        password = data['password']

        existing_username = await request.app['db_connection'].fetchval('''
            SELECT username FROM user_account WHERE username = $1
        ''', username)
        if existing_username is not None:
            return web.Response(text="Username already exists", status=400)
        
        await request.app['db_connection'].execute('''
            INSERT INTO user_account (username, password)
            VALUES ($1, $2)
        ''', username, password)

        created_user = await request.app['db_connection'].fetchrow('''
            SELECT * FROM user_account WHERE username = $1
        ''', username)
        json_response = dict(created_user)

        return web.json_response({'status': 'success',
                                  'user_account': json_response})
    except KeyError:
        return web.Response(text=f"Missing username or password: {request.json()}", status=400)
    

async def update_user_account_password(request):
    try:
        data = await request.json()

        username = data['username']
        old_password = data['old_password']
        new_password = data['new_password']

        password = await request.app['db_connection'].fetchval('''
            SELECT password FROM user_account WHERE username = $1
        ''', username)

        if password is None:
            return web.Response(text="User is not found", status=400)
        if password == old_password:
            await request.app['db_connection'].execute('''
                UPDATE user_account
                SET password = $1
                WHERE username = $2
            ''', new_password, username)
            return web.json_response({'status': 'success',
                                        'username': username,
                                        'password': new_password})
        else:
            return web.Response(text="Incorrect password", status=400)
    except KeyError:
        return web.Response(text="Missing username, old_password or new_password", status=400)
    
            
async def delete_user_account(request):
    try:
        data = await request.json()

        username = data['username']
        password = data['password']

        actual_password = await request.app['db_connection'].fetchval('''
            SELECT password FROM user_account WHERE username = $1
        ''', username)

        if actual_password is None:
            return web.Response(text="User is not found", status=400)
        if password == actual_password:
            await request.app['db_connection'].execute('''
                DELETE FROM user_account
                WHERE username = $1
            ''', username)
            return web.json_response({'status': 'success'})
        else:
            return web.Response(text="Incorrect password", status=400)
    except KeyError:
        return web.Response(text="Missing username or password", status=400)
     