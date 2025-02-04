from datetime import datetime
import requests
import json
from bs4 import BeautifulSoup
from signer import *
from utils import *

session = requests.Session()
certificate, fingerprint, private_key = generate_key_pair()

def getDebugInfo(data):
    data = json.loads(data)
    status = data.get("Status", {})
    code = status.get("Code")
    message = status.get("Message")
    return code, message

def APILogin(login, password):
    
    url = "https://eduvulcan.pl/"
    response1 = session.get(url)

    url = "https://eduvulcan.pl/logowanie"
    response2 = session.get(url)

    soup = BeautifulSoup(response2.text, 'html.parser')
    token_input = soup.find('input', {'name': '__RequestVerificationToken'})
    token = {"__RequestVerificationToken": token_input['value']}

    # Combine all cookies into a single string format for the Cookie header
    cookies = {**response1.cookies.get_dict(), **response2.cookies.get_dict()}
    cookies_str = "; ".join([f"{key}={value}" for key, value in cookies.items()])
    cookies_str += f"; __RequestVerificationToken={token_input['value']}"

    # Prometheus
    url = "https://eduvulcan.pl/logowanie?ReturnUrl=%2fapi%2fap"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": cookies_str,  # Use the formatted cookies string here
        "Host": "eduvulcan.pl",
        "Origin": "https://eduvulcan.pl",
        "Referer": "https://eduvulcan.pl/logowanie?ReturnUrl=%2fapi%2fap",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Android WebView\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-G935F Build/TQ3A.230901.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.107 Mobile Safari/537.36",
        "X-Requested-With": "pl.edu.vulcan.hebe.ce",
    }

    data = {
        "Alias": login,
        "Password": password,
        "captchaUser": "",
        "__RequestVerificationToken": token_input['value'],  # Use the actual token value here
    }

    response = session.post(url, headers=headers, data=data)
    content = response.text
    cookie_jar = response.cookies.get_dict()

    soup = BeautifulSoup(content, "html.parser")
    input_element = soup.find("input", {"id": "ap"})
    value = input_element["value"]
    parsed_json = json.loads(value)

    tokens = parsed_json.get("Tokens", [])
    token = " ".join(tokens)

    return token

def JWTLogin(token, debug=False): 
    
    timestamp = datetime.now()
    date = timestamp.strftime("%a, %d %b %Y %H:%M:%S GMT") 
    tenant = get_tenant_from_jwt(token)

    url = f"https://lekcjaplus.vulcan.net.pl/{tenant}/api/mobile/register/jwt"
    
    NotificationToken = None
    RequestId = getRandomIdentifier()  # Ensure this is a value (not a function)
    
    OS = "Android"
    Certificate = certificate
    CertificateThumbprint = fingerprint
    SelfIdentifier = getRandomIdentifier()  # Ensure this is a value (not a function)
    Tokens = token
    DeviceModel = "SM-G935F"

    signerurl = url
    signerbody = None
    digest, canonical_url, signature = get_signature_values(fingerprint, private_key, signerbody, signerurl, timestamp)

    headers = {
        "accept-encoding": "gzip",
        "content-type": "application/json",
        "host": "lekcjaplus.vulcan.net.pl",
        "signature": signature,
        "user-agent": "Dart/3.3 (dart:io)",
        "vapi": "1",
        "vcanonicalurl": "api%2fmobile%2fregister%2fjwt",
        "vdate": date,
        "vos": "Android",
        "vversioncode": "640",
    }


    bodytimestamp = getCurrentTimestamp()

    body = {
        "AppName": "DzienniczekPlus 3.0",
        "AppVersion": "24.11.07 (G)",
        "NotificationToken": str(NotificationToken) if NotificationToken else None,
        "API": 1,
        "RequestId": str(RequestId),  # Ensure RequestId is serializable
        "Timestamp": bodytimestamp,
        "TimestampFormatted": date,
        "Envelope": {
            "OS": OS,
            "Certificate": Certificate,
            "CertificateType": "X509",
            "DeviceModel": DeviceModel,
            "SelfIdentifier": str(SelfIdentifier),  # Ensure serializability
            "CertificateThumbprint": CertificateThumbprint,
            "Tokens": [Tokens]
        }
    }

    body_json = json.dumps(body, indent=4)

    response = session.post(url, headers=headers, data=body_json)
    content = response.text

    if debug:
        dinfo = getDebugInfo(content)
        return content, dinfo
    
    return content

def HEBELogin(tenant, debug=False):
    url = f"https://lekcjaplus.vulcan.net.pl/{tenant}/api/mobile/register/hebe?mode=2&lastSyncDate=1970-01-01%2001%3A00%3A00"
    signerurl = f"https://lekcjaplus.vulcan.net.pl/{tenant}/api/mobile/register/hebe?mode=2&lastSyncDate=1970-01-01%2001%3A00%3A00"
    body = None
    timestamp1 = datetime.now()
    date1 = timestamp1.strftime("%a, %d %b %Y %H:%M:%S GMT")
    digest, canonical_url, signature = get_signature_values(fingerprint, private_key, body, signerurl, timestamp=timestamp1)

    headers = {
        "accept-encoding": "gzip",
        "content-type": "application/json",
        "host": "lekcjaplus.vulcan.net.pl",
        "signature": signature,
        "user-agent": "Dart/3.3 (dart:io)",
        "vapi": "1",
        "vcanonicalurl": canonical_url,
        "vdate": date1,
        "vos": "Android",
        "vversioncode": "640",
    }

    response = requests.get(url, headers=headers)
    content = response.text

    if debug:
        dinfo = getDebugInfo(content)
        return content, dinfo
    
    return content

