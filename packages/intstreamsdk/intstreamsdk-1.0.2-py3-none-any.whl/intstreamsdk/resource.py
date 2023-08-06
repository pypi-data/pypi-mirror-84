import requests
from datetime import datetime
from intstreamsdk.client import Client
import tldextract
import logging

LOG = logging.getLogger(__name__)


class Resource(object):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

    def __init__(self, client, method=None):
        self.client = client
        self.base = self.client.server_url+"api/"
        self.endpoint=None  # assign endpoint to append to self.base
        self.request_url=None  # final url to make the request call
        self.method = method
        self.valid_codes = {Resource.GET: [200],
                            Resource.PUT: [200],
                            Resource.POST: [201,200],
                            Resource.DELETE: [204]}
        self.json = None# any json data to send with request
        self.params = {}  # any query string parameters to send with request
        self.headers = {}  # any headers to send with request
        self.files = None

    def full_request(self, raise_exc=True):
        """
        returns response and data for sync requests
        :param rasise_exc: bool
        :return:
        """
        pre_r = self.client.request(method=self.method,
                                headers=self.headers,
                                request_url=self.request_url,
                                params=self.params,
                                json=self.json,
                                files=self.files
                                )
        r = self.client.get_actual_response(pre_r)
        if raise_exc:
            r.raise_for_status()
        return self.getdata(r)

    def request(self):
        """
        returns response and data for sync requests
        :param rasise_exc: bool
        :return:
        """
        r = self.client.request(method=self.method,
                                headers=self.headers,
                                request_url=self.request_url,
                                params=self.params,
                                json=self.json,
                                )
        return r

    def getdata(self, response):
        """
        Test for html error code and return data
        :param response
        :return:
        """
        actual_response = response
        result = {}
        if actual_response.status_code in self.valid_codes[self.method]:
            result["status"] = self.SUCCESS
            result["response_code"] = actual_response.status_code
            format = actual_response.headers.get("Content-Type", None)
            if format == Client.FORMAT_JSON:
                json_response = actual_response.json()
                if isinstance(json_response, list):
                    result["data"] = {"results": json_response}
                else:
                    result["data"] = actual_response.json()

            elif format == Client.FORMAT_XML:
                result["data"]=actual_response.content.decode("utf8")
            else:
                result["data"]=actual_response.content
        else:
            result["status"] = self.FAILED
            result["response_code"] = actual_response.status_code
            result["data"] = actual_response.content.decode('utf8')
        return result

    def filter(self, filter):
        """

        :param filter: dict
        :return:
        """
        params = "?"
        count = 0
        for key, value in filter.items():
            if count == 0:
                params += key + "=" + str(value)
            else:
                params += "&" + key + "=" + str(value)
            count +=1

        self.request_url = '{current}{params}'.format(current=self.request_url,
                                                   params=params)

    def id(self, id):
        self.request_url = '{current}{id}/'.format(current=self.request_url,
                                                   id=id)


class ResourcePaged(Resource):

    def __init__(self,client,method=Resource.GET):
        super(ResourcePaged,self).__init__(client,method)
        self.first=True
        self.next=None #data field with next url
        self.previous=None #data field with previous url
        # for next if null we are done paging

    def __iter__(self):
        return self

    def __next__(self):
        if self.next is not None or self.first is not False:
            self.first=False
            if self.next is not None:
                self.request_url=self.next
            response = super(ResourcePaged,self).full_request()
            self.next = response["data"]["next"]
        else:
            raise StopIteration


class BaseArticle(ResourcePaged):
    def __init__(self, endpoint, client:Client, method=Resource.GET, ):
        super(BaseArticle,self).__init__(client, method)
        self.endpoint = endpoint
        self.request_url = '{base}{endpoint}'.format(base=self.base,
                                                         endpoint=self.endpoint)

    def article_post(self, title, source_id, filename):
        #set format to multipart
        """
        :param title: str
        :param file_h: file
        :return:
        """
        self.files = {"title": (None, title),
                      "source": (None, source_id),
                      "file": open(filename, "rb")}


class TextArticle(BaseArticle):
    def __init__(self, client:Client, method=Resource.GET):
        super(TextArticle,self).__init__("txtarticles/", client, method)


class HtmlArticle(BaseArticle):
    def __init__(self, client:Client, method=Resource.GET):
        super(HtmlArticle,self).__init__("htmlarticles/", client, method)


class PDFArticle(BaseArticle):
    def __init__(self, client:Client, method=Resource.GET):
        super(PDFArticle,self).__init__("pdfarticles/", client, method)


class WordDocxArticle(BaseArticle):
    def __init__(self, client:Client, method=Resource.GET):
        super(WordDocxArticle, self).__init__("pdfarticles/", client, method)


