import base64
import sys
import importlib.util
from pathlib import Path

# Load LangfuseClient from module with dashed name
spec = importlib.util.spec_from_file_location("langfuse_client", str(Path(__file__).parent.parent / "langfuse_client.py"))
langfuse_module = importlib.util.module_from_spec(spec)
sys.modules["langfuse_client"] = langfuse_module
spec.loader.exec_module(langfuse_module)
LangfuseClient = langfuse_module.LangfuseClient

def test_auth_header_valid_keys():
    client = LangfuseClient(host="http://localhost", public_key="test_pub", secret_key="test_sec")
    expected_token = base64.b64encode(b"test_pub:test_sec").decode("ascii")
    expected_header = {"Authorization": f"Basic {expected_token}"}
    assert client._auth_header() == expected_header

def test_auth_header_missing_keys():
    client = LangfuseClient(host="http://localhost", public_key="", secret_key="")
    assert client._auth_header() == {}

def test_auth_header_partial_keys():
    client1 = LangfuseClient(host="http://localhost", public_key="test_pub", secret_key="")
    assert client1._auth_header() == {}

    client2 = LangfuseClient(host="http://localhost", public_key="", secret_key="test_sec")
    assert client2._auth_header() == {}
