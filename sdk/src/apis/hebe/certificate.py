from dataclasses import dataclass
from sdk.src.apis.hebe.signer import generate_key_pair


@dataclass
class Certificate:
    certificate: str
    fingerprint: str
    private_key: str
    type: str

    @staticmethod
    def generate():
        certificate, fingerprint, private_key = generate_key_pair()
        return Certificate(certificate, fingerprint, private_key, "X509")
