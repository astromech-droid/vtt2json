import os
import json
from vtt2json.vtt2json import to_json

SUBTITLES_DIR = os.path.join(os.path.dirname(__file__), "subtitles")


def get_file(filename):
    return os.path.join(SUBTITLES_DIR, filename)


def test_ignore_lines():
    expected_value = {
        "parsed_lines": [],
        "ignored_lines": [
            "WEBVTT\n",
            "\n",
            "STYLE\n",
            "::cue() {\n",
            "  font-family: Arial, Helvetica, sans-serif;\n",
            "}\n",
        ],
    }
    parsed_value = to_json(get_file("ignore_lines.vtt"))

    assert parsed_value == json.dumps(expected_value)


def test_regular_lines():
    expected_value = {
        "parsed_lines": [
            {
                "start": "00:00:01.960",
                "end": "00:00:03.795",
                "text": "CLAIRE: Kids! Breakfast!",
                "_raw_text": "CLAIRE: Kids! Breakfast!",
            }
        ],
        "ignored_lines": [],
    }
    parsed_value = to_json(get_file("regular_lines.vtt"))

    assert parsed_value == json.dumps(expected_value)


def test_multiple_lines():
    expected_value = {
        "parsed_lines": [
            {
                "start": "00:00:22.231",
                "end": "00:00:25.526",
                "text": "All right, that's not gonna happen.\n",
                "_raw_text": "All right, that's not gonna happen.\n",
            },
            {
                "start": "00:00:22.231",
                "end": "00:00:25.526",
                "text": "And, wow, you're not wearing that outfit.",
                "_raw_text": "And, wow, you're not wearing that outfit.",
            },
        ],
        "ignored_lines": [],
    }
    parsed_value = to_json(get_file("multiple_lines.vtt"))
    print(parsed_value)

    assert parsed_value == json.dumps(expected_value)
