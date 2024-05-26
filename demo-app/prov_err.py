import aiohttp
import asyncio
from error_handler_diploma import error_handler
import subprocess

async def provoke_error():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8080/add_event_parameter') as response:
                
                return response

    except Exception as e:
        print("Error: ", e)


async def provoke_error_404():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8080/dumb_pass') as response:
                
                return response

    except Exception as e:
        print("Error: ", e)




async def main():    
    responce= await provoke_error()

    current_machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
    api_key = "8ec6ab43-8ac4-441a-b616-ba4a2cde1e4e"
    print (current_machine_id)
    
    handled_error_responce = await error_handler.handle_error_by_non_parsed_response(responce, machine_id=current_machine_id, api_key=api_key)

    print(handled_error_responce)


    ### parsed response
    # params = {}
    # for key, value in responce.headers.items():
    #     params[key] = value

    # parsed_responce = {
    #     "app_id": api_key,
    #     "event_name": str(responce.status) + " " + responce.reason,
    #     "event_description": "",
    #     "parameters": [
    #         {"parameter_name": key, "parameter_value": value}
    #             for key, value in params.items()
    #         ]
    #     }
    
    # handled_parsed_error_responce = await error_handler.handle_error_by_parsed_response(parsed_responce)
    # print(handled_parsed_error_responce)



if __name__ == "__main__":
    asyncio.run(main())