def getLuckyNumber(tenant, schoolid, pupilid, constituentid, debug=False):
    timestamp = datetime.now()
    date = timestamp.strftime("%Y-%m-%d") 
    url = f"https://lekcjaplus.vulcan.net.pl/{tenant}/{schoolid}/api/mobile/school/lucky?pupilId={pupilid}&constituentId={constituentid}&day={date}"
    
    signerurl = url
    body = None
    date1 = timestamp.strftime("%a, %d %b %Y %H:%M:%S GMT")
    digest, canonical_url, signature = get_signature_values(fingerprint, private_key, body, signerurl, timestamp=timestamp)

    headers = {
        "accept-encoding": "gzip",
        "content-type": "application/json",
        "host": "lekcjaplus.vulcan.net.pl",
        "signature": signature,
        "user-agent": "Dart/3.3 (dart:io)",
        "vapi": "1",
        "vcanonicalurl": canonical_url,
        "vdate": date1,
        "vos": "Android",
        "vversioncode": "640",
    }

    response = requests.get(url, headers=headers)
    content = response.text

    data = json.loads(content)
    Envelope = data.get("Envelope", {})
    
    LuckyNumberDay = Envelope.get("Day", {})
    LuckyNumber = Envelope.get("Number", {})

    if debug:
        dinfo = getDebugInfo(content)
        return LuckyNumber, LuckyNumberDay, dinfo
    
    return LuckyNumber, LuckyNumberDay


def getGrades(tenant, schoolid, pupilid, unitid, periodid, debug=False):
    timestamp = datetime.now()
    date = timestamp.strftime("%Y-%m-%d") 
    url = f"https://lekcjaplus.vulcan.net.pl/{tenant}/{schoolid}/api/mobile/grade/byPupil?unitId={unitid}&pupilId={pupilid}&periodId={periodid}&lastSyncDate=1970-01-01%2001%3A00%3A00&lastId=-2147483648&pageSize=500"

    signerurl = url
    body = None
    date1 = timestamp.strftime("%a, %d %b %Y %H:%M:%S GMT")
    digest, canonical_url, signature = get_signature_values(fingerprint, private_key, body, signerurl, timestamp=timestamp)
    
    headers = {
        "accept-encoding": "gzip",
        "content-type": "application/json",
        "host": "lekcjaplus.vulcan.net.pl",
        "signature": signature,
        "user-agent": "Dart/3.3 (dart:io)",
        "vapi": "1",
        "vcanonicalurl": canonical_url,
        "vdate": date1,
        "vos": "Android",
        "vversioncode": "640",
    }

    response = requests.get(url, headers=headers)
    content = response.text


    if debug:
        dinfo = getDebugInfo(content)
        return content, dinfo

    return content

def getTimetable(tenant, schoolid, pupilid, start_date, end_date, debug=False):
    url = f"https://lekcjaplus.vulcan.net.pl/{tenant}/{schoolid}/api/mobile/schedule/withchanges/byPupil?pupilId={pupilid}&dateFrom={start_date}&dateTo={end_date}&lastId=-2147483648&pageSize=500&lastSyncDate=1970-01-01%2001%3A00%3A00"
    signerurl = url
    body = None
    date1 = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    digest, canonical_url, signature = get_signature_values(fingerprint, private_key, body, signerurl, timestamp=datetime.now())

    headers = {
        "accept-encoding": "gzip",
        "content-type": "application/json",
        "host": "lekcjaplus.vulcan.net.pl",
        "signature": signature,
        "user-agent": "Dart/3.3 (dart:io)",
        "vapi": "1",
        "vcanonicalurl": canonical_url,
        "vdate": date1,
        "vos": "Android",
        "vversioncode": "640",
    }

    response = requests.get(url, headers=headers)
    content = response.text

    if debug:
        dinfo = getDebugInfo(content)
        return content, dinfo

    return content

def getExams(tenant, schoolid, pupilid, start_date, end_date, debug=False):
    url = f"https://lekcjaplus.vulcan.net.pl/{tenant}/{schoolid}/api/mobile/exam/byPupil?pupilId={pupilid}&dateFrom={start_date}&dateTo={end_date}&lastId=-2147483648&pageSize=500&lastSyncDate=1970-01-01%2001%3A00%3A00"
    signerurl = url
    body = None
    date1 = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    digest, canonical_url, signature = get_signature_values(fingerprint, private_key, body, signerurl, timestamp=datetime.now())

    headers = {
        "accept-encoding": "gzip",
        "content-type": "application/json",
        "host": "lekcjaplus.vulcan.net.pl",
        "signature": signature,
        "user-agent": "Dart/3.3 (dart:io)",
        "vapi": "1",
        "vcanonicalurl": canonical_url,
        "vdate": date1,
        "vos": "Android",
        "vversioncode": "640",
    }

    response = requests.get(url, headers=headers)
    content = response.text

    if debug:
        dinfo = getDebugInfo(content)
        return content, dinfo

    return content
