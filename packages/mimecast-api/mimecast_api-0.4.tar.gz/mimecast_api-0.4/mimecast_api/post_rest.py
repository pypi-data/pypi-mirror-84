import base64
from hashlib import sha1
import json
import hmac
import uuid
import datetime
import requests
from urllib.parse import urljoin
from .errors import MimecastAPIFail

def simple_exchange(base_url, access_key, secret_key, app_id, app_key, uri, payload,
                    session=None):
    """Send a properly authenticated "post-REST" request; return the result.

    This function borrows heavily from the Python examples in
    Mimecast's API documentation. For the originals, and for more on
    "post-REST," a "customized variant of the REST model," see the
    Mimecast API documentation, starting at
    <https://www.mimecast.com/tech-connect/documentation/api-overview/api-concepts/>.

    base_url is the base API URL appropriate to the place in the world
    whence you are calling the Mimecast API,
    e.g. 'https://au-api.mimecast.com'.

    access_key, secret_key, app_id, and app_key are the values
    necessary to authenticate this client to Mimecast as an API
    application.

    uri is the relative URI of the desired API endpoint, e.g.
    '/api/provisioning/get-packages'.

    payload is the value for the POST body, given as Python objects
    which will be dumped to JSON before being sent.

    If you have a requests.Session object, perhaps to specify things
    like CA certificate locations across multiple requests, provide it
    as session and it will be used.

    In case of failure, Mimecast returns the most detailed failure
    information in a 'fail' attribute of the returned JSON object, so
    in case of problems we fail with that. If it isn't parsable, a
    Requests HTTP exception results, instead.

    """
    
    request_id = str(uuid.uuid4()).encode('ascii')
    hdr_date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S UTC").encode('utf8')
    hmac_sha1 = hmac.new(base64.b64decode(secret_key.encode("ascii")),
                         b':'.join([hdr_date, request_id,
                                    uri.encode('utf8'),
                                    app_key.encode('ascii')]),
                         digestmod=sha1).digest()
    sig = base64.encodestring(hmac_sha1).rstrip().decode('ascii')
    headers = {
        'Authorization': 'MC ' + access_key + ':' + sig,
        'x-mc-app-id': app_id,
        'x-mc-date': hdr_date,
        'x-mc-req-id': request_id,
        'Content-Type': 'application/json'
    }
    post = session.post if session else requests.post
    response = post(url=urljoin(base_url, uri),
                    headers=headers,
                    data=json.dumps(payload))
    # first - if we get valid JSON back, the best detail about
    # any error will be in its fail key, not the HTTP response
    # code. then - if getting or parsing JSON fails, first try to
    # raise any HTTP problem. otherwise, raise any other parsing
    # problems.
    try:
        j = response.json()
    except Exception:
        response.raise_for_status()
        raise
    if j['fail']:
        raise MimecastAPIFail(j)
    return j['data']
