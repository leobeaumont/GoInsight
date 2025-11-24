import requests
import pytest

MODEL_URL = "https://github.com/lightvector/KataGo/releases/download/v1.16.3/katago-v1.16.3-eigen-linux-x64.zip"
NEURALNET_URL = "https://katagoarchive.org/g170/neuralnets/g170e-b10c128-s1141046784-d204142634.bin.gz"

@pytest.mark.parametrize("url", [MODEL_URL, NEURALNET_URL])
def test_url_accessible(url):
    """
    Test that the file at URL is reachable and returns a valid response.
    """
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
    except requests.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    assert response.status_code == 200, f"Unexpected status: {response.status_code}"
