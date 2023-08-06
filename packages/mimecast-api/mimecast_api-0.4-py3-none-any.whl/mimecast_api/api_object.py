import datetime
from urllib.parse import urlsplit
import logging
from .errors import URLDecodeFail
from .post_rest import simple_exchange

class MimecastAPI:
    """Call into the Mimecast API.

    Methods here translate values into the form Mimecast expects in
    requests. There may not be a method in this class for every API
    endpoint. Patches are welcome.

    """
    
    def __init__(self, *, base_url, access_key, secret_key, app_id, app_key,
                 session=None):
        """Get ready to call into the Mimecast API.

        base_url is of the form 'https://xyz-api.mimecast.com'; see
        "Global Base URLs" in the Mimecast API documentation.

        access_key, secret_key, app_id, and app_key are the values
        necessary to authenticate API calls.

        session is a Requests session object. If passed in, it will be
        used.

        """
        self.base_url = base_url
        self.access_key = access_key
        self.secret_key = secret_key
        self.app_id = app_id
        self.app_key = app_key
        self.session = session
        self.log = logging.getLogger('McA')

    def _all_request(self, uri, **kwargs):
        """Call into the API, possibly returning multiple results."""
        self.log.debug('_a_r: request payload: %r', {'data': [kwargs]})
        return simple_exchange(self.base_url, self.access_key,
                               self.secret_key, self.app_id,
                               self.app_key, uri,
                               { 'data': [kwargs] },
                               self.session)
    
    def _single_request(self, uri, **kwargs):
        """Call into the API; expect and return only a single result."""
        return self._all_request(uri, **kwargs)[0]

    def decode_url(self, url):
        """Decode a URL hidden behind a Mimecast URL Protect redirect."""
        data = self._single_request('/api/ttp/url/decode-url', url=url)
        # if data['success'] is not True, an exception has already
        # been thrown, and we are not here.
        return data['url']

    def list_recent_recipients_from(self, header_from, since_days_ago):
        """Find out to whom an email address has sent messages lately."""
        def mimetime(utc_dt):
            return utc_dt.strftime('%Y-%m-%dT%H:%M:%S+0000')
        now = mimetime(datetime.datetime.utcnow())
        ago = mimetime(datetime.datetime.utcnow() -
                       datetime.timedelta(since_days_ago))
        data = self._single_request('/api/message-finder/search',
                                    start=ago,
                                    end=now,
                                    searchReason="cybersecurity investigation",
                                    advancedTrackAndTraceOptions={
                                        'from': header_from})
        return list(set(to_['emailAddress']
                        for mail in data['trackedEmails']
                        for to_ in mail['to']))

    def get_all_managed_urls(self, dns_domain):
        """List all managed URLs in a given DNS domain.

        In May 2020, passing in a URL failed to find anything, so we
        are going to say it has to be a DNS domain, and at the scale
        we're operating on right now, we can just iterate through the
        results.

        """
        return self._all_request('/api/ttp/url/get-all-managed-urls',
                                 domainOrUrl=dns_domain)

    def is_url_managed(self, url, *, only_match_domain_blocks=False):
        """Find out if a given URL is already blocked via Managed URLs.

        If only_match_domain_blocks is True, only search for
        domain-wide blocks; otherwise explicit URL blocks for this URL
        may also be found.

        Returns some information about the first matching managed URL
        entry (which is truthy), or False if none is found.

        """
        pieces = urlsplit(url)
        # i am not going to roll my own netloc splitter. maybe someone
        # else has made one, but i haven't searched it out, and YAGNI.
        if ':' in pieces.netloc:
            # e.g. http://foo.example.com:8080 -> netloc
            # foo.example.com:8080
            raise NotImplemented('non-default ports')
        if '@' in pieces.netloc:
            # e.g. http://user@foo.example.com -> netloc
            # user@foo.example.com
            raise NotImplemented('usernames in URLs')
        data = self._all_request('/api/ttp/url/get-all-managed-urls',
                                 domainOrUrl=pieces.netloc)
        for murl in data:
            # "Do not include a fragment (#)" when adding a managed
            # URL; so we do not match on it.
            if (not only_match_domain_blocks and
                murl['matchType'] == 'explicit' and
                murl['scheme'] == pieces.scheme and
                murl['domain'] == pieces.netloc and
                murl['path'] == pieces.path and
                ((murl['queryString'] == pieces.query)
                 if murl['queryString'] else True)):
                break
            elif (murl['matchType'] == 'domain' and
                  murl['domain'] == pieces.netloc):
                break
        else:
            return False
        # If we are here, murl is the first matching managed URL
        # entry. This non-empty dictionary will be truthy, if you
        # don't care about the details.
        return {'matchType': murl['matchType'],
                'action': murl['action'],
                'comment': murl['comment']}

    def block_url(self, url, matchType, comment):
        """Block a URL using Mimecast managed URLs.

        matchType must be 'explicit' or 'domain'. Return value from
        the API appears to be a new managed URL object, same as we
        would have found in a search above.

        https://www.mimecast.com/tech-connect/documentation/endpoint-reference/targeted-threat-protection-url-protect/create-managed-url/

        """
        # "Do not include a fragment (#)."
        defragged = urldefrag(url).url
        murl = self._single_request('/api/ttp/url/create-managed-url',
                                    action='block',
                                    matchType=matchType,
                                    url=defragged,
                                    comment=comment)
        return murl
