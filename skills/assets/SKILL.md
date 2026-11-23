---
name: kingdomrushdove-plugin-assets
description: >-
  管理 KingdomRushDove 插件的图集、DDS/ASTC、声音组、动画、骨骼、语言和资源注册。提供跨平台检查，
  不替代目标游戏的实际编译和上传工具。
---

# 插件美术与资源

读取根目录 `SKILL.md`、`references/common.md`、`references/checklist.md` 和 `references/assets.md`。先确认资源使用场景，再决定
写入英雄/法术声明还是直接注册 `game`、`screen_map`、`game_gui` 的资源表。

跨平台纹理同时维护桌面 `.dds` 和 Android `.astc`，图集描述符的 `a_name` 指向 `.dds`。声音通过
`groups.lua` 和 `sounds.lua` 注册，动画写入 `data/animations.lua`，语言文件至少同步中文和英文。

使用 `tools/krdove_plugin.py asset-check <插件目录>` 检查描述符引用和常见路径错误。工具不会压缩、重排或
上传资源。已有图集必须使用项目认可的单文件编译/重打包流程，不能用未知工具改写坐标。

完成前逐项执行 `references/assets.md` 的资源交付 Checklist。
