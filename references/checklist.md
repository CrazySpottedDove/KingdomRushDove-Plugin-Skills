# 插件交付 Checklist

类型任务必须同时执行对应的详细清单：防御塔看 `references/tower.md`，英雄看 `references/hero.md`，法术看
`references/spell.md`，upgrade 看 `references/tech.md`，level/generation 看 `references/level.md`，资源看
`references/assets.md`。本文件负责跨类型门槛，不能替代这些清单。

## 需求与元数据

- [ ] 已要求用户提供本机 KingdomRushDove 本体路径。
- [ ] 该路径可读取 `version.lua`，后续代码、注册表、模板和资源查询均使用此路径。
- [ ] 已确认插件名称、唯一 entry、作者和功能类型。
- [ ] 已从目标游戏 `version.lua` 读取 `version.id`，并把它写入 `min_version`。
- [ ] `desc` 只描述玩家可见功能、适用范围和限制，未承诺未经验证的热重载。
- [ ] `config.lua` 的目录名、entry 和入口文件名完全一致。
- [ ] `category` 使用当前管理器支持的值：`gameplay`、`tower`、`hero`、`display`、`cosmetic`、
      `enemy`、`level`、`upgrade`、`generation`、`spell` 或 `other`。
- [ ] 版本、渠道、启用状态和优先级都有明确值。

## 入口与代码

- [ ] 入口使用 `local plugin = {}`，实现 `plugin:init(plugin_data)` 并返回 `plugin`。
- [ ] 插件内部模块使用 `<entry>.` 命名空间。
- [ ] 没有使用 `_G`、新建 metatable 或隐式全局状态。
- [ ] 固定模板名、资源名、语言键和声音 id 带 entry 前缀。
- [ ] 能使用声明、registry、模板字段或资源列表完成的操作没有引入 hook。
- [ ] hook 处理器保存了函数引用，责任链正确调用 `next`，并保留必要返回值。
- [ ] 玩家可调数值集中在 `<entry>_config.lua`，每个字段都有 `key_label_map` 项。

## 类型实现

- [ ] 英雄使用 `heroes.registry`，声明 room、技能顺序、模板模块和按场景资源。
- [ ] 法术使用 `spell_system`，模块的 `name` 与模块文件名一致，提供 `register_templates(E)`、
      `apply(level)` 和 `resources`。
- [ ] upgrade 科技线使用 `kr1.upgrades` 的六个列，科技包含 class、icon、level、price 和所需 patch。
- [ ] generation 使用 `generations.registry`，代际模块提供地图、关卡范围、资源、音乐和升级线信息。
- [ ] 防御塔的塔分类、升级列表、图鉴、菜单、模板、动画、声音和资源注册点都已覆盖。
- [ ] level 插件使用编辑器生成的网格、路径、实体和波次数据，战役波次文件存在。

## 资源

- [ ] 纹理描述符的 `a_name` 与文件实际存在，桌面 DDS 和 Android ASTC 按需提供。
- [ ] 声音组、音效定义、动画、骨骼和语言文件的引用路径均可解析。
- [ ] 场景资源注册到了正确的 `game`、地图或 UI 资源表。
- [ ] 语言键、动画 key、图集组和声音 id 没有跨插件冲突。

## 生命周期与验证

- [ ] 没有为了接口完整而添加空的 `reload`、`unload` 或 `on_config_change`。
- [ ] 每个已实现的生命周期接口都能处理模块缓存和共享注册表状态。
- [ ] `tools/krdove_plugin.py validate <插件目录> --game-root <用户本体路径>` 通过。
- [ ] `tools/krdove_plugin.py asset-check` 通过。
- [ ] 目标环境的 Lua 语法检查通过。
- [ ] 已在实际地图验证选择、加载、资源、实体、技能、升级、波次和 UI。
- [ ] 需要发布时，包中保留运行时资源，去除本地备份和临时文件。
