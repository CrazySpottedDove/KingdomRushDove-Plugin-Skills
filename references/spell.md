# 法术插件

法术通常由一个返回模块表的文件组成，例如 `<entry>/my_entry_spell.lua`。模块路径加入
`spell_system` 的 `module_names`，系统会读取 `name`、`i18n`、`control`、按钮图标、指针图标、海报、
`resources` 和等级方法。`name` 必须与模块文件名的最后一段一致。

```lua
local M = {}

M.name = "my_entry_spell"
M.i18n = "POWER_MY_ENTRY_SPELL"
M.control = "power_my_entry_spell_control"
M.button_icon = "in_game_icon_power_my_entry_spell"
M.pointer_icon = "pointer_power_my_entry_spell"
M.portrait = "power_portraits_big_my_entry_spell"
M.resources = {
	game = {
		required_textures = {},
		plugin_required_textures = {},
		required_sounds = {},
		plugin_required_sounds = {},
		required_exoskeletons = {},
		plugin_required_exoskeletons = {},
	},
}

function M.register_templates(E)
	local tt = E:register_t(M.control, "power_control_custom")
	-- 在这里设置 insert、update、选择范围和基础 cooldown
	E:set_template("user_power_3", tt)
end

function M.apply(level)
	local E = require("entity_db")
	local ctrl = E:get_template(M.control)
	-- 只按 1 到 6 级修改数值和开关
	ctrl.cooldown = 40
	if level >= 4 then
		ctrl.cooldown = 30
	end
end

return M
```

入口注册模块名，并注册声音和当前场景 UI 纹理：

```lua
require("lib.klua.table")
local plugin = {}
local SPELLS = require("spell_system")
local S = require("sound_db")
local ENTRY = "my_entry"

function plugin:init(plugin_data)
	table.arrayensure(SPELLS.module_names, ENTRY .. ".my_entry_spell")
	S:register_groups(require(ENTRY .. ".assets.sounds.groups"))
	S:register_sounds(require(ENTRY .. ".assets.sounds.sounds"))
end

return plugin
```

模板名和资源组使用 entry 前缀。`apply(level)` 在科技补丁前执行，不要在其中重新注册模板。法术文案
的 `_LARGE_DESCRIPTION` 对应 6 级最终效果，数值表达式应从模板和 `level` 推导。没有完整卸载注册表、
模板和声音的方案时，不实现可选热重载接口。

## 法术交付 Checklist

- [ ] 已从用户本体的 `kr1/spell_system.lua` 确认注册表名称、懒加载规则和必需字段。
- [ ] 模块文件名最后一段与 `M.name` 完全一致，模块路径已经加入 `spell_system.module_names`。
- [ ] 模块提供 `name`、`i18n`、`control`、按钮图标、指针图标、海报和当前版本要求的 `resources`。
- [ ] `resources.game` 的 required/plugin_required 纹理、声音和骨骼与实际文件逐项对应。
- [ ] `register_templates(E)` 只注册法术需要的控制器、弹道、特效、修饰器和召唤物。
- [ ] `user_power_3` 的绑定、选择范围、冷却、声音、插入和更新逻辑已经验证。
- [ ] `apply(level)` 覆盖 1 到 6 级边界，先重置基础值，再按等级应用差异，不重复注册模板。
- [ ] 伤害、地形和选择过滤使用本体常量与 helper，实体增删使用 simulation 队列。
- [ ] `POWER_<NAME>_NAME/DESCRIPTION/LARGE_DESCRIPTION` 与实际最终等级效果一致。
- [ ] 已验证未选中、选中、不同科技等级、不同地图上限、取消选择、施法和技能实体清理。
- [ ] 未实现无法完整撤销 `module_names`、模板和资源注册的热重载接口。
