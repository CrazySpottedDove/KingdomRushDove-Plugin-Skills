---
name: kingdomrushdove-spell-plugin
description: >-
  在 KingdomRushDove 中添加可选法术。负责 SPELLS.module_names、法术模块、控制器模板、等级成长、
  资源和文案，避免无必要的 hook 与不可逆热重载。
---

# 法术插件开发

读取根目录 `SKILL.md`、`references/common.md`、`references/checklist.md`、`references/spell.md`，资源需求再读取
`references/assets.md`。先确认法术目标、选择范围、等级 1–6 的效果、冷却、伤害类型和资源。

使用一个返回模块表的 `<entry>.<spell_name>` 文件，声明与模块文件名一致的 `name`、`i18n`、`control`、
按钮/指针/海报纹理、`resources` 和声音。入口把模块路径加入 `require("spell_system").module_names`。
控制器模板在 `register_templates(E)` 中注册，
`apply(level)` 只调整已经注册模板的数值和开关。

模板名、声音、图集和语言键使用 entry 前缀。法术按钮资源进入当前 UI 场景的资源表。没有完整移除
`SPELLS.module_names`、模板、声音和资源状态的方案时，不实现可选生命周期接口。

完成前逐项执行 `references/spell.md` 的交付 Checklist。
