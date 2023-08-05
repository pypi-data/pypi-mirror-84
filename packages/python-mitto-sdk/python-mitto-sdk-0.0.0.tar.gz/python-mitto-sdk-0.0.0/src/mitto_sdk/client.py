import requests


class Mitto:
    """
    Mitto instance
    """
    def __init__(self, base_url, api_key, verify=True):
        if base_url.endswith("/"):
            self.base_url = base_url[:-1]
        else:
            self.base_url = base_url
        self.api_key = api_key
        self.api_root = "/api"

        self.verify = verify

        # set up the session
        self.session = requests.Session()
        self.session.params = {
            "API_KEY": self.api_key
        }

    def page_through_results(self, url, params, limit=50, offset=0):
        params["offset"] = offset
        params["limit"] = limit
        more_pages = True

        while more_pages:
            response = self.session.get(url=url, params=params)
            response.raise_for_status()
            data = response.json()
            pagination = data.get("pagination")
            if pagination:
                more_pages = pagination.get("more_pages")
                offset = pagination.get("offset")
                params["offset"] = offset + params["limit"]
            yield data

    def get_jobs(self, search=None, tag=None, job_type=None, status=None, **kwargs):
        uri = "/v2/jobs"
        url = f"{self.base_url}{self.api_root}{uri}"

        params = {
            "search": search,
            "tag": tag,
            "type": job_type,
            "status": status
        }

        results = self.page_through_results(url=url, params=params, **kwargs)
        for result in results:
            yield from result["jobs"]

    def get_about(self):
        uri = "/about"
        url = f"{self.base_url}{self.api_root}{uri}"

        results = self.session.get(url)
        return results.json()
