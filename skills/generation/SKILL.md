---
name: kingdomrushdove-generation-plugin
description: >-
  为 KingdomRushDove 的 generation 分类添加代际地图、关卡、图鉴、通知、资源和默认升级线。使用
  generations.registry 和 kr1.generations.common。
---

# Generation 插件开发

读取根目录 `SKILL.md`、`references/common.md`、`references/checklist.md`、`references/level.md` 和 `references/porting.md`。代际
插件的 `config.lua` 使用 `category = "generation"`。入口注册 `require("generations.registry")`，
再调用 `GENS:register(require(ENTRY .. ".gen"))`。`gen.lua` 通常复用
`kr1.generations.common.standard({...})`，声明 `name`、`resource_root`、地图数据、关卡范围、音乐、
图鉴、通知和 `resources`。

目录可以拆分为 `data/levels`、`data/waves`、`templates`、`assets/images`、`assets/sounds` 和
`assets/strings`。代际资源和注册状态难以全部回滚时，不提供热卸载接口。

完成前逐项执行 `references/level.md` 的 Level / Generation 交付 Checklist。