class RawArticle(ResourcePaged):
    def __init__(self, client:Client, method=Resource.GET):
        super(RawArticle,self).__init__(client, method)
        self.endpoint = "rawarticles/"
        self.request_url = '{base}{endpoint}'.format(base=self.base,
                                                         endpoint=self.endpoint)

    def article_post(self, title, source_id, text):
        """
        :param title: str
        :param source_id: int
        :param text: str
        :return:
        """
        self.json = {"title": title,
                     "source": source_id,
                     "text": text}


class Indicator(ResourcePaged):
    def indicators_post(self, indicators):
        """

        :param indicators: list[str]
        :return:
        """
        self.json = [{"value": i} for i in indicators]



class MD5(Indicator):

    def __init__(self, client:Client, method=Resource.GET):
        super(MD5,self).__init__(client, method)
        self.endpoint = "indicatormd5/"
        self.request_url = '{base}{endpoint}'.format(base=self.base,
                                                         endpoint=self.endpoint)


class SHA1(Indicator):

    def __init__(self, client:Client, method=Resource.GET):
        super(SHA1,self).__init__(client, method)
        self.endpoint = "indicatorsha1/"
        self.request_url = '{base}{endpoint}'.format(base=self.base,
                                                     endpoint=self.endpoint)


class SHA256(Indicator):

    def __init__(self, client:Client, method=Resource.GET):
        super(SHA256,self).__init__(client, method)
        self.endpoint = "indicatorsha256/"
        self.request_url = '{base}{endpoint}'.format(base=self.base,
                                                     endpoint=self.endpoint)


class Email(Indicator):

    def __init__(self, client:Client, method=Resource.GET):
        super(Email, self).__init__(client, method)
        self.endpoint = "indicatoremail/"
        self.request_url = '{base}{endpoint}'.format(base=self.base,
                                                     endpoint=self.endpoint)


class IPV4(Indicator):

    def __init__(self, client:Client, method=Resource.GET):
        super(IPV4, self).__init__(client, method)
        self.endpoint = "indicatoripv4/"
        self.request_url = '{base}{endpoint}'.format(base=self.base,
                                                     endpoint=self.endpoint)


class IPV6(Indicator):

    def __init__(self, client:Client, method=Resource.GET):
        super(IPV6, self).__init__(client, method)
        self.endpoint = "indicatoripv6/"
        self.request_url = '{base}{endpoint}'.format(base=self.base,
                                                     endpoint=self.endpoint)


class PartsNetLoc(object):
    def __init__(self, subdomain, domain, suffix_id):
        """

        :param subdomain: str
        :param domain: str
        :param suffix_id: int
        """
        self.subdomain = subdomain
        self.domain = domain
        self.suffix_id = suffix_id


class PartsNetLocValue(object):
    def __init__(self, subdomain=None, domain=None, suffix__value=None):
        """

        :param subdomain: str
        :param domain: str
        :param suffix_id: int
        """
        self.subdomain = subdomain
        self.domain = domain
        self.suffix__value = suffix__value

    def full_domain(self):
        if self.subdomain is not None:
            self.subdomain += self.subdomain + "."
        else:
            self.subdomain = ""
        return self.subdomain + self.domain + "." + self.suffix__value


class NetLoc(Indicator):
    def __init__(self, client:Client, method=Resource.GET):
        super(NetLoc, self).__init__(client, method)
        self.endpoint = "indicatornetloc/"
        self.request_url = '{base}{endpoint}'.format(base=self.base,
                                                     endpoint=self.endpoint)

    def indicators_post(self, indicators):
        """

        :param indicators: list[PartsNetLoc]
        :return:
        """

        self.json = [{"subdomain": i.subdomain,
                      "domain": i.domain,
                      "suffix": i.suffix_id} for i in indicators]


class Suffix(Indicator):
    def __init__(self, client:Client, method=Resource.GET):
        super(Suffix, self).__init__(client, method)
        self.endpoint = "indicatorsuffix/"
        self.request_url = '{base}{endpoint}'.format(base=self.base,
                                                     endpoint=self.endpoint)


class IntstreamSDKException(Exception):
    pass


class NoTLD(IntstreamSDKException):
    pass


class ColumnNotFound(IntstreamSDKException):
    pass


class DomainExtractor(object):
    def __init__(self, url, client:Client, raise_exc=True):
        """
        :param client:
        :param url:
        """
        self.subdomain, self.domain, self.suffix = tldextract.extract(url)
        if self.suffix is None and raise_exc:
            raise NoTLD
        resource = Suffix(client)
        resource.filter(filter={"value":self.suffix})
        r = resource.full_request(raise_exc=raise_exc)
        suffix_id="NA"
        if r["status"] == Resource.SUCCESS:
            suffix_id = r["data"]["results"][0]["id"]
        self.net_loc = PartsNetLoc(subdomain=self.subdomain,
                                  domain=self.domain,
                                  suffix_id=suffix_id)


