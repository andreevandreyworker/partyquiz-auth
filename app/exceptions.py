from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    status_code: int = 500
    code: str = "internal_error"

    def __init__(self, code: str | None = None):
        self.code = code or self.__class__.code
        super().__init__(self.code)


class LoginTakenError(AppError):
    status_code = 409
    code = "login_taken"


class InvalidCredentialsError(AppError):
    status_code = 401
    code = "invalid_credentials"


class NotAuthenticatedError(AppError):
    status_code = 401
    code = "not_authenticated"


class AccountRequiredError(AppError):
    status_code = 403
    code = "account_required"


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(
        request: Request, exc: AppError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": exc.code},
        )
