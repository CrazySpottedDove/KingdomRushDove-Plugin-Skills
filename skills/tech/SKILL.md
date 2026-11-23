---
name: kingdomrushdove-tech-plugin
description: >-
  为 KingdomRushDove 添加 upgrade 分类的科技线。复用 kr1.upgrades 的六个科技列，定义 techs、patch、
  图标、价格和等级，并按项目约定注册和命名。
---

# 科技线插件开发

读取根目录 `SKILL.md`、`references/common.md`、`references/checklist.md` 和 `references/tech.md`。先确认科技所属列、每级价格、
图标帧、影响的塔/法术/援军以及科技线被选中时始终执行的逻辑。

科技模块返回 `{techs = ...}`，每条科技包含 `class`、`icon`、`level`、`price` 和 `patch(UP, u)`。
入口把模块放入 `UP.list[ENTRY]`，所有自定义字段和文案 key 使用 entry 前缀。使用现有
`kr1.upgrades.upgrade_utils`，不要复制整套本体升级表，也不要用裸整数代替常量。

科技补丁写入共享模板或升级列表后通常难以回滚。除非能逐项恢复所有共享状态，否则只实现启动时的
`init`，让配置和启用修改通过重启生效。

完成前逐项执行 `references/tech.md` 的 Upgrade 交付 Checklist。
