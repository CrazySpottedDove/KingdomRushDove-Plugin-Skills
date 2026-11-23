# 防御塔插件严格流程

本文件是防御塔插件的交付门槛。每一项都要在用户提供的本体路径中核对，不能用记忆中的模板名、
菜单位置或资源组名代替代码查询。

## 0. 开工前记录

- [ ] 已记录用户本体路径，并确认能读取 `version.lua`、`plugin/`、`kr1/`、`all/`、`all-desktop/`。
- [ ] 已确认塔的类别：`archer`、`barrack`、`mage` 或 `engineer`。
- [ ] 已确认是新增高级塔、修改现有塔、添加士兵/子弹，还是只改数值。
- [ ] 已确认塔的模板名、建造价格、升级价格、射程、攻击、技能等级和文案。
- [ ] 已列出所有需要的图鉴、菜单、图集、声音、动画、骨骼和语言资源。
- [ ] 已决定哪些数值是玩家配置，哪些是实现常量。

建议先在本体代码中定位以下位置，再开始写插件：

| 目标 | 查询位置 |
|---|---|
| 同类塔模板 | `kr1/archer_towers.lua`、`barrack_towers.lua`、`mage_towers.lua`、`engineer_towers.lua` |
| 塔分类 | `kr1/game_settings.lua` |
| 科技补丁列表 | `kr1/upgrades.lua` |
| 塔菜单 | `kr1/data/tower_menus_data.lua`、`kr1/data/tower_menus_data_scripts.lua` |
| 图鉴数据 | `kr1-desktop/data/tower_data.lua` |
| 行为脚本 | `kr1/tower_scripts.lua`、`kr1/game_scripts.lua` |
| 模板和组件 | `all/templates.lua`、`all/components.lua`、`all/entity_db.lua` |
| 加载生命周期 | `all/animation_db.lua`、`all/entity_db.lua`、`all/i18n.lua` |

## 1. 建立目录和命名表

推荐结构：

```text
<entry>/
├── config.lua
├── <entry>.lua
├── <entry>_config.lua          # 需要玩家配置时才创建
├── templates.lua
├── data/animations.lua         # 需要自定义动画时创建
└── assets/
    ├── images/
    ├── sounds/{groups.lua,sounds.lua}
    └── strings/{en.lua,zh-Hans.lua}
```

先写一张命名表，后续所有文件按表检查：

| 项目 | 命名要求 |
|---|---|
| 塔主模板 | `<entry>` 或 `<entry>_tower` |
| 士兵、子弹、修饰器、控制器 | `<entry>_...` |
| 图集组 | `<entry>_game`、`<entry>_gui` 等明确场景后缀 |
| 声音组和音效 | `<entry>_...` |
| 动画 key 和语言 key | 使用 `<entry>` 前缀 |
| 菜单 `action_arg` | 与实际塔模板名一致 |

entry、插件目录、入口文件和所有插件内 `require` 前缀必须一致。入口必须从 `local plugin = {}` 开始，
实现 `plugin:init(plugin_data)`，最后返回 `plugin`。

## 2. 模板依赖审计

- [ ] 从基础塔模板开始，递归记录 `attacks.list[*].bullet`、`barrack.soldier_type`、
      `powers.*`、`main_script.*`、`render.sprites[*]`、`sound_events.*` 和 `info.*` 的所有名称。
- [ ] 对每个名称在本体和插件内全局搜索，确认没有重复注册或错误覆盖。
- [ ] 每个插件专属模板都以 entry 前缀命名。
- [ ] 每个模板的父模板和组件在目标 `E:register_t` / `E:add_comps` 执行前已经存在。
- [ ] 脚本引用的模板、动画、声音、特效、修饰器和骨骼都有对应文件或本体定义。
- [ ] 逻辑只使用现有 `U`、`SU`、`simulation` 队列、`E:create_entity` 和本体常量。
- [ ] 没有直接写入 `store.entities`，没有用裸整数代替伤害类型、地形位或渲染层。

如果模板必须在实体库加载后修改，才使用 `hook_utils.HOOK(E, "load", handler)`。handler 必须先调用
`next(E)`，再按依赖顺序加载脚本和模板。能通过已有塔 registry 或声明字段完成的注册，不增加这个 hook。

## 3. 入口注册矩阵

按实际功能逐项填写，未使用的项保持不变：

