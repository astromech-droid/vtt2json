import json
import re


def _is_ignored_line(vtt_line: str) -> bool:
    ignore_patterns = [r"^WEBVTT", r"^STYLE$", r"::cue", r"^ ", r"^\}$", r"^\n$"]

    for ip in ignore_patterns:
        if re.match(ip, vtt_line):
            return True

    return False


def _is_timestamp_line(vtt_line: str) -> bool:
    timestamp_pattern = r"\d{2}:\d{2}:\d{2}.\d{3}"
    timestamp_line_pattern = rf"^{timestamp_pattern} --> {timestamp_pattern}"

    if re.match(timestamp_line_pattern, vtt_line):
        return True
    else:
        return False


def _extract_timestamps(vtt_line: str) -> list:
    timestamp_pattern = r"\d{2}:\d{2}:\d{2}.\d{3}"
    timestamps: tuple = re.match(
        rf"^({timestamp_pattern}) --> ({timestamp_pattern})", vtt_line
    ).groups()
    return timestamps


def to_json(vtt_path: str) -> str:
    return json.dumps(to_dict(vtt_path))


def to_dict(vtt_path: str) -> dict:
    parsed_lines = []
    ignored_lines = []
    parsed_line = {"start": None, "end": None, "text": None, "_raw_text": None}

    with open(vtt_path, "r") as vtt_file:

        for vtt_line in vtt_file:

            if _is_ignored_line(vtt_line):
                ignored_lines.append(vtt_line)

            elif _is_timestamp_line(vtt_line):
                timestamps: tuple = _extract_timestamps(vtt_line)
                parsed_line["start"] = timestamps[0]
                parsed_line["end"] = timestamps[1]

            else:
                parsed_line["text"] = str(vtt_line)
                parsed_line["_raw_text"] = str(vtt_line)

                # 値渡しする (参照渡しするとparsed_linesの中身が上書きされてしまう)
                parsed_lines.append(parsed_line.copy())

    return {"parsed_lines": parsed_lines, "ignored_lines": ignored_lines}
