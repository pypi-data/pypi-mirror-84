from io import BytesIO
import json
import platform

from pydantic import parse_obj_as, validate_arguments
from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from mondobrain import __version__ as VERSION
from mondobrain.client import error
from mondobrain.client.types import (
    Api,
    Auth,
    BaseOptions,
    BaseResponse,
    Language,
    Solve,
)


class Client:
    """ Simple API accessor class

    API client for accessing the mondobrain APIs (internally referred to as Cacti).
    With endpoints mapped as methods on client instances users are able to quickly
    and easily call the MondoBrain API. Client instances handle switching between
    sending pure JSON post data and files in multipart requests depending on data
    types.

    Parameters
    ----------
    api_token : str
        The authentication/access token returned from an Auth0 call
    api_base : str, default None
        Stack to use for api calls. If none, the production stack is used

    Examples
    --------
    Testing your authentication token

    >>> client = mb.Client("sometoken")
    >>> client.auth_test()
    """

    def __init__(self, api_token: str, api_base: str = None):

        self._api_token = api_token
        self.api_base = api_base or "https://api.prod.mondobrain.com"
        self.session = Session()

        retries = Retry(
            total=1000,
            backoff_factor=1.9793,
            status_forcelist=[202],
            method_whitelist=["POST"],
        )
        retries.BACKOFF_MAX = 20

        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def api_call(
        self,
        method: str,
        options,
        options_model=BaseOptions,
        response_model=BaseResponse,
    ):
        """Call endpoints directly

        This method is useful for when you need to call an endpoint that hasn't been
        implemented in the SDK yet
        """
        if options is None:
            options = {}

        options = parse_obj_as(options_model, options)

        payload = {}
        files = None

        for key, value in options:
            if value is None:
                continue

            if isinstance(value, BytesIO):
                if files is None:
                    files = {}

                value = value.getvalue()
                files[key] = (key, value, "application/octet-stream")
            else:
                payload[key] = value

        if files is None:
            resp = self._make_request(method, json=payload)
        else:
            resp = self._make_request(method, data=payload, files=files)

        return parse_obj_as(response_model, resp)

    def _make_request(self, path, **kwargs) -> dict:
        abs_url = "%s/%s" % (self.api_base, path)

        headers = self._request_headers(self._api_token)

        resp = self.session.request("POST", abs_url, headers=headers, **kwargs)

        resp = self._interpret_response(resp)

        return resp

    def _request_headers(self, api_token: str) -> dict:
        user_agent = "Mondobrain/v1 PythonBindings/%s" % (VERSION,)

        ua = {
            "bindings_version": VERSION,
            "lang": "python",
            "publisher": "mondobrain",
            "httplib": "requests",
            "lang_version": platform.python_version(),
            "platform": platform.platform(),
            "uname": " ".join(platform.uname()),
        }

        headers = {
            "X-Mondobrain-Client-User-Agent": json.dumps(ua),
            "User-Agent": user_agent,
            "Authorization": "Bearer %s" % (api_token,),
        }

        return headers

    def _interpret_response(self, response: Response):
        rbody = response.text
        rcode = response.status_code
        rheaders = response.headers

        try:
            resp = response.json()
        except Exception:
            raise error.APIError(
                "Invalid response body from API: %s "
                "(HTTP response code was %d" % (response.text, response.status_code),
                response.text,
                response.status_code,
                response.headers,
            )

        if not 200 <= response.status_code <= 300:
            self._handle_error_response(rbody, rcode, resp, rheaders)

        return resp

    def _handle_error_response(self, rbody, rcode, resp, rheaders):
        try:
            error_data = {"type": resp["type"], "message": resp["message"]}

            code = resp.get("code", None)
            if code is not None:
                error_data["code"] = code

        except (KeyError, TypeError):
            raise error.APIError(
                "Invalid response object from API: %r (HTTP response code "
                "was %d)" % (rbody, rcode),
                rbody,
                rcode,
                resp,
            )

        err = self._specific_api_error(rbody, rcode, resp, rheaders, error_data)
        raise err

    def _specific_api_error(self, rbody, rcode, resp, rheaders, error_data):
        if rcode == 401:
            return error.AuthenticationError(
                error_data.get("message"),
                rbody,
                rcode,
                resp,
                rheaders,
                error_data.get("code"),
            )
        elif rcode == 402:
            return error.SolveError(
                error_data.get("message"),
                error_data.get("type"),
                error_data.get("code"),
                rbody,
                rcode,
                resp,
                rheaders,
            )
        elif rcode == 403:
            return error.PermissionError(
                error_data.get("message"), rbody, rcode, resp, rheaders
            )
        else:
            return error.APIError(
                error_data.get("message"), rbody, rcode, resp, rheaders
            )

    @validate_arguments
    def api_test(self, options: Api.TestOptions = None) -> Api.TestResponse:
        """Tests the ability to connect to the API
        """
        return self.api_call("api.test", options, response_model=Api.TestResponse)

    @validate_arguments
    def auth_test(self, options: Auth.TestOptions = None) -> Auth.TestResponse:
        """Tests that the authentication token is set correctly
        """
        return self.api_call("auth.test", options, response_model=Auth.TestResponse)

    @validate_arguments
    def solve_start(self, options: Solve.StartOptions) -> Solve.StartResponse:
        """Used for starting a solve using inline data (array of dicts)

        Parameters
        ----------
            options: :class: mondobrain.client.types.solve.StartOptions
        """
        return self.api_call("solve.start", options, response_model=Solve.StartResponse)

    @validate_arguments
    def solve_start_file(
        self, options: Solve.StartFileOptions
    ) -> Solve.StartFileResponse:
        """Used for starting a solve using a file to "carry" the data
        """
        return self.api_call(
            "solve.start.file", options, response_model=Solve.StartFileResponse
        )

    @validate_arguments
    def solve_result(self, options: Solve.ResultOptions) -> Solve.ResultResponse:
        """Read solve results (rules) from the API
        """
        return self.api_call(
            "solve.result", options, response_model=Solve.ResultResponse
        )

    @validate_arguments
    def language_entities(
        self, options: Language.EntitiesOptions
    ) -> Language.EntitiesResponse:
        """Use the API to extract entities in a sentence
        """
        return self.api_call(
            "langugage.entities", options, response_model=Language.EntitiesResponse
        )