| 目标状态 | 初始化动作 | 卸载动作（只有可完整恢复时才实现） |
|---|---|---|
| 塔可建造 | `GS.<class>_towers`、`GS.advanced_towers` 加入塔名 | 从相同数组移除同一值 |
| 科技能影响塔 | `UP` 对应数组加入塔/士兵/子弹 | 从相同数组移除同一值 |
| 局内图集 | `game.plugin_required_textures` 注册 | 删除相同 key |
| 地图/图鉴图集 | `screen_map` 或 `game_gui` 注册 | 删除相同 key |
| 纹理常驻 | `image_db.persistent_textures[key] = true` | 删除相同 key |
| 音效组 | `sound_db:register_groups`、`register_sounds` | 只有数据库提供对应移除 API 时才清理 |
| 局内声音 | `game.plugin_required_sounds` 加入组名 | 移除同一组名 |
| 图鉴 | `data.tower_data` 加入同一 table item | 删除同一 table item |
| 建造/升级菜单 | 用 `clever_add` 加入正确类别的三级列表 | 用 `clever_remove` 按 `action_arg` 删除，并清理 `tower_menus_data[entry]` |
| 国际化 | 合并当前 locale，并处理后续语言切换 | 只有能逐键恢复旧值时才清理 |
| 动画 | 在 `animation_db:load` 后 `register_animations` | `UNHOOK`，并确认数据库支持安全重建 |
| 模板 | 在 `entity_db:load` 后执行模板模块 | `UNHOOK`，清掉插件模板并重建受影响模板 |

`table.arrayensure` 使用前显式 `require("lib.klua.table")`。所有注册动作集中在 `init` 或清晰的局部
`inject` 函数中，避免模块加载时产生无法追踪的副作用。

## 4. 模板和脚本实现

- [ ] `templates.lua` 只注册插件拥有的模板，或修改已确认的目标模板。
- [ ] 塔的主实体使用本体已有的塔组件和 `tt.powers.*` 约定，技能升级字段与菜单等级一一对应。
- [ ] 士兵、子弹、修饰器和特效按依赖顺序注册，父模板明确可追溯。
- [ ] 行为函数使用局部函数或现有 `scripts.*`，不向全局脚本表写入无前缀名称。
- [ ] 实体插入、移除和伤害使用 `simulation:queue_*` 或现有包装函数。
- [ ] 攻击、索敌、冷却、伤害、护甲和移动速度使用本体 helper，运行时倍率不直接乘除字段。
- [ ] 协程逻辑在每个循环的正确位置 `coroutine.yield()`，并处理实体死亡、目标消失和插件配置边界。
- [ ] 模板字段的默认值、技能成长和配置字段的类型保持一致。
- [ ] 语言文案中的表达式引用了存在的模板字段，并覆盖所有声明的技能等级。

## 5. 资源与菜单检查

- [ ] `assets/images` 的每个描述符引用真实 `.dds`，按需提供同名 `.astc`。
- [ ] `game`、地图和 UI 图集注册到了实际使用它们的场景。
- [ ] `assets/sounds/groups.lua` 的每个文件存在，`sounds.lua` 中的每个 id 与模板事件一致。
- [ ] `data/animations.lua` 的 prefix、from、to 与图集真实帧连续对应。
- [ ] `TOWER_<NAME>_NAME`、`TOWER_<NAME>_DESCRIPTION` 和每个技能的名称/描述都有中英文键。
- [ ] 建造菜单放入正确基础塔类别的三级列表，升级项 `action_arg` 与塔名一致。
- [ ] 技能菜单的 `place`、图标、音效、短句和等级描述互相对应。
- [ ] 图鉴缩略图和详情图存在，`tower_data` 字段使用当前版本实际字段名。

## 6. 生命周期决策

默认只实现 `init`。完整实现以下条件后才增加可选接口：

- [ ] `reload` 不重复注册列表、菜单、声音、动画和 hook。
- [ ] `unload` 能撤销入口注册矩阵中的每一项，并清理插件模板。
- [ ] 重新加载时指定的 `package.loaded` 项会按依赖顺序重新执行。
- [ ] `on_config_change` 能更新当前运行逻辑，不重新读取旧配置，不留下旧模板状态。
- [ ] 已创建的场上塔、士兵、子弹和修饰器的行为影响已经明确，无法回溯时按重启处理。

空的 `reload`、`unload` 或 `on_config_change` 不计入完成度。

## 7. 验证门槛

- [ ] `tools/krdove_plugin.py validate <插件目录> --game-root <用户本体路径>` 通过。
- [ ] `tools/krdove_plugin.py asset-check <插件目录>` 通过。
- [ ] 用用户本体路径中的 Lua/LuaJIT 检查入口、模板、脚本、配置和资源描述符。
- [ ] 启动时日志没有入口加载、模板不存在、动画不存在、声音不存在或图集不存在错误。
- [ ] 地图上可以建造、出售、升级塔，基础攻击和每个技能都能触发。
- [ ] 士兵生成、死亡、重生、索敌、子弹命中、修饰器持续时间和声音均已实机检查。
- [ ] 图鉴、建造菜单、升级菜单、技能提示、语言切换和不同难度均已检查。
- [ ] 修改配置后按实际支持情况验证即时应用或重启生效。
