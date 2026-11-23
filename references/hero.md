# 英雄插件

## 推荐结构

```text
<entry>/
├── config.lua
├── <entry>.lua
├── templates.lua
├── data/animations.lua
└── assets/{images,sounds,strings,exoskeletons}/
```

## 注册方式

使用 `heroes.registry` 的声明接口，不要把英雄列表直接写入旧式全局表：

```lua
local plugin = {}
local ENTRY = "my_hero"
local HERO_NAME = "hero_my_hero"
local HEROES = require("heroes.registry")

function plugin:init(plugin_data)
	HEROES:register({
		name = HERO_NAME,
		room = {
			available = {mode = "default"},
			stats = {5, 5, 5, 5},
			portrait_image = ENTRY .. "_portrait",
			thumb_image = ENTRY .. "_thumb",
			icon_image = ENTRY .. "_icon",
		},
		room_special_order = {"SKILL_A"},
		templates = {ENTRY .. ".templates"},
		animations = {ENTRY .. ".data.animations"},
		sounds = {ENTRY .. ".assets.sounds.sounds"},
		groups = {ENTRY .. ".assets.sounds.groups"},
		resources = {
			game = {
				required_textures = {},
				plugin_required_textures = {},
				required_sounds = {},
				plugin_required_sounds = {},
				required_exoskeletons = {},
				plugin_required_exoskeletons = {},
			},
			map = {
				required_textures = {},
				plugin_required_textures = {},
				required_sounds = {},
				plugin_required_sounds = {},
				required_exoskeletons = {},
				plugin_required_exoskeletons = {},
			},
		},
	})
end

return plugin
```

实际资源组应填入 `path = ENTRY .. "/assets/images"`，并根据场景填 `plugin_required_*`。模板文件在英雄
被选中、实体库正确加载时执行，模板依赖的脚本和子实体应在同一模块中按依赖顺序定义。技能显示顺序使用
`room_special_order`，文案使用 `HERO_ROOM_<HERO>_<SKILL>_NAME/DESC`。

## 模板和配置

`templates.lua` 直接取得 `E:get_template(HERO_NAME)` 后修改字段，或注册 entry 前缀的子模板。脚本使用
`tt.main_script`、`tt.hero` 和现有 `U` / `SU` API。玩家可调数值放 `<entry>_config.lua`，初始化时保存
配置或把配置传给模板注册函数。

## 生命周期

新英雄完整实现了 `HEROES:unregister`、所有注册表移除、模板重建和资源清理后，才可以实现 `unload`。
扩展本体英雄时，卸载不能注销本体英雄，而应移除插件模板和技能声明后重建本体模板。无法做到时省略
`reload`、`unload` 和 `on_config_change`，让管理器重启游戏。

## 英雄交付 Checklist

- [ ] 已在用户本体中确认 `heroes.registry` 的当前字段和 `room.available` 格式。
- [ ] 已递归列出英雄主模板、普通攻击、技能、召唤物、弹道、修饰器、特效和动画的全部引用。
- [ ] 新增英雄的模板名、模块名、声音、图集、动画和语言 key 都有 entry 前缀。
- [ ] 扩展本体英雄时只追加目标英雄模块的 `templates`、`room_special_order`、升级列表和资源，不注销本体声明。
- [ ] `resources.game` 与 `resources.map` 只登记实际使用的 required/plugin_required 项。
- [ ] `templates.lua` 在英雄模板可用的加载阶段执行，且模板依赖的脚本已经定义。
- [ ] `room_special_order` 与语言文件中的 `HERO_ROOM_<HERO>_<SKILL>_NAME/DESC` 一一对应。
- [ ] 每个英雄等级属性数组长度、技能等级数组和实际 `apply/level_up` 访问范围一致。
- [ ] 已检查英雄殿堂解锁、选中、局内插入、升级、技能、死亡、复活和多个英雄同时存在的情况。
- [ ] 已检查图集、动画、音效、骨骼、中文和英文文案，并通过工具校验。
- [ ] 未实现无法完整回滚的热重载接口。
