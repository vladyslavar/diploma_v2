from aiohttp import web

# COMMON EVENTS

async def get_common_events(request):
    try:
        events = await request.app['db_connection'].fetch('''
            SELECT * FROM common_events
        ''')

        json_response = [dict(event) for event in events]
        return web.json_response(json_response)
    except KeyError:
        return web.Response(text="Bad Request", status=400)
    

    

# async def get_common_event(request):
#     try:
#         app_id = int(request.query.get('app_id'))
#         event_id = int(request.query.get('event_id'))
        
#         app = await request.app['db_connection'].fetchrow('''
#             SELECT * FROM app WHERE id = $1
#         ''', app_id)
#         if app is None:
#             return web.Response(text="App is not found", status=400)
        
#         common_events = await request.app['db_connection'].fetch('''
#             SELECT * FROM common_event_for_app WHERE app_id = $1
#         ''', app_id)
#         if common_events is None:
#             return web.Response(text="Event is not found", status=400)
        
#         json_response = [dict(event) for event in common_events]
#         return web.json_response(json_response)
    
#     except KeyError:
#         return web.Response(text="Missing app_id or event_name", status=400)


async def create_common_event(request):
    try:
        data = await request.json()

        event_name = data['event_name']
        event_description = data['event_description']

        existing_event = await request.app['db_connection'].fetchval('''
            SELECT name FROM common_events WHERE name = $1
        ''', event_name)
        if existing_event is not None:
            return web.Response(text="Event with the same name already exists", status=400)
        
        await request.app['db_connection'].execute('''
            INSERT INTO common_events (name, description)
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

        event_id = data['event_id']
        new_event_description = data['new_event_description']

        event = await request.app['db_connection'].fetchrow('''
            SELECT * FROM common_events WHERE id = $1
        ''', event_id)
        if event is None:
            return web.Response(text="Event is not found", status=400)

        await request.app['db_connection'].execute('''
            UPDATE common_events SET description = $1
            WHERE id = $2
        ''', new_event_description, event_id)
        return web.json_response({'status': 'success',
                                  'event_id': event_id,
                                  'enent_name': event['name'],
                                  'event_description': new_event_description})
    except KeyError as e:
        return web.Response(text=f"Missing {e.args[0]}", status=400)
    

async def delete_common_event(request):
    try:
        data = await request.json()

        event_id = data['event_id']

        event = await request.app['db_connection'].fetchrow('''
            SELECT * FROM common_events WHERE id = $1
        ''', event_id)
        if event is None:
            return web.Response(text="Event is not found", status=400)

        await request.app['db_connection'].execute('''
            DELETE FROM common_events WHERE id = $1
        ''', event_id)
        return web.json_response({'status': 'success',
                                  'event_id': event_id,
                                  'event_name': event['name']})
    except KeyError:
        return web.Response(text="Missing event_name", status=400)