class DomainLoader(object):
    def __init__(self, urls, client:Client,):
        """
        :param urls: list[str]
        :param client: Client
        :param raise_exc: bool
        """
        self.urls = ["http://" + i for i in urls]
        self.client = client

    def _get_perform(self, method):
        """

        :param method: str
        :return: list[dict]
        """
        net_locs = []
        all_data = []
        for i in self.urls:
            extractor = DomainExtractor(i, self.client,)
            resource_get = NetLoc(self.client, method=Resource.GET)
            filter = {
                "subdomain":extractor.net_loc.subdomain,
                "domain":extractor.net_loc.domain,
                "suffix":extractor.net_loc.suffix_id
            }
            resource_get.filter(filter=filter)
            r = resource_get.full_request()
            if r["status"] == Resource.SUCCESS and r["data"]["count"] == 0:
                net_locs.append(extractor.net_loc)
            else:
                all_data.extend(r["data"]["results"])

        resource = NetLoc(self.client, method=Resource.POST)
        resource.indicators_post(net_locs)
        res = resource.full_request()
        all_data.extend(res["data"]["results"])
        return all_data

    def upload(self):
        """
        :return: list[dict]
        """
        res = self._get_perform(method=Resource.POST)
        return res

    def delete(self):
        """
        :return: list[dict]
        """
        res = self._get_perform(method=Resource.DELETE)
        return res


class Link(Indicator):

    def __init__(self, client:Client, method=Resource.GET, article_id=None, indicator_ids=None):
        super(Link, self).__init__(client, method)
        self.endpoint = "articles/{id}/link/".format(id=article_id)
        self.request_url = '{base}{endpoint}'.format(base=self.base,
                                                     endpoint=self.endpoint)
        self.json = {
            "indicator_ids": [i for i in indicator_ids]
        }


class Uploader(object):
    def __init__(self, client):
        self.client = client

    def check_upload(self,
                     indicators,
                     resource_class,
                     ):
        resource_get = resource_class(client=self.client, method=Resource.GET)
        filter = {"value_in":indicators}
        resource_get.filter(filter)
        response_get = resource_get.full_request()
        existing = [i["value"] for i in response_get["data"]["results"]]
        not_existing = set(indicators).difference(existing)

        resource_post = resource_class(client=self.client, method=Resource.POST)
        resource_post.indicators_post(not_existing)
        response_post = resource_post.full_request()
        all_data = response_get["data"]["results"]
        all_data.extend(response_post["data"]["results"])
        return all_data


class ValueDelete(object):
    def __init__(self, client):
        self.client = client

    def check_delete(self, indicators, resource_class):
        resource_get = resource_class(client=self.client, method=Resource.GET)
        filter = {"value_in":indicators}
        resource_get.filter(filter)
        response_get = resource_get.full_request()
        existing = [i["id"] for i in response_get["data"]["results"]]
        for i in existing:
            resource_del = resource_class(client=self.client, method=Resource.DELETE)
            resource_del.id(i)
            resource_del.full_request()


class Source(ResourcePaged):
    def __init__(self, client:Client, method=Resource.GET):
        super(Source, self).__init__(client, method)
        self.endpoint = "sources/"
        self.request_url = '{base}{endpoint}'.format(base=self.base,
                                                     endpoint=self.endpoint)

    def source_post(self, name):
        self.json = {"name": name}


class CustomField(Resource):
    """
    abstract class
    """
    def __init__(self, client:Client, method=Resource.GET):
        super(CustomField, self).__init__(client, method)

    def col_value_put(self, id, name, value, indicator_id):
        self.request_url += str(id) + "/"
        self.json = {"name": name, "value": value,"indicator": indicator_id}

    def col_value_post(self, name, value, indicator_id):
        self.json = {"name": name, "value": value, "indicator": indicator_id}


class IndicatorNumericField(CustomField):
    def __init__(self, client:Client, method=Resource.GET):
        super(IndicatorNumericField, self).__init__(client, method)
        self.endpoint = "indicatornumericfield/"
        self.request_url = '{base}{endpoint}'.format(base=self.base,
                                                     endpoint=self.endpoint)


class IndicatorTextField(CustomField):
    def __init__(self, client:Client, method=Resource.GET):
        super(IndicatorTextField, self).__init__(client, method)
        self.endpoint = "indicatortextfield/"
        self.request_url = '{base}{endpoint}'.format(base=self.base,
                                                     endpoint=self.endpoint)


class ColumnGetPerform(object):
    def __init__(self, client):
        self.client = client

    def upsert(self, col_class,  name, value, indicator_id):
        """

        :param col_class: CustomField child class
        :param name:
        :param value:
        :param indicator_id: int
        :return:
        """
        res_get = col_class(self.client, method=Resource.GET)
        res_get.filter({"name":name, "indicator": indicator_id})
        r = res_get.full_request()
        if len(r["data"]["results"]) == 0:
            res_put = col_class(self.client, method=Resource.POST)
            res_put.col_value_post(name=name, value=value, indicator_id=indicator_id)
            res_put.full_request()

        else:
            id = r["data"]["results"][0]["id"]
            res_put = col_class(self.client, method=Resource.PUT)
            res_put.col_value_put(id=id, name=name, value=value, indicator_id=indicator_id)
            res_put.full_request()


