---
name: kingdomrushdove-upgrade-plugin
description: >-
  为 KingdomRushDove 的 upgrade 分类添加科技线或升级线。复用 kr1.upgrades 的六个科技列，定义
  techs、patch、图标、价格和等级，并按项目约定注册和命名。
---

# Upgrade 插件开发

读取根目录 `SKILL.md`、`references/common.md`、`references/checklist.md` 和 `references/tech.md`。当前插件管理器的正式分类值是
`upgrade`，不是旧文档中泛化的 `gameplay`。实现方式仍以 `kr1.upgrades` 和本体 `line*.lua` 为准。

每条科技声明 `class`、`icon`、`level`、`price`，需要改模板时提供 `patch(UP, u)`。入口将模块写入
`UP.list[ENTRY]`，文案使用 `UPGRADES_<ENTRY>`。无法恢复共享模板、升级列表和已执行补丁时，不实现热卸载。

完成前逐项执行 `references/tech.md` 的 Upgrade 交付 Checklist。
