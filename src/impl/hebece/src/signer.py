import cryptography
import re
import urllib
import base64
from OpenSSL import crypto
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_der_private_key
from cryptography.hazmat.backends import default_backend


def get_encoded_path(full_url):
    path = re.search(r"(api/mobile/.+)", full_url)
    if path is None:
        raise ValueError(
            "The URL does not seem correct (does not match `(api/mobile/.+)` regex)"
        )
    return urllib.parse.quote(path[1], safe="").lower()

def get_digest(body):
    if not body:
        return None

    m = hashlib.sha256()
    m.update(bytes(body, "utf-8"))
    return base64.b64encode(m.digest()).decode("utf-8")

def get_headers_list(body, digest, canonical_url, timestamp):
    sign_data = [
        ["vCanonicalUrl", canonical_url],
        ["Digest", digest] if body else None,
        ["vDate", timestamp.strftime("%a, %d %b %Y %H:%M:%S GMT")],
    ]

    return (
        " ".join(item[0] for item in sign_data if item),
        "".join(item[1] for item in sign_data if item),
    )

def get_signature(data, private_key):
    # Convert data to a string representatio
    data_str = (
        json.dumps(data)
        if isinstance(data, (dict, list))
        else str(data)
    )
    
    # Decode the base64 private key and load it
    private_key_bytes = base64.b64decode(private_key)
    pkcs8_key = load_der_private_key(private_key_bytes, password=None, backend=default_backend())
    
    # Sign the data
    signature = pkcs8_key.sign(
        bytes(data_str, "utf-8"),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    
    # Encode the signature in base64 and return
    return base64.b64encode(signature).decode("utf-8")

def get_signature_values(fingerprint, private_key, body, full_url, timestamp):
    canonical_url = get_encoded_path(full_url)
    digest = get_digest(body)
    headers, values = get_headers_list(body, digest, canonical_url, timestamp)
    signature = get_signature(values, private_key)

    return (
        "SHA-256={}".format(digest) if digest else None,
        canonical_url,
        'keyId="{}",headers="{}",algorithm="sha256withrsa",signature=Base64(SHA256withRSA({}))'.format(
            fingerprint, headers, signature
        ),
    )

def pem_getraw(pem):
    return pem.decode("utf-8").replace("\n", "").split("-----")[2]

def generate_key_pair():
    pkcs8 = crypto.PKey()
    pkcs8.generate_key(crypto.TYPE_RSA, 2048)

    x509 = crypto.X509()
    x509.set_version(2)
    x509.set_serial_number(1)
    subject = x509.get_subject()
    subject.CN = "APP_CERTIFICATE CA Certificate"
    x509.set_issuer(subject)
    x509.set_pubkey(pkcs8)
    x509.sign(pkcs8, "sha256")
    x509.gmtime_adj_notBefore(0)
    x509.gmtime_adj_notAfter(20 * 365 * 24 * 60 * 60)

    certificate = pem_getraw(crypto.dump_certificate(crypto.FILETYPE_PEM, x509))
    fingerprint = x509.digest("sha1").decode("utf-8").replace(":", "").lower()
    private_key = pem_getraw(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkcs8))

    return certificate, fingerprint, private_key
