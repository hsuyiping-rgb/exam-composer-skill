#!/usr/bin/env python3
"""Build a repeated English listening-test MP3 from a UTF-8 JSON config."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import subprocess
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SAMPLE_RATE = 48_000
DEFAULT_VOICES = {
    "narrator": "en-US-AriaNeural",
    "boy": "en-US-GuyNeural",
    "girl": "en-US-JennyNeural",
    "zh_tw": "zh-TW-YunJheNeural",
}


@dataclass(frozen=True)
class Spoken:
    speaker: str
    voice: str
    text: str
    rate: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path, help="UTF-8 JSON config")
    parser.add_argument("--output", required=True, type=Path, help="Output MP3 path")
    parser.add_argument("--work-dir", type=Path, help="Cache/temp directory")
    parser.add_argument("--ffmpeg", default="ffmpeg", help="ffmpeg executable")
    parser.add_argument("--dry-run", action="store_true", help="Validate only")
    return parser.parse_args()


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as stream:
        data = json.load(stream)
    if not isinstance(data, dict):
        raise ValueError("Config root must be a JSON object")
    return data


def validate_config(data: dict[str, Any]) -> None:
    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        raise ValueError("questions must be a non-empty array")

    repeat_count = data.get("repeat_count", 2)
    if not isinstance(repeat_count, int) or repeat_count < 1:
        raise ValueError("repeat_count must be a positive integer")

    voices = {**DEFAULT_VOICES, **data.get("voices", {})}
    numbers: list[int] = []
    for question in questions:
        if not isinstance(question, dict):
            raise ValueError("Each question must be an object")
        number = question.get("number")
        if not isinstance(number, int) or number < 1:
            raise ValueError("Each question.number must be a positive integer")
        numbers.append(number)
        pause = question.get("pause_seconds")
        if not isinstance(pause, (int, float)) or pause < 0:
            raise ValueError(f"Question {number}: pause_seconds must be non-negative")
        turns = question.get("turns")
        if not isinstance(turns, list) or not turns:
            raise ValueError(f"Question {number}: turns must be a non-empty array")
        for turn in turns:
            if not isinstance(turn, dict):
                raise ValueError(f"Question {number}: each turn must be an object")
            speaker = turn.get("speaker")
            text = turn.get("text")
            if speaker not in voices:
                raise ValueError(f"Question {number}: unknown speaker {speaker!r}")
            if not isinstance(text, str) or not text.strip():
                raise ValueError(f"Question {number}: turn text cannot be empty")

    expected = list(range(1, len(numbers) + 1))
    if numbers != expected:
        raise ValueError(f"Question numbers must be sequential: expected {expected}, got {numbers}")


def spoken_from(data: dict[str, Any], speaker: str, text: str) -> Spoken:
    voices = {**DEFAULT_VOICES, **data.get("voices", {})}
    rates = data.get("voice_rates", {})
    return Spoken(speaker, voices[speaker], text.strip(), rates.get(speaker, data.get("rate", "-10%")))


def clip_key(item: Spoken) -> str:
    raw = f"{item.voice}|{item.rate}|{item.text}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:20]


async def synthesize(item: Spoken, clips: Path, ffmpeg: str) -> Path:
    try:
        import edge_tts
    except ImportError as error:
        raise RuntimeError("edge-tts is required for synthesis") from error

    clips.mkdir(parents=True, exist_ok=True)
    key = clip_key(item)
    mp3_path = clips / f"{key}.mp3"
    wav_path = clips / f"{key}.wav"
    if not mp3_path.exists():
        await edge_tts.Communicate(item.text, item.voice, rate=item.rate).save(str(mp3_path))
    if not wav_path.exists():
        subprocess.run(
            [
                ffmpeg,
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-i",
                str(mp3_path),
                "-ar",
                str(SAMPLE_RATE),
                "-ac",
                "1",
                "-c:a",
                "pcm_s16le",
                str(wav_path),
            ],
            check=True,
        )
    return wav_path


def append_silence(output: wave.Wave_write, seconds: float) -> None:
    output.writeframes(b"\x00\x00" * int(SAMPLE_RATE * seconds))


def append_clip(output: wave.Wave_write, path: Path) -> None:
    with wave.open(str(path), "rb") as source:
        if (
            source.getnchannels() != 1
            or source.getsampwidth() != 2
            or source.getframerate() != SAMPLE_RATE
        ):
            raise RuntimeError(f"Unexpected PCM format: {path}")
        output.writeframes(source.readframes(source.getnframes()))


async def build(data: dict[str, Any], output_path: Path, work_dir: Path, ffmpeg: str) -> None:
    repeat_count = data.get("repeat_count", 2)
    turn_pause = float(data.get("turn_pause_seconds", 0.45))
    question_gap = float(data.get("question_gap_seconds", 0.8))
    number_template = data.get("number_template", "Number {number}.")

    intro = None
    if data.get("intro"):
        intro = spoken_from(data, data.get("intro_speaker", "zh_tw"), data["intro"])
    outro = None
    if data.get("outro"):
        outro = spoken_from(data, data.get("outro_speaker", "zh_tw"), data["outro"])

    questions: list[tuple[Spoken, list[Spoken], float]] = []
    all_items: list[Spoken] = [item for item in (intro, outro) if item]
    for question in data["questions"]:
        number_item = spoken_from(
            data, "narrator", number_template.format(number=question["number"])
        )
        turns = [spoken_from(data, turn["speaker"], turn["text"]) for turn in question["turns"]]
        questions.append((number_item, turns, float(question["pause_seconds"])))
        all_items.extend([number_item, *turns])

    unique_items = {clip_key(item): item for item in all_items}
    clip_paths: dict[str, Path] = {}
    clips = work_dir / "clips"
    for index, item in enumerate(unique_items.values(), start=1):
        print(f"Synthesizing {index}/{len(unique_items)}: {item.text}")
        clip_paths[clip_key(item)] = await synthesize(item, clips, ffmpeg)

    work_dir.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wav_path = work_dir / f"{output_path.stem}.wav"
    with wave.open(str(wav_path), "wb") as assembled:
        assembled.setnchannels(1)
        assembled.setsampwidth(2)
        assembled.setframerate(SAMPLE_RATE)
        if intro:
            append_clip(assembled, clip_paths[clip_key(intro)])
            append_silence(assembled, float(data.get("intro_gap_seconds", 2.0)))

        for index, (number_item, turns, answer_pause) in enumerate(questions):
            append_clip(assembled, clip_paths[clip_key(number_item)])
            append_silence(assembled, float(data.get("number_gap_seconds", 0.8)))
            for _ in range(repeat_count):
                for turn_index, item in enumerate(turns):
                    append_clip(assembled, clip_paths[clip_key(item)])
                    if turn_index < len(turns) - 1:
                        append_silence(assembled, turn_pause)
                append_silence(assembled, answer_pause)
            if index < len(questions) - 1:
                append_silence(assembled, question_gap)

        if outro:
            append_clip(assembled, clip_paths[clip_key(outro)])
            append_silence(assembled, 1.0)

    subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(wav_path),
            "-af",
            "loudnorm=I=-18:TP=-2:LRA=7",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
            str(output_path),
        ],
        check=True,
    )
    print(f"Created: {output_path}")


def main() -> None:
    args = parse_args()
    data = load_config(args.config)
    validate_config(data)
    print(f"Validated {len(data['questions'])} questions; repeat_count={data.get('repeat_count', 2)}")
    if args.dry_run:
        return
    work_dir = args.work_dir or args.output.parent / ".listening_audio_work"
    asyncio.run(build(data, args.output, work_dir, args.ffmpeg))


if __name__ == "__main__":
    main()
