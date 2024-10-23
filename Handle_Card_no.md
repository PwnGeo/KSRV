# Sử dụng request bên dưới để tra cứu thông tin hồ sơ đã tạo trong hệ thống:

```
GET /enroll/getFaceList.php HTTP/1.1
Host: localhost:81
sec-ch-ua-platform: "Windows"
X-Requested-With: XMLHttpRequest
Accept-Language: en-US,en;q=0.9
Accept: application/json, text/javascript, */*; q=0.01
sec-ch-ua: "Chromium";v="129", "Not=A?Brand";v="8"
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Safari/537.36
sec-ch-ua-mobile: ?0
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:81/enroll/Enroll.php
Accept-Encoding: gzip, deflate, br
Cookie: PHPSESSID=36facc11a4bad936efc5478015a2b4c0
Connection: keep-alive
```


# Kết quả phản hồi từ Server AI FR:
```
HTTP/1.1 200 OK
Date: Wed, 23 Oct 2024 10:15:15 GMT
Server: Apache
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Content-Length: 2267
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: application/json

{"draw":0,"recordsTotal":"11","recordsFiltered":"11","data":[{"serial":0,"face_uuid":"e7c0b136-d4d0-470a-8c9a-970bc7d75b4b","group":"Unauthorized","id":"060097009192","id2":"Nam","name":"L\u00ea Minh Thanh","cardno":"001-00019","pic_hash":"eb3121cc737e162d0d650f0225140d29"},{"serial":1,"face_uuid":"204674ec-5dda-4813-b85e-4b6db6c0e4e4","group":"Kh\u00e1ch","id":"068078007031","id2":"Nam","name":"Nghi\u00eam S\u1ef9 Th\u1eafng","cardno":"001-00018","pic_hash":"0deaa300e87592984c1b849541402f58"},{"serial":2,"face_uuid":"653ea167-bf1e-40be-a7a5-5c9521150c2e","group":"Kh\u00e1ch","id":"060097009192","id2":"Nam","name":"L\u00ea Minh Thanh","cardno":"001-00012","pic_hash":"36bfb58689ab4b99c917ebb325b39869"},{"serial":3,"face_uuid":"62d103a7-ee06-4580-ac49-e929d69701ae","group":"Kh\u00e1ch","id":"060097009192","id2":"Nam","name":"L\u00ea Minh Thanh","cardno":"001-00010","pic_hash":"26263167d243c3728893749269854636"},{"serial":4,"face_uuid":"ee20540d-9d17-4a4f-a66b-d75c2f4085fe","group":"C\u00e1n b\u1ed9 C06","id":"068078007031","id2":"Nam","name":"Nghi\u00eam S\u1ef9 Th\u1eafng","cardno":"001-00008","pic_hash":"1ea55f730c13d6898129359ff2074c55"},{"serial":5,"face_uuid":"72e6d895-72d2-4cda-bb90-485d904963d7","group":"Kh\u00e1ch","id":"068078007031","id2":"Nam","name":"Nghi\u00eam S\u1ef9 Th\u1eafng","cardno":"001-00007","pic_hash":"7cbb0c7a61f3899852c6ec3d94fe3f72"},{"serial":6,"face_uuid":"b60704ac-bc2d-44ea-b7dd-81184acadf17","group":"Kh\u00e1ch","id":"068078007031","id2":"Nam","name":"Nghi\u00eam S\u1ef9 Th\u1eafng","cardno":"001-00006","pic_hash":"29c8e37a1680c39dc367f447fb5f4421"},{"serial":7,"face_uuid":"2dc8e2bf-5bec-440d-b072-406fbcb6f965","group":"Kh\u00e1ch","id":"060097009192","id2":"Nam","name":"L\u00ea Minh Thanh","cardno":"001-00005","pic_hash":"9fad28cfe50b1118fa2ba00c5236fe40"},{"serial":8,"face_uuid":"b680cc29-fecf-4ded-9b72-008af7d187e5","group":"Kh\u00e1ch","id":"060097009192","id2":"Nam","name":"L\u00ea Minh Thanh","cardno":"001-00004","pic_hash":"a1781220123f7084ab4861518ae4feea"},{"serial":9,"face_uuid":"1b1bcc2a-99f6-40dd-b1ec-9dcfb088df84","group":"Unauthorized","id":"068078007031","id2":"Nam","name":"Nghi\u00eam S\u1ef9 Th\u1eafng","cardno":"001-00003","pic_hash":"4a4bde604ed3aa6262afd2dff6485161"}],"error":""}
``` 
