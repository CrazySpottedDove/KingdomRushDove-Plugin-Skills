# 插件元数据与玩家配置

## `config.lua`

最小元数据包含以下字段：

```lua
return {
	name = "插件名称",
	entry = "my_entry",
	version = "0.1.0",
	desc = "插件功能的简短描述",
	url = "",
	by = "作者名称",
	category = "other",
	enabled = true,
	priority = 0,
	branch = "master",
	min_version = "2.1.1.3",
}
```

`name`、`entry`、`version`、`desc`、`url`、`by`、`category`、`enabled` 和 `priority` 必须有值。
`branch`、`min_version` 和 `release_version` 是可选字段。当前游戏插件管理器支持
`gameplay`、`tower`、`hero`、`display`、`cosmetic`、`enemy`、`level`、`upgrade`、`generation`、
`spell` 和 `other`。科技线使用 `upgrade`，代际内容使用 `generation`，法术使用 `spell`。

`entry` 是唯一标识。它必须是 Lua 模块安全的 ASCII 标识符，且同时匹配插件目录名和入口文件名。
`priority` 越小越早初始化。只有确实需要覆盖其它插件时才设置非零优先级。

`min_version` 从目标游戏 `version.lua` 的 `id` 读取。只有使用了较新本体 API、资源或字段时才需要把它
提高到对应版本。不要凭记忆填写，也不要把插件版本写入 `min_version`。

`branch = "dev"` 和 `release_version` 只用于开发预览渠道。发布正式插件时使用 `master`，不填写无关的
`release_version`。

## `<entry>_config.lua`

玩家配置文件是可选的。只放玩家确实需要调整的数字、布尔值、字符串和一维数组。每个可编辑键都要登记
在 `key_label_map` 中，显示顺序可用 `key_order_list` 指定。不要手写 `__default_config`，由游戏维护。

```lua
return {
	attack_cooldown = 1,
	use_true_damage = false,
	key_label_map = {
		attack_cooldown = "攻击冷却（秒）",
		use_true_damage = "造成真实伤害",
	},
	key_order_list = {"attack_cooldown", "use_true_damage"},
}
```

插件中用 `require("<entry>.<entry>_config")` 读取。配置变更后，只有实现完整的
`on_config_change` 才能即时应用，否则让插件管理器重启游戏。

## 描述文本

`desc` 是商店和管理器中的短描述。它应说明玩家能看到的效果、适用范围和明显限制。不要把实现细节、
未完成功能或热重载承诺写入描述。需要更长的故事和更新记录时放入 `README.md`。
