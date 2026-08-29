from fastapi import HTTPException, status


def handle_service_error(exc: ValueError) -> HTTPException:
    error_msg = str(exc)

    if 'not found' in error_msg.lower():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)