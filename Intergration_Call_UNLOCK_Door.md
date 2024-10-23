**Call API kích hoạt nút mở cửa**\n
#Bước 1: Sử dụng thông tin đăng nhập để lấy được Token\n
##Request:\n
```
GET /ASWeb/WebService.srf?action=LOGIN&username=admin&password=Dev@1234 HTTP/1.1
Host: localhost
Cache-Control: max-age=0
Sec-Ch-Ua: "Chromium";v="129", "Not=A?Brand";v="8"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
Connection: keep-alive
```
\n
##Response:\n
```
HTTP/1.0 200 OK
Date: Wed, 23 Oct 2024 03:49:49 GMT
Server: GeoWebServer
Allow: GET, POST, HEAD
Access-Control-Allow-Origin:*

{ "success": 1, "token": "DF4CBA19C7AE4f5bA53FCE740A834770", "version": "6.0.2.0" }
```

#Bước 2: Sử dụng Token để tiếp tục lấy thông tin client_guid
##Request:
```
GET /ASWeb/WebService.srf?token=DF4CBA19C7AE4f5bA53FCE740A834770&module=monitor&action=WEBCLIENT_LOGIN&login=1
Host: localhost
Cache-Control: max-age=0
Sec-Ch-Ua: "Chromium";v="129", "Not=A?Brand";v="8"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
Connection: keep-alive
```
\n
##Response:\n
```
HTTP/1.0 200 OK
Date: Wed, 23 Oct 2024 04:01:35 GMT
Server: GeoWebServer
Allow: GET, POST, HEAD
Connection: Keep-Alive
Content-Type: text/html
Access-Control-Allow-Origin: *
Content-Length: 118

{"client_guid":"8B81519A-DF4C-4b95-94A9-9707048877BF","host_guid":"A14E2EF2-D22C-4172-8753-8E7A389B8083","success":1}
```
\n
#Bước 3: Sử dụng kết hợp giữa thông tin Token và client_guid để tiến hành gọi API kích hoạt mở cửa:\n
##Request:\n
```
POST /ASWeb/WebService.srf HTTP/1.1
Host: 192.168.10.41
User-Agent: python-requests/2.32.3
Accept-Encoding: gzip, deflate, br
Accept: */*
Connection: keep-alive
Content-Length: 176
Content-Type: application/x-www-form-urlencoded

action=DOOR_OPERATION&token=DF4CBA19C7AE4f5bA53FCE740A834770&client_guid=8B81519A-DF4C-4b95-94A9-9707048877BF&module=monitor&dvg_id=-1&ctrl_id=-1&dr_id=-1&operation=UNLOCK_DOOR
```
\n
##Response:\n
```
POST /ASWeb/WebService.srf HTTP/1.1
Host: 192.168.10.41
User-Agent: python-requests/2.32.3
Accept-Encoding: gzip, deflate, br
Accept: */*
Connection: keep-alive
Content-Length: 176
Content-Type: application/x-www-form-urlencoded

action=DOOR_OPERATION&token=DF4CBA19C7AE4f5bA53FCE740A834770&client_guid=8B81519A-DF4C-4b95-94A9-9707048877BF&module=monitor&dvg_id=-1&ctrl_id=-1&dr_id=-1&operation=UNLOCK_DOOR
```
\n
