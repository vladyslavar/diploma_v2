from aiohttp import web

# COMMON EVENTS

async def get_common_events(request):
    try:
        events = await request.app['db_connection'].fetch('''
            SELECT * FROM common_event
        ''')

        json_response = [dict(event) for event in events]
        return web.json_response(json_response)
    except KeyError:
        return web.Response(text="Bad Request", status=400)
    

async def create_common_event(request):
    try:
        data = await request.json()

        event_name = data['event_name']
        event_description = data['event_description']

        existing_event = await request.app['db_connection'].fetchval('''
            SELECT name FROM common_event WHERE name = $1
        ''', event_name)
        if existing_event is not None:
            return web.Response(text="Event with the same name already exists", status=400)
        
        await request.app['db_connection'].execute('''
            INSERT INTO common_event (name, description)
            VALUES ($1, $2)
        ''', event_name, event_description)
        return web.json_response({'status': 'success',
                                  'event_name': event_name,
                                  'event_description': event_description})
    
    except KeyError as e:
        return web.Response(text=f"Missing {e.args[0]}", status=400)
    

async def update_common_event(request):
    try:
        data = await request.json()

        event_name = data['event_name']
        new_event_name = data['new_event_name']
        new_event_description = data['new_event_description']

        event = await request.app['db_connection'].fetchrow('''
            SELECT * FROM common_event WHERE name = $1
        ''', event_name)
        if event is None:
            return web.Response(text="Event is not found", status=400)

        await request.app['db_connection'].execute('''
            UPDATE common_event SET name = $1, description = $2
            WHERE name = $3
        ''', new_event_name, new_event_description, event_name)
        return web.json_response({'status': 'success',
                                  'event_name': new_event_name,
                                  'event_description': new_event_description})
    except KeyError as e:
        return web.Response(text=f"Missing {e.args[0]}", status=400)
    

async def delete_common_event(request):
    try:
        data = await request.json()

        event_name = data['event_name']

        event = await request.app['db_connection'].fetchrow('''
            SELECT * FROM common_event WHERE name = $1
        ''', event_name)
        if event is None:
            return web.Response(text="Event is not found", status=400)

        await request.app['db_connection'].execute('''
            DELETE FROM common_event WHERE name = $1
        ''', event_name)
        return web.json_response({'status': 'success',
                                  'event_name': event_name})
    except KeyError:
        return web.Response(text="Missing event_name", status=400)