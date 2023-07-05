import azure.functions as func
import logging
import requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="wikiMediaLoginSample")
def wikiMediaLoginSample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    USERNAME = req.params.get('username')
    PASSWORD = req.params.get('password')
    if not USERNAME:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            USERNAME = req_body.get('username')
            PASSWORD = req_body.get('password')
    S = requests.Session()

    URL = "https://www.mediawiki.org/w/api.php"

    # Retrieve login token first
    PARAMS_0 = {
        'action':"query",
        'meta':"tokens",
        'type':"login",
        'format':"json"
    }

    R = S.get(url=URL, params=PARAMS_0)
    DATA = R.json()

    LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

    # Send a post request to login. Using the main account for login is not
    # supported. Obtain credentials via Special:BotPasswords
    # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword

    PARAMS_1 = {
        'action': "login",
        'lgname': USERNAME,
        'lgpassword': PASSWORD,
        'lgtoken': LOGIN_TOKEN,
        'format': "json"
    }
    newReq = requests.Request('POST', URL, data=PARAMS_1)
    prepared = newReq.prepare()
    logging.info(prepared.body)
    reqBody = prepared.body
    reqHeaders = prepared.headers
    R = S.post(URL, data=PARAMS_1)
    DATA = R.json()

    if DATA:
        return func.HttpResponse(f"Data return result {DATA['login']['result']}", status_code=200)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully but we did not get data returned.",
             status_code=200
        )