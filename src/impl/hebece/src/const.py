from impl.hebece.src.utils import *
# Endpoints

JWT = "/api/mobile/register/jwt"
HEBE = "/api/mobile/register/hebe"
LUCKY = "/api/mobile/school/lucky"
GRADES = "/api/mobile/grade/byPupil"
TIMETABLE = "/api/mobile/schedule/withchanges/byPupil"
EXAMS = "/api/mobile/exam/byPupil"

# Header
DEVICE = "SM-G935F"
DEVICE_OS = "Android"
APPVERSION = "24.11.07 (G)"

def makeHeader(signature, canonical_url):
    return {
        "accept-encoding": "gzip",
        "content-type": "application/json",
        "host": "lekcjaplus.vulcan.net.pl",
        "signature": signature,
        "user-agent": "Dart/3.3 (dart:io)",
        "vapi": "1",
        "vcanonicalurl": canonical_url,
        "vdate": getDate(),
        "vos": DEVICE_OS,
        "vversioncode": "640",
    }
    
def makeLoginHeader(cookies):
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": cookies,
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