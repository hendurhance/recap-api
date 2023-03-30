from fastapi import status
from fastapi.responses import JSONResponse

def success_response(data, message, status_code=status.HTTP_200_OK):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "success",
            "message": message,
            "data": data
        }
    )

def error_response(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message
        }
    )

def not_found_response(message, status_code=status.HTTP_404_NOT_FOUND):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message
        }
    )

def bad_request_response(message, status_code=status.HTTP_400_BAD_REQUEST):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message
        }
    )

def unauthorized_response(message, status_code=status.HTTP_401_UNAUTHORIZED):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message
        }
    )

def forbidden_response(message, status_code=status.HTTP_403_FORBIDDEN):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message
        }
    )

def conflict_response(message, status_code=status.HTTP_409_CONFLICT):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message
        }
    )

def unprocessable_entity_response(message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message
        }
    )

def too_many_requests_response(message, status_code=status.HTTP_429_TOO_MANY_REQUESTS):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message
        }
    )

def service_unavailable_response(message, status_code=status.HTTP_503_SERVICE_UNAVAILABLE):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message
        }
    )

def gateway_timeout_response(message, status_code=status.HTTP_504_GATEWAY_TIMEOUT):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message
        }
    )