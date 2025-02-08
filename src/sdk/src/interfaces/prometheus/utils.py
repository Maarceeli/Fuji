import base64
import json

from sdk.src.apis.hebe.student import HebePeriod


def parse_jwt_payload(token: str):
    # Split the JWT into parts
    _, payload, _ = token.split(".")

    # Decode the payload from Base64
    # Add padding
    payload += "=" * (-len(payload) % 4)
    decoded_payload = base64.urlsafe_b64decode(payload).decode("utf-8")

    # Parse the payload as JSON
    payload_json = json.loads(decoded_payload)
    return payload_json


def get_hebe_url(symbol: str, unit_symbol: str | None = None):
    return f"https://lekcjaplus.vulcan.net.pl/{symbol}{'/' + unit_symbol if unit_symbol else ''}/api"


def get_context_periods_from_hebe_periods(hebe_periods: list[HebePeriod]):
    periods = {}
    for period in hebe_periods:
        periods[period.number] = period.id
    return periods


def flat_map(list: list[list]):
    new = []
    for sublist in list:
        [new.append(item) for item in sublist]
    return new
