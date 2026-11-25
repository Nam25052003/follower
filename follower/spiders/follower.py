import scrapy
import time, random
from urllib.parse import urlencode
from follower.sign import xdynosaur
from follower.utils.ua_lib import UserAgentService

class FollowerSpider(scrapy.Spider):
    name = "follower"

    def __init__(self, name = None, **kwargs):
        super().__init__(name, **kwargs)

        self.base_url = "https://www.tiktok.com/api/user/list/?"
        self.ua_service = UserAgentService()
        self.ms_token = "AA-WE3BapeOZjweCZWdihAA9YOce9aXzIBvxo61eea6wNuGdIiLSen5rab0zOuvq4wc_vBWFAvAsqtl0VcfC2iq-8p7KR9WqZkr4QiIOHm_pBEzOmuO6OlS9LyQN5L2BMIUS4bcig3aPlMoIRYPkoq68TO0eDKnB1k_-wj8="
        self.sec_uid = "MS4wLjABAAAAnzMceaKFmIiFjPATOgBca-yBjSPAWvhgKVQMFRHSyAQUfEi_KLRVlPEKW6c2cYcn"

    def errback(self, failure):
        self.logger.error(repr(failure))

    def sign_dyno(self, param, ua):
        dyno = xdynosaur.encrypt(qs=param, body="", ua=ua)
        return dyno

    def start_requests(self):
        target = self.ua_service.target_random()

        print("Browser =", target)

        yield self.make_list_request(
            target=target,
            min_cursor=0,
        )


    def make_list_request(self, target, min_cursor=0):
        ua = self.ua_service.get_user_agent(target)

        qs = self.parse_param(
            sec_uid=self.sec_uid,
            target=target,
            min_cursor=min_cursor,
        )

        dyno = self.sign_dyno(
            param=qs,
            ua=ua,
        )

        headers_mod = {
            "Accept": "*/*",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": "https://www.tiktok.com",
            "Referer": "https://www.tiktok.com/",
        }

        fn_url = (
            self.base_url
            + qs
            + "&X-Dynosaur=" + dyno
            + "&msToken=" + self.ms_token
        )

        return scrapy.Request(
            url=fn_url,
            method="GET",
            headers=headers_mod,
            callback=self.parse,
            errback=self.errback,
            meta={
                "curl_cffi_options": {
                    "impersonate": target,
                },
                "target": target,
                "min_cursor": min_cursor,
            },
            dont_filter=True,
        )


    def parse(self, response):
        try:
            data = response.json()
        except Exception as e:
            self.logger.error(
                "Failed to parse JSON: %s",
                e,
            )
            return

        status_code = data.get("statusCode")

        if status_code != 0:
            self.logger.error(
                "TikTok API error: %s",
                data.get("status_msg"),
            )
            return

        user_list = data.get("userList", [])

        self.logger.info(
            "Received %s users | Total: %s",
            len(user_list),
            data.get("total"),
        )

        # Process current page
        for item in user_list:
            yield item

        # Pagination
        has_more = data.get("hasMore", False)
        next_cursor = data.get("minCursor", 0)

        current_cursor = response.meta.get("min_cursor", 0)

        if has_more and next_cursor and next_cursor != current_cursor:

            self.logger.info(
                "Next page: minCursor=%s",
                next_cursor,
            )

            yield self.make_list_request(
                target=response.meta["target"],
                min_cursor=next_cursor,
            )

        else:
            self.logger.info(
                "Pagination completed. Total=%s",
                data.get("total"),
            )


    def parse_param(self, sec_uid, target, min_cursor=0):
        metadata = self.ua_service.get_browser_metadata(target)

        now = int(time.time())

        device_id = (
            7472955720000000000
            + random.randint(10000000000, 100000000000)
        )

        scene = 67

        params = {
            "WebIdLastTime": now,
            "aid": 1988,
            "app_language": "en",
            "app_name": "tiktok_web",
            "browser_language": "en-US",
            "browser_name": metadata["browser_name"],
            "browser_online": "true",
            "browser_platform": metadata["browser_platform"],
            "browser_version": metadata["browser_version"],
            "channel": "tiktok_web",
            "cookie_enabled": "true",
            "count": 30,
            "data_collection_enabled": "true",
            "device_id": device_id,
            "device_platform": metadata["device_platform"],
            "focus_state": "true",
            "from_page": "user",
            "history_len": 2,
            "is_fullscreen": "false",
            "is_page_visible": "true",
            "maxCursor": 0,
            "minCursor": min_cursor,
            "odinId": "6768452196390388738",
            "os": metadata["os"],
            "priority_region": "VN",
            "referer": "https://www.tiktok.com/",
            "region": "VN",
            "root_referer": "https://www.tiktok.com/",
            "scene": scene,
            "screen_height": 1200,
            "screen_width": 1920,
            "secUid": sec_uid,
            "tz_name": "Asia/Saigon",
            "user_is_login": "false",
            "webcast_language": "en",
        }

        return urlencode(params)
