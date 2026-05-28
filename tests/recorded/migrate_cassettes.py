# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from tests.recorded.cassette import cassette_with_rehydrated_bodies
from tests.recorded.conftest import (
    ReadableYamlSerializer,
    _filter_headers_by_prefix,
    _replace_case_insensitive,
)
from tests.recorded.sanitization import FILTERED_HEADERS, VOLATILE_RESPONSE_HEADERS

RECORDED_ROOT = Path(__file__).parent


def _filter_interaction_headers(interaction: dict[str, Any]) -> None:
    request_headers = interaction.get("request", {}).get("headers")
    if isinstance(request_headers, dict):
        _replace_case_insensitive(request_headers, FILTERED_HEADERS)
        _filter_headers_by_prefix(request_headers)
    response_headers = interaction.get("response", {}).get("headers")
    if isinstance(response_headers, dict):
        _replace_case_insensitive(response_headers, FILTERED_HEADERS | VOLATILE_RESPONSE_HEADERS)
        _filter_headers_by_prefix(response_headers)


def migrate_cassette(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    cassette = yaml.safe_load(original)
    if not isinstance(cassette, dict):
        return False
    cassette = cassette_with_rehydrated_bodies(cassette)
    for interaction in cassette.get("interactions", []):
        _filter_interaction_headers(interaction)
    serialized = ReadableYamlSerializer.serialize(cassette)
    if serialized == original:
        return False
    path.write_text(serialized, encoding="utf-8")
    return True


def main() -> None:
    changed = 0
    total = 0
    for path in sorted(RECORDED_ROOT.glob("**/cassettes/**/*.yaml")):
        if "/fake/" in path.as_posix():
            continue
        total += 1
        if migrate_cassette(path):
            changed += 1
            print(f"rewrote {path.relative_to(RECORDED_ROOT)}")
    print(f"{changed}/{total} cassettes rewritten")


if __name__ == "__main__":
    main()
