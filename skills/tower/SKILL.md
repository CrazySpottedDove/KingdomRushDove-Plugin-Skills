---
name: kingdomrushdove-tower-plugin
description: >-
  在 KingdomRushDove 中新增防御塔或修改塔模板。覆盖塔注册、模板、菜单、动画、音效、图集和可逆
  生命周期，适用于复杂塔而非单纯数值配置。
---

# 防御塔插件开发

读取根目录 `SKILL.md`、`references/common.md`、`references/checklist.md` 和 `references/tower.md`，资源部分再读取
`references/assets.md`。先确认塔类别、建造/升级菜单、士兵和子弹、技能等级、资源和是否需要图鉴。

按入口注册、模板、动画、音效、文案和菜单数据拆分。先在目标游戏找到同类塔模板和
脚本，再注册塔列表、升级列表、图鉴、场景资源和菜单。使用现有模板继承、`U`、`SU`、`simulation` 队列
和 sound/animation 数据库。只有没有直接注册点时才使用 hook。

入口必须明确使用 `local plugin = {}`。每一个 `init` 副作用都要能在 `unload` 中撤销，才实现热卸载。
不要为了接口完整而写空方法，也不要在热重载中重复注册菜单或模板。

完成前逐项执行 `references/tower.md` 的 0–7 节。任一注册点、资源引用、菜单动作或实机验证没有证据时，
保留为未完成项，不用占位代码掩盖缺口。
