# REST API example application

Сервис, в котором котором можно увидеть справочники, созданные администрацией,
а также элементы в них.

# REST API

REST API к этому сервису описано ниже.

## Get list of Handbooks
    Возвращает список всех версий всех справочников.

### Request

`GET /handbooks/`

    http GET http://localhost:8000/api/handbooks/

### Response

    HTTP/1.1 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    Content-Length: 955
    Content-Type: application/json
    Cross-Origin-Opener-Policy: same-origin
    Date: Tue, 21 Jun 2022 11:54:15 GMT
    Referrer-Policy: same-origin
    Server: WSGIServer/0.2 CPython/3.9.0
    Vary: Accept, Cookie
    X-Content-Type-Options: nosniff
    X-Frame-Options: DENY
    
    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "begin_date": "2022-06-15",
                "description": "asd",
                "identifier": "5c25bdda-ef0d-11ec-8ea0-0242ac120002",
                "short_title": "asd",
                "title": "asd",
                "version": "1"
            },
            {
                "begin_date": "2022-05-03",
                "description": "Старые кошки",
                "identifier": "00000000-0000-0000-0000-000000000001",
                "short_title": "Кошки",
                "title": "Кошки и коты",
                "version": "0"
            }
        ]
    {


## Get list of handbooks relevant on a specific date
    Возвращает список справочников, актуальных на указанную дату.

### Request

`GET /up_to_date/?date=date`

    http GET http://localhost:8000/api/handbooks/up_to_date/?date=2022-06-09


### Response
    
    HTTP/1.1 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Length: 208
    Content-Type: application/json
    Cross-Origin-Opener-Policy: same-origin
    Date: Tue, 21 Jun 2022 12:00:34 GMT
    Referrer-Policy: same-origin
    Server: WSGIServer/0.2 CPython/3.9.0
    Vary: Accept, Cookie
    X-Content-Type-Options: nosniff
    X-Frame-Options: DENY
    
    [
        {
            "begin_date": "2022-06-08",
            "description": "Справочник о кошках",
            "identifier": "00000000-0000-0000-0000-000000000001",
            "short_title": "Кошки",
            "title": "Кошки и коты",
            "version": "1"
        }
    ]


## Get a list of elements of relevant version of a specific handbook
    Возвращает список элементов актуальной версии указанного справочника.

### Request

`GET /elements/get_by_handbook/?handbook_identifier=UUID`

    http GET http://localhost:8000/api/elements/get_by_handbook/?handbook_identifier=00000000-0000-0000-0000-000000000001

### Response

    HTTP/1.1 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Length: 1432
    Content-Type: application/json
    Cross-Origin-Opener-Policy: same-origin
    Date: Tue, 21 Jun 2022 12:05:28 GMT
    Referrer-Policy: same-origin
    Server: WSGIServer/0.2 CPython/3.9.0
    Vary: Accept, Cookie
    X-Content-Type-Options: nosniff
    X-Frame-Options: DENY
    
    [
        {
            "code": "5997",
            "handbook": "http://localhost:8000/api/handbooks/1/",
            "id": 11,
            "parent_identifier": "00000000-0000-0000-0000-000000000001",
            "value": "Бенга"
        },
        {
            "code": "5997",
            "handbook": "http://localhost:8000/api/handbooks/1/",
            "id": 10,
            "parent_identifier": "00000000-0000-0000-0000-000000000001",
            "value": "Бенгальский тигр"
        }
    ]


## Validate values by a relevant version of a specific handbook
    Возвращает словарь, в котором для каждого переданного слова указывает,
    является ли это слово элементом актуальной версии указанного справочника.

### Request

`GET /elements/validate_by_handbook/?handbook_identifier=UUID&q1=WORD&q2=WORD`

    http GET http://localhost:8000/api/elements/validate_by_handbook/ handbook_identifier==00000000-0000-0000-0000-000000000001 q1==Тигр q2==Лев

### Response

    HTTP/1.1 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Length: 32
    Content-Type: application/json
    Cross-Origin-Opener-Policy: same-origin
    Date: Tue, 21 Jun 2022 12:11:27 GMT
    Referrer-Policy: same-origin
    Server: WSGIServer/0.2 CPython/3.9.0
    Vary: Accept, Cookie
    X-Content-Type-Options: nosniff
    X-Frame-Options: DENY
    
    {
        "Лев": false,
        "Тигр": true
    }

## Get a list of elements of a specific version of a specific handbook
    
    Возвращает список элементов указанной версии указанного справочника
    
    Если версия не указана, поведение совпадает с get_by_handbook

### Request

`GET /get_by_handbook_version/handbook_identifier=UUID&handbook_version=VERSION`

    http GET http://localhost:8000/api/elements/get_by_handbook_version/ handbook_identifier==00000000-0000-0000-0000-000000000001 handbook_version==0

### Response

    HTTP/1.1 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Length: 172
    Content-Type: application/json
    Cross-Origin-Opener-Policy: same-origin
    Date: Tue, 21 Jun 2022 12:31:53 GMT
    Referrer-Policy: same-origin
    Server: WSGIServer/0.2 CPython/3.9.0
    Vary: Accept, Cookie
    X-Content-Type-Options: nosniff
    X-Frame-Options: DENY
    
    [
        {
            "code": "фывфывф",
            "handbook": "http://localhost:8000/api/handbooks/6/",
            "id": 3,
            "parent_identifier": "00000000-0000-0000-0000-000000000001",
            "value": "Саблезуб"
        }
    ]


## Validate values by a specific version of a specific handbook 
    Возвращает словарь, в котором для каждого переданного слова указывает,
    является ли это слово элементом указанной версии указанного справочника.
    
    Если версия не указана, поведение совпадает с validate_by_handbook

### Request

`POST /validate_by_handbook_version/handbook_identifier=UUID&q1=WORD&...&handbook_version=VERSION`

    http GET http://localhost:8000/api/elements/validate_by_handbook_version/ handbook_identifier==00000000-0000-0000-0000-000000000001 q1==Тигр q2==Лев handbook_version==0

### Response

    HTTP/1.1 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Length: 33
    Content-Type: application/json
    Cross-Origin-Opener-Policy: same-origin
    Date: Tue, 21 Jun 2022 12:24:42 GMT
    Referrer-Policy: same-origin
    Server: WSGIServer/0.2 CPython/3.9.0
    Vary: Accept, Cookie
    X-Content-Type-Options: nosniff
    X-Frame-Options: DENY
    
    {
        "Лев": false,
        "Тигр": false
    }
