---
name: kingdomrushdove-level-plugin
description: >-
  制作 KingdomRushDove 自制地图插件。使用地图编辑器生成关卡实体、网格、路径和波次，注册地图资源、
  元数据与模式，并保持入口最小化。
---

# 地图插件开发

读取根目录 `SKILL.md`、`references/common.md`、`references/checklist.md`、`references/level.md`，资源部分再读取
`references/assets.md`。先确认地图名称、entry、模式、战役/英雄/铁人波次、背景和本体资源依赖。

`config.lua` 使用 `category = "level"`，入口只保留必要的 `init`。`data/levels/`、`data/waves/` 和
`data/waveconfigs/` 的文件名必须包含 entry。网格、路径、塔位、出怪点和波次优先由游戏内编辑器生成，
不要手写替代编辑器的巨大数据。

地图脚本使用 `level:init(store)` 和 `level:update(store)`。在当前关卡修改模板时只改本局实体库，实体
插入和英雄选择使用 `level_utils`。没有完整移除地图注册和资源的方案时，不实现可选热接口。

完成前逐项执行 `references/level.md` 的 Level / Generation 交付 Checklist。
