---
name: kingdomrushdove-hero-plugin
description: >-
  在 KingdomRushDove 中新增英雄或扩展已有英雄。使用 heroes.registry 声明、按场景注册资源，
  组织模板、动画、音效和文案，并只在可以完整回滚时实现热重载。
---

# 英雄插件开发

先读取根目录 `SKILL.md`、`references/common.md`、`references/checklist.md` 和 `references/hero.md`。向用户确认英雄是新增还是扩展
本体英雄、解锁条件、技能顺序、资源范围和玩家可调参数。再按需读取 `references/assets.md`。

实现时：

1. 入口使用 `local plugin = {}`，在 `init` 中调用 `heroes.registry:register`。
2. 英雄声明包含 `room`、`room_special_order`、`templates`、`animations`、`sounds`、`groups` 和按场景
   划分的 `resources`。模块路径使用 `<entry>.` 前缀。
3. `templates.lua` 只注册或修改该英雄真正拥有的模板。脚本通过模板字段连接现有 `U`、`SU` 和游戏脚本。
4. 动画、声音和语言资源分别登记，所有 id 和 key 带 entry 前缀。
5. 配置变更没有经过完整实机验证时，不提供 `reload`、`unload` 或 `on_config_change`。

使用 registry 声明结构。不要把旧式全局英雄表、未使用的脚本函数或空热重载接口搬进来。

完成前逐项执行 `references/hero.md` 的交付 Checklist。
