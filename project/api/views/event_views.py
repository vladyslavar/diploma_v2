from aiohttp import web
import json

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
    

async def get_last_n_events(request):
    try:
        app_id = int(request.query.get('app_id'))
        n = int(request.query.get('n'))

        app = await request.app['db_connection'].fetchrow('''
            SELECT * FROM app WHERE id = $1
        ''', app_id)

        if app is None:
            return web.Response(text="App is not found", status=400)
        
        events = await request.app['db_connection'].fetch('''
            SELECT * FROM event WHERE app_id = $1 ORDER BY created_at DESC LIMIT $2
        ''', app_id, n)

        events_dict = [dict(event) for event in events]
        for event in events_dict:
            datetime = event['created_at']
            event['created_at'] = datetime.strftime("%Y-%m-%d %H:%M:%S")

        json_response = events_dict

        return web.json_response(json_response)
    except KeyError:
        return web.Response(text="Missing app_id or n", status=400)


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
    

async def get_event_by_params(request):
    try:
        user_id = int(request.query.get('user_id'))
        parameter_name = request.query.get('parameter_name')
        parameter_value = request.query.get('parameter_value')

        parameters = await request.app['db_connection'].fetch('''
            SELECT * FROM event_parameter WHERE parameter_name = $1 AND parameter_value = $2
        ''', parameter_name, parameter_value)

        events = []
        for parameter in parameters:
            event_id = parameter['event_id']
            event = await request.app['db_connection'].fetchrow('''
                SELECT * FROM event WHERE id = $1
            ''', event_id)
            events.append(event)

        print(events)

        users_events = []
        for event in events:
            app_id = event['app_id']
            app = await request.app['db_connection'].fetchrow('''
                SELECT * FROM app WHERE id = $1
            ''', app_id)
            apps_organization = app['organization_id']
            print(apps_organization)
            user_has_access = await request.app['db_connection'].fetchval('''
                SELECT * FROM user_organization_access WHERE user_id = $1 AND organization_id = $2
            ''', user_id, apps_organization)
            if user_has_access is not None:
                print("User has access")
                users_events.append(event)

        json_response = [dict(event) for event in users_events]
        for responce in json_response:
            datetime = responce['created_at']
            responce['created_at'] = datetime.strftime("%Y-%m-%d %H:%M:%S")
        return web.json_response(json_response)
    

    except KeyError:
        return web.Response(text="Missing user_id or parameter_name or parameter_value", status=400)

    

    except KeyError:
        return web.Response(text="Missing user_id or parameter_name or parameter_value", status=400)

    


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
        
        # add event name to parameters
        parameters.append({'parameter_name': 'event_name', 'parameter_value': event_name})
        
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