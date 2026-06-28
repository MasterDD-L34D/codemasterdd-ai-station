import importlib.util
from pathlib import Path
import pytest

_spec = importlib.util.spec_from_file_location(
    "atomize_mod", Path(__file__).resolve().parent / "atomize.py"
)
atomize_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(atomize_mod)
message_to_text = atomize_mod.message_to_text

def test_visually_hidden():
    msg = {
        "content": {"content_type": "text", "parts": ["hello"]},
        "metadata": {"is_visually_hidden_from_conversation": True}
    }
    assert message_to_text(msg) == ""

def test_empty_message():
    assert message_to_text({}) == ""
    assert message_to_text({"content": {}}) == ""
    assert message_to_text({"content": {"content_type": "unknown_type"}}) == ""

def test_text_content_type():
    msg = {
        "content": {
            "content_type": "text",
            "parts": ["hello", {"dict": "ignored"}, "world"]
        }
    }
    assert message_to_text(msg) == "hello\nworld"

def test_code_content_type():
    msg = {
        "content": {
            "content_type": "code",
            "text": "print('hello world')"
        }
    }
    assert message_to_text(msg) == "```\nprint('hello world')\n```"

    msg_no_text = {
        "content": {
            "content_type": "code"
        }
    }
    assert message_to_text(msg_no_text) == "```\n\n```"

def test_multimodal_text():
    msg = {
        "content": {
            "content_type": "multimodal_text",
            "parts": [
                "some text",
                {"content_type": "image_asset_pointer", "asset_pointer": "sediment://abc-123"},
                {"content_type": "image_asset_pointer", "asset_pointer": "file-service://def-456"},
                {"content_type": "other"}
            ]
        }
    }
    expected = "some text\n![image: abc-123]\n![image: def-456]"
    assert message_to_text(msg) == expected

def test_thoughts():
    msg = {
        "content": {
            "content_type": "thoughts",
            "parts": ["thinking...", "more thoughts"]
        }
    }
    expected = "<details>\n<summary>Thinking</summary>\n\nthinking...\nmore thoughts\n\n</details>"
    assert message_to_text(msg) == expected

    msg_empty = {
        "content": {
            "content_type": "thoughts",
            "parts": ["   "]
        }
    }
    assert message_to_text(msg_empty) == ""

def test_reasoning_recap():
    msg = {
        "content": {
            "content_type": "reasoning_recap",
            "parts": ["recap one", "recap two"]
        }
    }
    expected = "*Reasoning recap: recap one\nrecap two*"
    assert message_to_text(msg) == expected

    msg_empty = {
        "content": {
            "content_type": "reasoning_recap",
            "parts": []
        }
    }
    assert message_to_text(msg_empty) == ""

def test_tether_browsing_display():
    msg = {
        "content": {
            "content_type": "tether_browsing_display",
            "parts": ["result one", "result two"]
        }
    }
    expected = "> **Browsing Result:** result one\nresult two"
    assert message_to_text(msg) == expected

    msg_empty = {
        "content": {
            "content_type": "tether_browsing_display",
            "parts": [""]
        }
    }
    assert message_to_text(msg_empty) == ""

def test_model_editable_context():
    msg = {
        "content": {
            "content_type": "model_editable_context",
            "parts": ["should be ignored"]
        }
    }
    assert message_to_text(msg) == ""
