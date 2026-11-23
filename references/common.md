# 通用实现约定

## 本体路径

工作开始前必须取得用户提供的 KingdomRushDove 本体路径。用该路径读取 `version.lua`、`plugin/`、
`dove_modules/`、`all/`、`all-desktop/` 和 `kr1/`。仓库内文档只提供导航，实际字段和注册表以用户指定
本体中的当前代码为准。

## 运行时结构

KingdomRushDove 是 LÖVE 2D + Lua 游戏。插件由 `plugin_main` 扫描 `plugins/`，按
`config.lua` 的 `priority` 排序，加载 `<entry>/<entry>.lua`，再调用入口表的 `init(plugin_data)`。
插件自己的目录必须等于 `entry`。插件只应改运行时注册表、模板和资源声明，不直接改核心仓库文件。

常用模块如下：

| 模块 | 用途 |
|---|---|
| `entity_db` | `E:get_template`、`E:register_t`、模板实例化 |
| `animation_db` | 注册动画定义 |
| `sound_db` | 注册音效和声音组 |
| `i18n` | 合并当前语言文案 |
| `game` | 对局资源和运行时数据 |
| `screen_map` / `game_gui` | 大地图和局内 UI 资源 |
| `kr1.game_settings` | 塔分类和可建造列表 |
| `kr1.upgrades` | 科技、兵种和弹道补丁列表 |
| `heroes.registry` | 英雄声明、资源和模板模块 |
| `hook_utils` | 只有没有更直接注册 API 时才使用 hook |

插件管理器的分类以 `dove_modules/gui/plugin_manager_view.lua` 的 `CATEGORY_OPTIONS` 为准。当前包含
`gameplay`、`tower`、`hero`、`display`、`cosmetic`、`enemy`、`level`、`upgrade`、`generation`、
`spell` 和 `other`。法术注册表实现位于 `kr1/spell_system.lua`，代际注册表位于
`kr1/generations/registry.lua`，科技线数据由 `kr1/upgrades.lua` 的 `list` 消费。

游戏实体是 ECS 模板。模板模块通常通过副作用注册，不返回工厂函数。模板中的运行逻辑使用现有的
`scripts`、`U`、`SU`、`LU` 和 `simulation` API。创建或删除场上实体使用队列 API，不能直接修改
`store.entities`。

## Lua 书写风格

- 使用 tab 缩进，局部变量优先，固定名称使用大写常量，例如 `local ENTRY = "my_entry"`。
- 入口从普通 table 开始。不要用 hook 工具实例代替插件本身，也不要依赖自动创建字段的 metatable。
- 函数参数沿用项目约定。普通方法使用 `function plugin:init(plugin_data)`，hook 处理器使用
  `function handler(next, self, ...)` 并在适当位置调用 `next(self, ...)`。
- 模板名、声音 id、图集组名、动画 key 和语言键默认添加 entry 前缀。
- `require` 的插件内模块始终添加 entry 前缀。不要写可能命中其它插件的裸模块名。
- 数值调优优先放入 `<entry>_config.lua`，实现常量和模板字段放在对应模块顶部。不要把玩家设置、
  本体版本号、场景资源名散落在多个函数中。
- 伤害类型、地形位、Z 层和其它枚举使用本体常量。不要把整数直接写进逻辑。
- 将每个注册动作放在可追踪的位置。不要在模块顶层偷偷修改共享表，除非该模块就是一个明确的模板或
  数据声明文件。

## 生命周期

`init` 是唯一必需接口。启动时插件模块只会得到一次初始化调用。`reload` 运行在全新入口实例上，
但 `require` 子模块仍可能在缓存中。`unload` 必须撤销 hook、列表项、菜单项、纹理组、声音组、模板
覆盖和其它共享状态。已创建的场上实体不会因为卸载而自动恢复。

只要无法证明完整回滚，就不要实现三个可选接口。插件管理器发现缺少对应接口时会回退到保存并重启，
这是安全且受支持的行为。配置热加载的参数已经写入磁盘，`on_config_change(new_config)` 应直接使用
参数，不要重新读取旧文件。

## Hook 决策

优先级顺序如下：

1. 使用已有注册表或声明字段。
2. 使用模板模块在正确的加载阶段注册。
3. 直接修改明确的、由插件拥有的列表项。
4. 最后才使用 `hook_utils.HOOK`。

需要 hook 时保存处理器函数本身，以便 `UNHOOK` 使用同一个引用。处理器应保持责任链，不吞掉原始函数
的返回值，也不在每帧创建无必要的闭包或表。

## 结构取舍

- 英雄按声明、模板、动画、声音、文案和场景资源拆分。
- 防御塔按入口注册、模板、菜单、图鉴、动画、声音和资源拆分。
- generation 按代际描述符、地图数据、关卡、模板、资源和文案拆分。
- level 按入口、关卡数据、网格、路径、波次和资源拆分，网格与路径优先由地图编辑器生成。
