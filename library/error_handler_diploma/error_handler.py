import aiohttp


def some_method():
    print("This is a method")


async def handle_error_by_non_parsed_response(responce, **kwargs):

    try:
        responce_params = dict(responce.headers)
        custom_params = {}
        for key, value in kwargs.items():
            custom_params[key] = value

        api_key = custom_params.get("api_key", None)

        if api_key != None:
            custom_params.pop("api_key")
            api_key_responce = await check_api_key(api_key)

            print("api_key_responce: " + str(api_key_responce))

            if api_key_responce != False:
                print("key is valid")

                params = {**responce_params, **custom_params}
                print("params: " + str(params))

                event = {
                    "app_id": api_key_responce,
                    "event_name": str(responce.status) + " " + responce.reason,
                    "event_description": "",
                    "parameters": [
                        {"parameter_name": key, "parameter_value": value}
                            for key, value in params.items()
                        ]
                    }
                add_event_responce = await record_event_with_params(event)

                print("add_event_responce: " + str(add_event_responce))
                print("add_event_responce.status: " + str(add_event_responce['status']))
                return "success", "Event Recorded Successfully"
                
            else:
                return "Error: Invalid API Key"
            
        else:
            return "General Error: No API Key"
            

    except Exception as e:
        return "Error: ", e
    

# responce param is json
async def handle_error_by_parsed_response(responce):
    try:
        print("In handle_error_by_parsed_response: " + str(responce))
        api_key = responce.get("app_id", None)
        if api_key != None:
            api_key_responce = await check_api_key(api_key)
            responce.pop("app_id")
            print("api_key_responce: " + str(api_key_responce))
            if api_key_responce != False:
                print("key is valid")
                responce["app_id"] = api_key_responce
                add_event_responce = await record_event_with_params(responce)
                print("add_event_responce: " + str(add_event_responce))
                return "success", "Event Recorded Successfully"
            else:
                return "Error: Invalid API Key"
        else:
            return "General Error: No API Key"
        

    except Exception as e:
        return "Error: ", e    


async def check_api_key(api_key):
    async with aiohttp.ClientSession() as session:
        params = {
            "api_key": api_key
        }
        async with session.get('http://localhost:8080/check_api_key', params=params) as response:
            if response.status == 200:
                json_responce = await response.json()
                return json_responce.get("app_id", None)
            else:
                return False
            

async def record_event_with_params(data):
    print("In record_event: " + str(data))
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8080/record_event', json=data) as response:
            print("In record_event responce: " + str(response))
            json_responce = await response.json()
            return json_responce
        

async def record_parameter(data):
    print("In record_parameter: " + str(data))
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8080/add_event_parameter', json=data) as response:
            print("In record_parameter responce: " + str(response))
            waited_responce = await response.text()
            print(waited_responce)
            json_responce = await response.json()
            return json_responce