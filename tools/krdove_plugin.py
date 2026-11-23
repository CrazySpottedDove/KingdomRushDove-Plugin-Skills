#!/usr/bin/env python3
"""Portable helpers for KingdomRushDove plugin work.

The script deliberately performs filesystem and text checks only.  It does not
invoke a shell, Lua, an image encoder, or an uploader.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable


ENTRY_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
VERSION_RE = re.compile(r"^\s*id\s*=\s*[\"']([^\"']+)[\"']")
FIELD_RE = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?:[\"']([^\"']*)[\"']|(true|false)|(-?\d+(?:\.\d+)?))\s*,?\s*(?:--.*)?$"
)
ASSET_NAME_RE = re.compile(r"\ba_name\s*=\s*[\"']([^\"']+)[\"']")
SOUND_FILE_RE = re.compile(r"\bfiles\s*=\s*\{([^}]*)\}", re.DOTALL)
QUOTED_RE = re.compile(r"[\"']([^\"']+)[\"']")
REQUIRED_METADATA = (
    "name",
    "entry",
    "version",
    "desc",
    "url",
    "by",
    "category",
    "enabled",
    "priority",
)
KNOWN_CATEGORIES = {
    "gameplay",
    "cosmetic",
    "display",
    "tower",
    "hero",
    "enemy",
    "level",
    "upgrade",
    "spell",
    "other",
    "generation",  # used by existing generation plugins
}
TYPE_ALIASES = {
    "map": "level",
    "tech": "upgrade",
}
PLUGIN_TYPES = KNOWN_CATEGORIES | set(TYPE_ALIASES)


def read_game_version(game_root: Path) -> str:
    """Read version.lua without executing Lua code."""

    version_file = game_root / "version.lua"
    if not version_file.is_file():
        raise ValueError(f"找不到本体版本文件: {version_file}")
    for line in version_file.read_text(encoding="utf-8").splitlines():
        match = VERSION_RE.match(line)
        if match:
            return match.group(1)
    raise ValueError(f"version.lua 中没有找到 version.id: {version_file}")


def parse_version(value: str) -> tuple[int, ...]:
    parts = value.split(".")
    if not parts or any(not part.isdigit() for part in parts):
        raise ValueError(f"版本号必须是点分数字: {value}")
    return tuple(int(part) for part in parts)


def version_at_least(current: str, required: str) -> bool:
    left = parse_version(current)
    right = parse_version(required)
    width = max(len(left), len(right))
    return left + (0,) * (width - len(left)) >= right + (0,) * (width - len(right))


def read_metadata(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = FIELD_RE.match(line)
        if not match:
            continue
        key, string_value, bool_value, number_value = match.groups()
        values[key] = string_value or bool_value or number_value
    return values


def write_if_allowed(path: Path, content: str, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def scaffold(args: argparse.Namespace) -> int:
    output = Path(args.output).expanduser().resolve()
    if not ENTRY_RE.fullmatch(args.entry):
        raise ValueError(f"entry 不是安全的 Lua 标识符: {args.entry}")
    game_version = read_game_version(Path(args.game_root).expanduser().resolve())
    if args.category not in PLUGIN_TYPES:
        raise ValueError(f"未知插件类型: {args.category}")
    category = TYPE_ALIASES.get(args.category, args.category)
    if not args.desc.strip():
        raise ValueError("desc 不能为空。请先由 AI 根据功能概括，再传入工具。")

    lua_string = lambda value: json.dumps(value, ensure_ascii=False)
    metadata = f'''return {{
\tname = {lua_string(args.name)},
\tentry = {lua_string(args.entry)},
\tversion = {lua_string(args.version)},
\tdesc = {lua_string(args.desc)},
\turl = {lua_string(args.url)},
\tby = {lua_string(args.author)},
\tcategory = {lua_string(category)},
\tenabled = true,
\tpriority = 0,
\tbranch = {lua_string(args.branch)},
\tmin_version = {lua_string(game_version)},
}}
'''
    entry = f'''local plugin = {{}}

function plugin:init(plugin_data)
\tself.plugin_data = plugin_data
end

return plugin
'''
    created = []
    for path, content in (
        (output / "config.lua", metadata),
        (output / f"{args.entry}.lua", entry),
    ):
        if write_if_allowed(path, content, args.force):
            created.append(str(path))
        else:
            print(f"skip existing: {path}")
    print(f"min_version = {game_version}")
    for path in created:
        print(f"created: {path}")
    return 0


def check_metadata(plugin_dir: Path, game_root: Path | None) -> list[str]:
    errors: list[str] = []
    config = plugin_dir / "config.lua"
    if not config.is_file():
        return [f"缺少 config.lua: {config}"]
    values = read_metadata(config)
    missing = [key for key in REQUIRED_METADATA if key not in values]
    errors.extend(f"config.lua 缺少字段: {key}" for key in missing)
    entry = values.get("entry", "")
    if entry and not ENTRY_RE.fullmatch(entry):
        errors.append(f"entry 不是安全的 Lua 标识符: {entry}")
    if entry and plugin_dir.name != entry:
        errors.append(f"目录名 {plugin_dir.name} 与 entry {entry} 不一致")
    if entry and not (plugin_dir / f"{entry}.lua").is_file():
        errors.append(f"缺少入口文件: {entry}.lua")
    category = values.get("category")
    if category and category not in KNOWN_CATEGORIES:
        errors.append(f"不认识的 category: {category}")
    if "min_version" in values:
        try:
            parse_version(values["min_version"])
        except ValueError as exc:
            errors.append(str(exc))
    if game_root and "min_version" in values:
        try:
            current = read_game_version(game_root)
            if not version_at_least(current, values["min_version"]):
                errors.append(
                    f"本体版本 {current} 低于插件 min_version {values['min_version']}"
                )
        except ValueError as exc:
            errors.append(str(exc))
    return errors


def source_lines(plugin_dir: Path) -> Iterable[tuple[Path, str]]:
    for path in sorted(plugin_dir.rglob("*.lua")):
        if path.is_file():
            for line in path.read_text(encoding="utf-8").splitlines():
                yield path, line


def check_forbidden_source(plugin_dir: Path) -> list[str]:
    errors: list[str] = []
    patterns = (
        (re.compile(r"\b_G\b"), "不要使用 _G"),
        (re.compile(r"\bsetmetatable\s*\("), "插件不要新建 metatable"),
        (re.compile(r"\blocal\s+hook\s*="), "入口应使用 local plugin = {}"),
    )
    for path, line in source_lines(plugin_dir):
        stripped = line.lstrip()
        if stripped.startswith("--"):
            continue
        for pattern, message in patterns:
            if pattern.search(line):
                errors.append(f"{path.relative_to(plugin_dir)}: {message}")
    return errors


def validate(args: argparse.Namespace) -> int:
    plugin_dir = Path(args.plugin_dir).expanduser().resolve()
    if not plugin_dir.is_dir():
        raise ValueError(f"插件目录不存在: {plugin_dir}")
    game_root = Path(args.game_root).expanduser().resolve() if args.game_root else None
    errors = check_metadata(plugin_dir, game_root)
    errors.extend(check_forbidden_source(plugin_dir))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"valid: {plugin_dir}")
    return 0


def asset_check(args: argparse.Namespace) -> int:
    plugin_dir = Path(args.plugin_dir).expanduser().resolve()
    image_dir = plugin_dir / "assets" / "images"
    sound_dir = plugin_dir / "assets" / "sounds"
    errors: list[str] = []
    warnings: list[str] = []
    if image_dir.is_dir():
        for descriptor in sorted(image_dir.rglob("*.lua")):
            text = descriptor.read_text(encoding="utf-8")
            for name in ASSET_NAME_RE.findall(text):
                image = descriptor.parent / name
                if not image.is_file():
                    errors.append(f"{descriptor.relative_to(plugin_dir)} 引用的图集不存在: {name}")
                if image.suffix.lower() == ".dds":
                    astc = image.with_suffix(".astc")
                    if not astc.is_file():
                        warnings.append(f"缺少 Android 纹理（可选）: {astc.relative_to(plugin_dir)}")
    if sound_dir.is_dir():
        for descriptor in sorted(sound_dir.rglob("*.lua")):
            text = descriptor.read_text(encoding="utf-8")
            for block in SOUND_FILE_RE.findall(text):
                for name in QUOTED_RE.findall(block):
                    sound = descriptor.parent / name
                    if not sound.is_file():
                        errors.append(f"{descriptor.relative_to(plugin_dir)} 引用的声音不存在: {name}")
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"assets checked: {plugin_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="KingdomRushDove plugin helpers")
    sub = parser.add_subparsers(dest="command", required=True)

    version = sub.add_parser("version", help="读取本体 version.lua 的 version.id")
    version.add_argument("--game-root", required=True)

    init = sub.add_parser("scaffold", help="生成最小插件入口和元数据")
    init.add_argument("--output", required=True)
    init.add_argument("--game-root", required=True)
    init.add_argument("--name", required=True)
    init.add_argument("--entry", required=True)
    init.add_argument("--author", required=True)
    init.add_argument("--category", default="other", choices=sorted(PLUGIN_TYPES))
    init.add_argument("--desc", required=True)
    init.add_argument("--version", default="0.1.0")
    init.add_argument("--url", default="")
    init.add_argument("--branch", default="master", choices=("master", "dev"))
    init.add_argument("--force", action="store_true")

    check = sub.add_parser("validate", help="校验元数据、路径和插件代码红线")
    check.add_argument("plugin_dir")
    check.add_argument("--game-root", required=True)

    assets = sub.add_parser("asset-check", help="校验图集和声音文件引用")
    assets.add_argument("plugin_dir")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "version":
            print(read_game_version(Path(args.game_root).expanduser().resolve()))
            return 0
        if args.command == "scaffold":
            return scaffold(args)
        if args.command == "validate":
            return validate(args)
        if args.command == "asset-check":
            return asset_check(args)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    parser.error("未知命令")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
