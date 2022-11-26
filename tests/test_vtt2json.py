import os
import json
from vtt2json.vtt2json import to_json

SUBTITLES_DIR = os.path.join(os.path.dirname(__file__), "subtitles")


def get_file(filename):
    return os.path.join(SUBTITLES_DIR, filename)


def test_ignore_lines():
    expected_value = {
        "parsed_lines": [],
    }
    parsed_value = to_json(get_file("ignore_lines.vtt"))

    assert parsed_value == json.dumps(expected_value)


def test_ignore_lines_verbos():
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
    parsed_value = to_json(get_file("ignore_lines.vtt"), verbos=True)

    assert parsed_value == json.dumps(expected_value)


def test_regular_lines():
    expected_value = {
        "parsed_lines": [
            {
                "start": "00:00:01.960",
                "end": "00:00:03.795",
                "text": "CLAIRE: Kids! Breakfast!",
            }
        ],
    }
    parsed_value = to_json(get_file("regular_lines.vtt"))

    assert parsed_value == json.dumps(expected_value)


def test_regular_lines_verbos():
    expected_value = {
        "parsed_lines": [
            {
                "start": "00:00:01.960",
                "end": "00:00:03.795",
                "text": "CLAIRE: Kids! Breakfast!",
                "_raw": {
                    "start": "00:00:01.960",
                    "end": "00:00:03.795",
                    "text": "CLAIRE: Kids! Breakfast!",
                },
            }
        ],
        "ignored_lines": [],
    }
    parsed_value = to_json(get_file("regular_lines.vtt"), verbos=True)

    assert parsed_value == json.dumps(expected_value)


def test_multiple_lines():
    expected_value = {
        "parsed_lines": [
            {
                "start": "00:00:22.231",
                "end": "00:00:25.526",
                "text": "All right, that's not gonna happen.",
            },
            {
                "start": "00:00:22.231",
                "end": "00:00:25.526",
                "text": "And, wow, you're not wearing that outfit.",
            },
        ],
    }
    parsed_value = to_json(get_file("multiple_lines.vtt"))

    assert parsed_value == json.dumps(expected_value)


def test_multiple_lines_verbos():
    expected_value = {
        "parsed_lines": [
            {
                "start": "00:00:22.231",
                "end": "00:00:25.526",
                "text": "All right, that's not gonna happen.",
                "_raw": {
                    "start": "00:00:22.231",
                    "end": "00:00:25.526",
                    "text": "All right, that's not gonna happen.",
                },
            },
            {
                "start": "00:00:22.231",
                "end": "00:00:25.526",
                "text": "And, wow, you're not wearing that outfit.",
                "_raw": {
                    "start": "00:00:22.231",
                    "end": "00:00:25.526",
                    "text": "And, wow, you're not wearing that outfit.",
                },
            },
        ],
        "ignored_lines": [],
    }
    parsed_value = to_json(get_file("multiple_lines.vtt"), verbos=True)

    assert parsed_value == json.dumps(expected_value)


def test_separated_lines():
    expected_value = {
        "parsed_lines": [
            {
                "start": "00:02:41.161",
                "end": "00:02:43.956",
                "text": "We just adopted her from Vietnam",
            },
            {
                "start": "00:02:44.039",
                "end": "00:02:46.250",
                "text": "and we're bringing her home",
            },
            {
                "start": "00:02:44.039",
                "end": "00:02:46.250",
                "text": "for the first time.",
            },
        ],
    }
    parsed_value = to_json(get_file("separated_lines.vtt"))

    assert parsed_value == json.dumps(expected_value)


def test_separated_lines_verbos():
    expected_value = {
        "parsed_lines": [
            {
                "start": "00:02:41.161",
                "end": "00:02:43.956",
                "text": "We just adopted her from Vietnam",
                "_raw": {
                    "start": "00:02:41.161",
                    "end": "00:02:43.956",
                    "text": "We just adopted her from Vietnam",
                },
            },
            {
                "start": "00:02:44.039",
                "end": "00:02:46.250",
                "text": "and we're bringing her home",
                "_raw": {
                    "start": "00:02:44.039",
                    "end": "00:02:46.250",
                    "text": "and we're bringing her home",
                },
            },
            {
                "start": "00:02:44.039",
                "end": "00:02:46.250",
                "text": "for the first time.",
                "_raw": {
                    "start": "00:02:44.039",
                    "end": "00:02:46.250",
                    "text": "for the first time.",
                },
            },
        ],
        "ignored_lines": ["\n"],
    }
    parsed_value = to_json(get_file("separated_lines.vtt"), verbos=True)

    assert parsed_value == json.dumps(expected_value)


def test_join_separated_lines():
    expected_value = {
        "parsed_lines": [
            {
                "start": "00:02:41.161",
                "end": "00:02:46.250",
                "text": "We just adopted her from Vietnam and we're bringing her home for the first time.",
            },
        ],
    }
    parsed_value = to_json(get_file("separated_lines.vtt"), join_separated_lines=True)

    assert parsed_value == json.dumps(expected_value)


def test_join_separated_lines_verbos():
    expected_value = {
        "parsed_lines": [
            {
                "start": "00:02:41.161",
                "end": "00:02:46.250",
                "text": "We just adopted her from Vietnam and we're bringing her home for the first time.",
                "_raw": [
                    {
                        "start": "00:02:41.161",
                        "end": "00:02:43.956",
                        "text": "We just adopted her from Vietnam",
                    },
                    {
                        "start": "00:02:44.039",
                        "end": "00:02:46.250",
                        "text": "and we're bringing her home",
                    },
                    {
                        "start": "00:02:44.039",
                        "end": "00:02:46.250",
                        "text": "for the first time.",
                    },
                ],
            },
        ],
        "ignored_lines": ["\n"],
    }
    parsed_value = to_json(
        get_file("separated_lines.vtt"), verbos=True, join_separated_lines=True
    )

    assert parsed_value == json.dumps(expected_value)
