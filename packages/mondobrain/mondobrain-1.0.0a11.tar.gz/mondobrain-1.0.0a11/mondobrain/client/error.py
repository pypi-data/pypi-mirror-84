class APIError(Exception):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super(APIError, self).__init__(message)

        if http_body and hasattr(http_body, "decode"):
            try:
                http_body = http_body.decode("utf-8")
            except BaseException:
                http_body = (
                    "<Could not decode body as utf-8. "
                    "Please report to support@stripe.com>"
                )

        self._message = message
        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}
        self.code = code
        self.error = self.load_error()

    def __str__(self):
        msg = self._message or "<empty message>"
        return msg

    @property
    def user_message(self):
        return self._message

    def __repr__(self):
        return "%s(message=%r, http_status=%r,)" % (
            self.__class__.__name__,
            self._message,
            self.http_status,
        )

    def load_error(self):
        if (
            self.json_body is None
            or "error" not in self.json_body
            or not isinstance(self.json_body["error"], dict)
        ):
            return None

        return self.json_body["error"]


class APIConnectionError(APIError):
    def __init__(
        self,
        message,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
        should_retry=False,
    ):
        super(APIConnectionError, self).__init__(
            message, http_body, http_status, json_body, headers, code
        )

        self.should_retry = should_retry


class SolveError(APIError):
    def __init__(
        self,
        message,
        type,
        code,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
    ):
        super(SolveError, self).__init__(
            message, http_body, http_status, json_body, headers, code
        )

        self.type = type


class AuthenticationError(APIError):
    pass


class PermissionError(APIError):
    pass
