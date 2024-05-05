from aiohttp import web

# CUSTOM EVENTS

#треба описати нажходження івенту, апку, 
# перевірити імя івенту якщо така ж як дефолтна, використати дефолтну
# якщо івент існує створити новий, якщо дефолтний і вже повзаний з апкою то також створити новий

async def get_all_events(request):
    try:
        app_id = int(request.query.get('app_id'))
        app = await request.app['db_connection'].fetchrow('''
            SELECT * FROM app WHERE id = $1
        ''', app_id)
        if app is None:
            return web.Response(text="App is not found", status=400)
        
        events = await request.app['db_connection'].fetch('''
            SELECT * FROM event WHERE app_id = $1
        ''', app_id)

        events_dict = [dict(event) for event in events]
        for event in events_dict:
            datetime = event['created_at']
            event['created_at'] = datetime.strftime("%Y-%m-%d %H:%M:%S")

        # events_common = await request.app['db_connection'].fetch('''
        #     SELECT * FROM common_event_for_app WHERE app_id = $1
        # ''', app_id)

        # events_common_dict = [dict(event) for event in events_common]
        # for event in events_common_dict:
        #     event_id = event['common_event_id']
        #     common_event = await request.app['db_connection'].fetchrow('''
        #         SELECT * FROM common_events WHERE id = $1
        #     ''', event_id)
        #     event['name'] = common_event['name']
        #     event['description'] = common_event['description']
        #     event['created_at'] = event['created_at'].strftime("%Y-%m-%d %H:%M:%S")

        json_response = events_dict

        return web.json_response(json_response)
    except KeyError:
        return web.Response(text="Missing app_id", status=400)
    

async def get_event(request):
    try:
        app_id = int(request.query.get('app_id'))
        event_id = int(request.query.get('event_id'))
        
        app = await request.app['db_connection'].fetchrow('''
            SELECT * FROM app WHERE id = $1
        ''', app_id)
        if app is None:
            return web.Response(text="App is not found", status=400)
        
        custom_events = await request.app['db_connection'].fetch('''
            SELECT * FROM event WHERE id = $1
        ''', event_id)
        if custom_events is None:
            return web.Response(text="Event is not found", status=400)
        
        json_response = [dict(event) for event in custom_events]
        return web.json_response(json_response)    
            
    except KeyError:
        return web.Response(text="Missing app_id or event_name", status=400)
    

async def add_event(request):
    try:
        data = await request.json()

        app_id = int(data['app_id'])
        event_name = data['event_name']
        event_description = data['event_description']
        parameters = data['parameters']
        
        app = await request.app['db_connection'].fetchrow('''
            SELECT * FROM app WHERE id = $1
        ''', app_id)
        if app is None:
            return web.Response(text="App is not found", status=400)
        
        # default_event = await request.app['db_connection'].fetchrow('''
        #     SELECT * FROM common_events WHERE name = $1
        # ''', event_name)
        # if default_event is not None:
            
        #     inserted_event_id = await request.app['db_connection'].fetchval('''
        #         INSERT INTO common_event_for_app (common_event_id, app_id, created_at)
        #         VALUES ($1, $2, CURRENT_TIMESTAMP) RETURNING id
        #     ''', default_event['id'], app_id)

        #     for parameter in parameters:
        #         parameter_name = parameter['parameter_name']
        #         parameter_value = parameter['parameter_value']
        #         await request.app['db_connection'].execute('''
        #             INSERT INTO event_parameter (event_id, parameter_name, parameter_value)
        #             VALUES ($1, $2, $3)
        #         ''', inserted_event_id, parameter_name, parameter_value)

        #     return web.json_response({'status': 'success (default event)',
        #                             'event_id': inserted_event_id,
        #                             'app_id': app_id,
        #                             'event_name': default_event['name'],
        #                             'event_description': default_event['description']})

        
        inserted_event_id = await request.app['db_connection'].fetchval('''
            INSERT INTO event (name, description, app_id, created_at)
            VALUES ($1, $2, $3, CURRENT_TIMESTAMP) RETURNING id
        ''', event_name, event_description, app_id)

        for parameter in parameters:
            parameter_name = parameter['parameter_name']
            parameter_value = parameter['parameter_value']
            await request.app['db_connection'].execute('''
                INSERT INTO event_parameter (event_id, parameter_name, parameter_value)
                VALUES ($1, $2, $3)
            ''', inserted_event_id, parameter_name, parameter_value)


        return web.json_response({'status': 'success',
                                'event_id': inserted_event_id,
                                'app_id': app_id,
                                'event_name': event_name,
                                'event_description': event_description})
       
    except KeyError as e:
        return web.Response(text=f"Missing {e.args[0]}", status=400)
    

async def delete_event(request):
    try:
        data = await request.json()

        app_id = int(data['app_id'])
        event_id = data['event_id']

        app = await request.app['db_connection'].fetchrow('''
            SELECT * FROM app WHERE id = $1
        ''', app_id)
        if app is None:
            return web.Response(text="App is not found", status=400)
        
        event = await request.app['db_connection'].fetchrow('''
            SELECT * FROM event WHERE id = $1
        ''', event_id)
        if event is None:
            return web.Response(text="Event is not found", status=400)
        
        await request.app['db_connection'].execute('''
            DELETE FROM event WHERE id = $1
        ''', event_id)

        return web.json_response({'status': 'success',
                                'app_id': app_id,
                                'event_id': event_id})

    except KeyError as e:
        return web.Response(text=f"Missing {e.args[0]}", status=400)