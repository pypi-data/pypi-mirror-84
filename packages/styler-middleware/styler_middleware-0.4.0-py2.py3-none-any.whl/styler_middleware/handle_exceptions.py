""" Middleware that handles exceptions
"""

import logging

from aiohttp import web


def handle_exceptions(
        generic_message='An error has occurred',
        status_code=500,
        error_handler=None):
    """ Generate a middleware that logs unexpected exceptions
        and returns a JSON response.

        Exceptions of type HTTPException won't be handled as they should be
        expected exceptions.
 
        Args:
            generic_message: The message that will be send as an error
            status_code: The HTTP status code (default = 500)
            error_handler: Callable(request, exception) to be executed when an exception occurs
    """
    @web.middleware
    async def middleware(request, handler):
        try:
            response = await handler(request)
            return response
        except web.HTTPException:
            raise
        except Exception as ex:
            message = str(ex)
            if error_handler:
                error_handler(request, ex)
            logging.exception('Error: %s', message)
            return web.json_response(
                {'error': generic_message},
                status=status_code
            )
    return middleware
