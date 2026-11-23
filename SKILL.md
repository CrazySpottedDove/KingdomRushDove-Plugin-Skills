---
name: kingdomrushdove-plugin
description: >-
  为 KingdomRushDove 制作 Lua 插件。先收集名称、entry、作者和插件类型，
  从本体 version.lua 读取 min_version，再按功能加载英雄、法术、科技、防御塔、
  关卡或美术资源参考。遵循项目的插件入口、模板、资源注册和保守热重载约定。
---

# KingdomRushDove 插件开发

这个 skill 面向 `/plugins/<entry>/` 下的插件，不直接修改游戏本体。开始实现前读取本文件、
`references/common.md` 和 `references/checklist.md`。需要具体类型时，再读取对应的子 skill。所有参考资料、脚本和模板都在本目录内，
不要假定用户机器安装了某个 shell、ImageMagick 或 LÖVE。

Wiki 用来解释字段和使用流程，目标游戏当前代码决定真实的注册表、分类和生命周期。遇到 Wiki 与
`/plugin`、`/dove_modules`、`/kr1` 中的代码不一致时，先验证代码，再更新本次实现所依据的字段。

## 开始工作

开始工作前先要求用户给出其机器上的 KingdomRushDove 本体路径，并确认该目录包含 `version.lua`。
后续读取版本、注册表、模板、资源和 API 时都以这个路径为准，不使用预设本体目录，也不根据其它副本推断。

再向用户收集四项元数据：插件名称、entry、作者名称、插件类型。不要要求用户填写 `min_version` 或
`desc`。从目标游戏根目录的 `version.lua` 读取 `version.id` 作为 `min_version`，根据用户描述概括 `desc`。
如果用户没有给版本号，使用 `0.1.0` 作为初始插件版本。`url` 默认空字符串，`branch` 默认 `master`，
`enabled` 默认 `true`，`priority` 默认 `0`。

确认元数据后，再和用户确认要实现的功能和影响范围。按功能加载下表中的一个或多个子 skill：

| 功能 | 子 skill | 参考 |
|---|---|---|
| 新英雄或已有英雄扩展 | `skills/hero/SKILL.md` | `references/hero.md` |
| 新法术 | `skills/spell/SKILL.md` | `references/spell.md` |
| 新科技线或升级线 | `skills/upgrade/SKILL.md`（或 `skills/tech/SKILL.md`） | `references/tech.md` |
| 新代际 | `skills/generation/SKILL.md` | `references/level.md`、`references/porting.md` |
| 新防御塔或塔模板 | `skills/tower/SKILL.md` | `references/tower.md` |
| 自制地图和波次 | `skills/level/SKILL.md` | `references/level.md` |
| 纹理、音效、动画、文案和打包 | `skills/assets/SKILL.md` | `references/assets.md` |

功能同时涉及多个类型时，只加载实际需要的子 skill。所有任务都使用 `references/common.md` 的通用约定，
移植来源和验证方式见 `references/porting.md`。

实现过程中持续填写 `references/checklist.md` 和对应类型的详细清单。清单中未完成的注册、资源或验证项
应保持公开状态，不能用空接口、模拟验证或占位代码标记为完成。

## 不可省略的编码约定

- 入口文件明确写 `local plugin = {}`，实现 `plugin:init(plugin_data)`，最后返回 `plugin`。
- 插件目录名、`config.lua` 的 `entry`、入口文件名和 `require` 前缀必须完全一致，统一使用
  `require("<entry>.<module>")` 访问插件自己的模块。
- 不使用 `_G`、新建 metatable 或依赖隐式全局状态。优先使用现有注册表、模板 API、资源 API 和
  `table.arrayensure` 等项目工具。不可避免的固定标识符集中在文件顶部，玩家可调数值放入
  `<entry>_config.lua`。
- 能通过注册表、模板声明或资源列表完成的功能，不使用 hook。确实需要 hook 时，使用
  `hook_utils.HOOK`，保留 `next(...)` 的责任链语义，并在实现了完整撤销逻辑时才提供 `unload`。
- `reload`、`unload` 和 `on_config_change` 都是可选接口。没有经过完整生命周期验证时省略接口，
  不写空函数、假热加载或占位实现。`init` 注册的每一项副作用都必须能在 `unload` 中逐项撤销，才可以
  声明热卸载支持。
- 模板、脚本、动画、声音、语言键和资源组的名称使用 entry 前缀，避免插件之间冲突。
- 不把 `package.loaded` 清理、全局脚本覆盖或整表重写当作默认方案。只有确实需要重新执行副作用模块时，
  才按对应参考文档清理指定缓存。

## 验证与工具

先用 `tools/krdove_plugin.py version --game-root <游戏根目录>` 检查本体版本，再用 `scaffold` 或手写文件。
完成后运行 `validate <插件目录> --game-root <用户提供的游戏根目录>`，并用 `asset-check <插件目录>` 检查图集描述符、
`.dds` 和 `.astc` 引用。Lua 语法检查和游戏内验证由目标环境执行，工具不会伪造成功结果。

```text
python tools/krdove_plugin.py version --game-root /path/to/KingdomRushDove
python tools/krdove_plugin.py scaffold --output /path/to/plugins/my_entry \
  --name "插件名称" --entry my_entry --author "作者" --category tower \
  --desc "插件功能的简短描述"
python tools/krdove_plugin.py validate /path/to/plugins/my_entry \
  --game-root /path/to/user/KingdomRushDove
python tools/krdove_plugin.py asset-check /path/to/plugins/my_entry
```

工具支持 Windows、Linux 和 macOS 的 Python 3.10+。路径参数使用当前平台的路径分隔符，工具不调用外部
命令。`scaffold --category` 接受本体当前的 `gameplay`、`tower`、`hero`、`display`、`cosmetic`、`enemy`、
`level`、`upgrade`、`generation`、`spell`、`other`，也接受 `tech` 和 `map` 这两个工作别名，分别映射
到 `upgrade` 和 `level`。脚本只创建不存在的文件，覆盖已有文件必须显式传 `--force`。

## 参考资料

- `references/common.md`：项目架构、入口、命名、模板和生命周期。
- `references/metadata.md`：`config.lua` 与玩家配置的字段和更新规则。
- `references/assets.md`：纹理、声音、动画、i18n 和多平台资源。
- `references/hero.md`、`spell.md`、`tech.md`、`tower.md`、`level.md`：各类插件的最小实现路径。
- `references/porting.md`：从外部内容移植时的边界、目录布局和验证阶梯。
- `references/checklist.md`：从需求确认到发布前验证的交付清单。
