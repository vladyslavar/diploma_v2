from aiohttp import web

# CUSTOM EVENTS

#треба описати нажходження івенту, апку, 
# перевірити імя івенту якщо така ж як дефолтна, використати дефолтну
# якщо івент існує створити новий, якщо дефолтний і вже повзаний з апкою то також створити новий

async def get_all_events(request):
    try:
        data = await request.json()
        app_id = data['app_id']
        app = await request.app['db_connection'].fetchrow('''
            SELECT * FROM app WHERE id = $1
        ''', app_id)
        if app is None:
            return web.Response(text="App is not found", status=400)
        
        events_custom = await request.app['db_connection'].fetch('''
            SELECT * FROM event WHERE app_id = $1
        ''', app_id)

        events_common = await request.app['db_connection'].fetch('''
            SELECT * FROM common_event_for_app WHERE app_id = $1
        ''', app_id)
 
        json_response = [dict(event) for event in events_custom]
        json_response += [dict(event) for event in events_common]

        return web.json_response(json_response)
    except KeyError:
        return web.Response(text="Missing app_id", status=400)
    

async def get_event(request):
    try:
        data = await request.json()
        app_id = data['app_id']
        event_name = data['event_name']
        app = await request.app['db_connection'].fetchrow('''
            SELECT * FROM app WHERE id = $1
        ''', app_id)
        if app is None:
            return web.Response(text="App is not found", status=400)
        
        event_custom = await request.app['db_connection'].fetchrow('''
            SELECT * FROM event WHERE name = $1 AND app_id = $2
        ''', event_name, app_id)
        if event_custom is None:
            event_common = await request.app['db_connection'].fetchrow('''
                SELECT * FROM common_event_for_app WHERE name = $1 AND app_id = $2
            ''', event_name, app_id)
            if event_common is None:
                return web.Response(text="Event is not found", status=400)
            else:
                return web.json_response(dict(event_common))
        else:
            return web.json_response(dict(event_custom))
            
    except KeyError:
        return web.Response(text="Missing app_id or event_name", status=400)


async def add_custom_event(request):
    try:
        data = await request.json()
        app_id = data['app_id']
        event_name = data['event_name']
        event_description = data['event_description']
        
        app = await request.app['db_connection'].fetchrow('''
            SELECT * FROM app WHERE id = $1
        ''', app_id)
        if app is None:
            return web.Response(text="App is not found", status=400)
        
        is_default_event = await request.app['db_connection'].fetchval('''
            SELECT id FROM common_event WHERE name = $1
        ''', event_name)
        if is_default_event is not None:
            common_event_id = await request.app['db_connection'].fetchval('''
                SELECT id FROM common_event WHERE name = $1
            ''', event_name)
            await request.app['db_connection'].execute('''
                INSERT INTO common_event_for_app (common_event_id, app_id, created_at)
                VALUES ($1, $2, CURRENT_TIMESTAMP)
            ''', common_event_id, app_id)

            return web.json_response({'status': 'success (default event)',
                                    'app_id': app_id,
                                    'event_name': event_name,
                                    'event_description': event_description})

        else:
            await request.app['db_connection'].execute('''
                INSERT INTO event (name, description, app_id, created_at)
                VALUES ($1, $2, $3, CURRENT_TIMESTAMP)
            ''', event_name, event_description, app_id)

            return web.json_response({'status': 'success (custom event)',
                                    'app_id': app_id,
                                    'event_name': event_name,
                                    'event_description': event_description})

    except KeyError as e:
        return web.Response(text=f"Missing {e.args[0]}", status=400)
    

async def delete_custom_event(request):
    try:
        data = await request.json()
        app_id = data['app_id']
        event_name = data['event_name']

        app = await request.app['db_connection'].fetchrow('''
            SELECT * FROM app WHERE id = $1
        ''', app_id)
        if app is None:
            return web.Response(text="App is not found", status=400)

        event_custom = await request.app['db_connection'].fetchrow('''
            SELECT * FROM event WHERE name = $1 AND app_id = $2
        ''', event_name, app_id)
        if event_custom is None:
            event_common = await request.app['db_connection'].fetchrow('''
                SELECT * FROM common_event_for_app WHERE name = $1 AND app_id = $2
            ''', event_name, app_id)
            if event_common is None:
                return web.Response(text="Event is not found", status=400)
            else:
                await request.app['db_connection'].execute('''
                    DELETE FROM common_event_for_app WHERE name = $1 AND app_id = $2
                ''', event_name, app_id)
        else:
            await request.app['db_connection'].execute('''
                DELETE FROM event WHERE name = $1 AND app_id = $2
            ''', event_name, app_id)

        return web.json_response({'status': 'success',
                                    'app_id': app_id,
                                    'event_name': event_name})

    except KeyError as e:
        return web.Response(text=f"Missing {e.args[0]}", status=400)