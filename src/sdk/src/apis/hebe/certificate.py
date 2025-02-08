from pydantic import BaseModel
from sdk.src.apis.hebe.signer import generate_key_pair


class Certificate(BaseModel):
    certificate: str
    fingerprint: str
    private_key: str
    type: str

    @staticmethod
    def generate():
        certificate, fingerprint, private_key = generate_key_pair()
        return Certificate(certificate=certificate, fingerprint=fingerprint, private_key=private_key, type="X509")
