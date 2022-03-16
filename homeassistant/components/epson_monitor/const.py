"""Constants for the epson integration."""

DOMAIN = "epson_monitor"
SERVICE_SELECT_CMODE = "select_cmode"

ATTR_CMODE = "cmode"
HTTP = "http"

#URL = "http://10.129.101.4:8123/api/states/switch.pei_xun_shi_tou_ying_ji_dian_yuan_socket_1"
URL = "http://10.129.101.4:8123/api/states/switch.15ceng_pei_xun_shi_wi_fizhi_neng_liu_kong_ji_liang_pai_cha_socket_3"

HEADERS = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIxN2Q0ZGU3YTI5MDU0NDA2ODllYjNlMzczNGFkNTNhZCIsImlhdCI6MTY0NDMwMDA4OSwiZXhwIjoxOTU5NjYwMDg5fQ.70V-dsBRPvD07YIIuHwDzhZPz2-VKMdvFdI0bQEUYcU",
    "content-type": "application/json",
}
REQUEST_TIMEOUT = 6  # In seconds; argument to asyncio.timeout
