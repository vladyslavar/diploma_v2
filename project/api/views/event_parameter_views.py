from aiohttp import web

# EVENT PARAMETERS
async def get_event_parameters(request):
    try:
        event_id = int(request.query.get('event_id'))
        parameters = await request.app['db_connection'].fetch('''
            SELECT * FROM event_parameter WHERE event_id = $1
        ''', event_id)
        
        json_response = [dict(param) for param in parameters]
        return web.json_response(json_response)
    except KeyError:
        return web.Response(text="Missing event_id", status=400)
    


async def get_all_app_parameters(request):
    try:
        app_id = int(request.query.get('app_id'))

        does_app_exist = await request.app['db_connection'].fetchval('''
            SELECT id FROM app WHERE id = $1
        ''', app_id)
        if does_app_exist is None:
            return web.Response(text="App is not found", status=400)
        
        all_app_events = await request.app['db_connection'].fetch('''
            SELECT * FROM event WHERE app_id = $1
        ''', app_id)

        all_app_parameters = []
        for event in all_app_events:
            event_parameters = await request.app['db_connection'].fetch('''
                SELECT * FROM event_parameter WHERE event_id = $1
            ''', event['id'])
            all_app_parameters += [dict(param) for param in event_parameters]

        return web.json_response(all_app_parameters)
    
    except KeyError:
        return web.Response(text="Missing app_id", status=400)

    

async def add_event_parameter(request):
    try:
        data = await request.json()

        event_id = int(data['event_id'])
        parameter_name = data['parameter_name']
        parameter_value = data['parameter_value']

        is_event_exists = await request.app['db_connection'].fetchval('''
            SELECT id FROM event WHERE id = $1
        ''', event_id)
        if is_event_exists is None:
            return web.Response(text="Event is not found", status=400)

        existing_parameter = await request.app['db_connection'].fetchval(''' 
            SELECT parameter_name FROM event_parameter WHERE parameter_name = $1 AND event_id = $2
        ''', parameter_name, event_id)
        if existing_parameter is not None:
            return web.Response(text="Parameter with the same name already exists", status=400)
    
        await request.app['db_connection'].execute('''
            INSERT INTO event_parameter (event_id, parameter_name, parameter_value)
            VALUES ($1, $2, $3)
        ''', event_id, parameter_name, parameter_value)

        return web.json_response({'status': 'success',
                                    'event_id': event_id,
                                    'parameter_name': parameter_name,
                                    'parameter_value': parameter_value})
    except KeyError:
        return web.Response(text="Missing event_id, parameter_name or parameter_value", status=400)
    

async def update_event_parameter_value(request):
    try:
        data = await request.json()

        parameter_id = int(data['parameter_id'])
        new_parameter_value = data['new_parameter_value']

        parameter = await request.app['db_connection'].fetchrow('''
            SELECT * FROM event_parameter WHERE id = $1
        ''', parameter_id)
        if parameter is None:
            return web.Response(text="Parameter is not found", status=400)
        
        await request.app['db_connection'].execute('''
            UPDATE event_parameter SET parameter_value = $1
            WHERE id = $2
        ''', new_parameter_value, parameter_id)

        return web.json_response({'status': 'success',
                                    'parameter_id': parameter_id,
                                    'parameter_name': parameter['parameter_name'],
                                    'new_parameter_value': new_parameter_value})
    
    except KeyError:
        return web.Response(text="Missing event_id, parameter_name or new_parameter_value", status=400)


async def delete_event_parameter(request):
    try:
        data = await request.json()
        parameter_id = int(data['parameter_id'])

        parameter = await request.app['db_connection'].fetchrow('''
            SELECT * FROM event_parameter WHERE id = $1
        ''', parameter_id)
        
        if parameter is None:
            return web.Response(text="Parameter is not found", status=400)
        
        await request.app['db_connection'].execute('''
            DELETE FROM event_parameter WHERE id = $1
        ''', parameter_id)

        return web.json_response({'status': 'success',
                                    'parameter_id': parameter_id,
                                    'parameter_name': parameter['parameter_name']})
    
    except KeyError:
        return web.Response(text="Missing event_id or parameter_name", status=400)
