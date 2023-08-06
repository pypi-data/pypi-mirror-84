import unittest
import os
from intstreamsdk.client import SyncClient, AsyncClient
from intstreamsdk.resource import (MD5, SHA1, SHA256, NetLoc,
                                    IPV6, IPV4, Email,
                                   Resource, DomainExtractor, DomainLoader)


class IntegrationAsync(unittest.TestCase):
    def setUp(self):
        username = os.environ.get("TESTUSER", "")
        password = os.environ.get("TESTPASSWORD", "")
        server = os.environ.get("TESTSERVER", "http://127.0.0.1:8000")
        self.client = AsyncClient(username=username,
                            password=password,
                            server_url=server)

    def test_md5_resource(self):
        # get ind
        ind = "0800fc577294c34e0b28ad2839435945"
        res = MD5(client=self.client, method=Resource.GET)
        res.indicators_post([ind])
        result = res.full_request(raise_exc=True)
        length = len(result.get("data", {}).get("results",[]))
        # if exists delete
        if result["status"] == "SUCCESS"and length == 1:
            id = result.get("data", {}).get("results",[])[0]["id"]
            res = MD5(client=self.client, method=Resource.DELETE)
            res.id(id)
            # could do multiple full requests here and they will async
            r = res.request()
            # collect multiple responses
            result = res.response(r)
            self.assertEqual(result["status"], "SUCCESS")
        # create
        res = MD5(client=self.client, method=Resource.POST)
        res.indicators_post([ind])
        result = res.full_request(raise_exc=True)
        self.assertEqual(result["status"], "SUCCESS")


class IntegrationSync(unittest.TestCase):

    def setUp(self):
        username = os.environ.get("TESTUSER", "")
        password = os.environ.get("TESTPASSWORD", "")
        server = os.environ.get("TESTSERVER", "http://127.0.0.1:8000")
        self.client = SyncClient(username=username,
                            password=password,
                            server_url=server)

    def test_email(self):
        ind = "test@testing.com"
        self._delete_update(Email, ind)

    def _delete_update(self, resource_class, ind):
        res = resource_class(client=self.client, method=Resource.GET)
        res.indicators_post([ind])
        result = res.full_request(raise_exc=True)
        length = len(result.get("data", {}).get("results",[]))
        # if exists delete
        if result["status"] == "SUCCESS"and length == 1:
            id = result.get("data", {}).get("results",[])[0]["id"]
            res = resource_class(client=self.client, method=Resource.DELETE)
            res.id(id)
            result = res.full_request(raise_exc=True)
            self.assertEqual(result["status"], "SUCCESS")
        # create indicator
        res = resource_class(client=self.client, method=Resource.POST)
        res.indicators_post([ind])
        result = res.full_request(raise_exc=True)
        self.assertEqual(result["status"], "SUCCESS")

    def test_ipv4(self):
        ind = "1.1.1.1"
        self._delete_update(IPV4, ind)

    def test_ipv6(self):
        ind = "2607:f0d0:1002:0051:0000:0000:0000:0004"
        self._delete_update(IPV6, ind)

    def test_md5_resource(self):
        # get indicator
        ind = "0800fc577294c34e0b28ad2839435945"
        self._delete_update(MD5, ind)

    def test_sha256_resource(self):
        # get indicator
        ind = "b1bb0b49069db3871451654efb038e9674ca2595d665c9fc6b5c65e54c5f76cb"
        self._delete_update(SHA256, ind)

    def test_sha1_resource(self):
        # get indicator
        ind = "2346ad27d7568ba9896f1b7da6b5991251debdf2"
        self._delete_update(SHA1, ind)

    def test_domain(self):
        dom1 = "test.com"
        dom2 = "testing.com"
        ind = [dom1, dom2]
        # upload urls
        uploader = DomainLoader(ind, self.client)
        r = uploader.upload()
        
        # verify dom1 in database
        extractor = DomainExtractor(dom1, self.client)
        resource_net_loc = NetLoc(client=self.client, method=Resource.GET)
        filter = {
            "suffix": extractor.net_loc.suffix_id,
            "domain": extractor.net_loc.domain,
            "subdomain": extractor.net_loc.subdomain
        }
        resource_net_loc.filter(filter=filter)
        r = resource_net_loc.full_request()
        self.assertEqual(r["data"]["count"], 1)

        # delete
        uploader.delete()
        r = resource_net_loc.full_request()
        self.assertEqual(r["status"], Resource.SUCCESS)


if __name__ == "__main__":
    unittest.main()





