# 科技线插件

科技线模块返回包含 `techs`、可选 `patch` 的表，复用 `kr1.upgrades` 的六列
`archers`、`barracks`、`mages`、`engineers`、`rain`、`reinforcements`。

```lua
local H = require("kr1.upgrades.upgrade_utils")

local techs = {
	my_entry_archer_range = {
		class = "archers",
		icon = 14,
		level = 1,
		price = 1,
		range_factor = 1.05,
		patch = function(UP, u)
			H.scale_tower_attack_range(UP.archer_towers, u.range_factor)
		end,
	},
}

return {
	techs = techs,
}
```

入口把模块写入 `UP.list[ENTRY]`。每条科技必须有 `class`、`icon`、`level`、`price` 和购买后的
`patch(UP, u)`。自定义字段放在该科技表上。字段和文案 key 使用 entry 前缀。科技线没有注册 `unload`
的通用撤销机制，除非能恢复 `UP.list`、升级补丁和已写入的共享模板，否则不要声明热卸载。

## Upgrade 交付 Checklist

- [ ] `config.lua` 使用 `category = "upgrade"`，入口和模块路径与 entry 一致。
- [ ] 已从用户本体的 `kr1/upgrades.lua` 确认当前 `list`、`list_id`、`get_techs` 和 `patch_templates` 行为。
- [ ] 每条科技的 `class` 只使用 `archers`、`barracks`、`mages`、`engineers`、`rain` 或 `reinforcements`。
- [ ] 每条科技都有 1–6 的 `level`、有效 `icon`、`price`，自定义字段命名清楚且类型稳定。
- [ ] `patch(UP, u)` 只修改确定存在的模板和列表，批量模板访问对懒加载内容做存在性判断。
- [ ] 补丁顺序、重复执行结果和 `max_level` 限制已经按当前 `patch_templates` 逻辑核对。
- [ ] 模块注册到 `UP.list[ENTRY]`，科技线标题和每条科技文案都有语言键。
- [ ] 已检查科技线选择、存档读写、不同代际默认升级线和自制地图的最大科技等级。
- [ ] 已确认补丁对共享模板的副作用，无法逆向恢复时按重启路径交付。
