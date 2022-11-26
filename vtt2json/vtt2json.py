import json
import re
import copy


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


def _erase_lf_code(vtt_line: str) -> str:
    return re.sub(r"^(.*)\n$", "\\1", vtt_line)


def _is_end_of_line(text: str) -> list:
    return re.match(r".*\W$", text)


def _join_separated_lines(separated_lines: list) -> list:
    joined_lines = []
    text_queue = []
    start = None
    end = None
    text = None
    raw = []

    for parsed_line in separated_lines:

        text_queue.append(parsed_line["text"])

        if start is None:
            start = parsed_line["start"]

        if "_raw" in parsed_line:
            raw.append(parsed_line["_raw"])

        if _is_end_of_line(parsed_line["text"]):
            end = parsed_line["end"]
            text = " ".join(text_queue)
            text_queue.clear()
            joined_line = {"start": start, "end": end, "text": text}

            if len(raw) > 0:
                joined_line["_raw"] = raw

            joined_lines.append(joined_line)

            # 初期化
            start = None
            end = None
            text = None
            raw = []

    return joined_lines


def to_json(vtt_path: str, verbos=False, join_separated_lines=False) -> str:
    return json.dumps(to_dict(vtt_path, verbos, join_separated_lines))


def to_dict(vtt_path: str, verbos=False, join_separated_lines=False) -> dict:
    parsed_lines = []
    ignored_lines = []
    parsed_line = {"start": None, "end": None, "text": None}

    if verbos:
        parsed_line["_raw"] = {"start": None, "end": None, "text": None}

    with open(vtt_path, "r") as vtt_file:

        for vtt_line in vtt_file:

            if _is_ignored_line(vtt_line):
                ignored_lines.append(vtt_line)

            elif _is_timestamp_line(vtt_line):
                timestamps: tuple = _extract_timestamps(vtt_line)
                start = timestamps[0]
                end = timestamps[1]
                parsed_line["start"] = start
                parsed_line["end"] = end

                if verbos:
                    parsed_line["_raw"]["start"] = start
                    parsed_line["_raw"]["end"] = end

            else:
                text = _erase_lf_code(vtt_line)
                parsed_line["text"] = text

                if verbos:
                    parsed_line["_raw"]["text"] = text

                # 値渡しする (参照渡しするとparsed_linesの中身が上書きされてしまう)
                # ※deepcopyでないと子dict(_raw)が値渡しにならない)
                parsed_lines.append(copy.deepcopy(parsed_line))

    if join_separated_lines:
        parsed_lines = _join_separated_lines(parsed_lines)

    dict_data = {
        "parsed_lines": parsed_lines,
    }

    if verbos:
        dict_data["ignored_lines"] = ignored_lines

    return dict_data
