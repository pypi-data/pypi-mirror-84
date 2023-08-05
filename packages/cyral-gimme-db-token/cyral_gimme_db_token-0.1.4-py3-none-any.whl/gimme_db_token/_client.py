import json
import sys
import webbrowser

import requests


def browser_authenticate(tenant, public_key):
    url = f"https://{tenant}.cyral.com/app/cli/{public_key}"
    webbrowser.open(url)
    print("Please continue the authentication in the opened browser window.")
    print(
        "If the window didn't automatically start, please open the following URL in \
your browser:"
    )
    print(url)


def poll_opaque_token_service(tenant, public_key, timeout):
    time_before_retry = 1  # in seconds
    num_retries = int(timeout / time_before_retry)
    url = f"https://{tenant}.cyral.com:8000/v1/opaqueToken/tokens/{public_key}"
    success = False
    for _ in range(num_retries):
        try:
            r = requests.get(url, timeout=time_before_retry)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            continue
        if r.status_code == 200:
            success = True
            break
    if not success:
        print(
            "Unable to retrieve DB token. Please try again or contact Cyral \
Support"
        )
        sys.exit(1)
    return json.loads(r.text)
