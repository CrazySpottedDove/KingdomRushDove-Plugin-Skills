# 美术与资源管理

推荐目录：

```text
<entry>/
├── config.lua
├── <entry>.lua
├── assets/images/       # 图集描述符、.dds、.astc
├── assets/sounds/       # sounds.lua、groups.lua、.ogg
├── assets/strings/      # en.lua、zh-Hans.lua 等
└── data/                # animations.lua、其它数据
```

## 纹理

每个纹理组是一个 Lua 文件，返回精灵名到描述的表。`a_name` 指向桌面端 `.dds` 文件，描述中使用
`size`、`trim`、`a_size`、`f_quad` 和可选的 `alias`、`ref_scale`。桌面端常用 BC3 DDS，Android
常用 ASTC。一个插件包可以同时包含两种格式，服务端再按平台拆分。

```lua
return {
	my_entry_icon = {
		a_name = "my_entry_ui.dds",
		size = {64, 64},
		trim = {0, 0, 0, 0},
		a_size = {64, 64},
		f_quad = {0, 0, 64, 64},
		alias = {},
	},
}
```

在场景资源表中注册插件组，路径相对 `plugins/`，不要重复写 `plugins/`：

```lua
local game = require("game")
game.plugin_required_textures[ENTRY .. "_game"] = {
	use_bytecode = false,
	path = ENTRY .. "/assets/images",
}
```

英雄和法术的声明资源优先写入其 `resources` / 模块字段。只有场景没有现成注册入口时，才直接改
`game.plugin_required_textures`、`screen_map.plugin_required_textures` 或 `game_gui` 对应表。

## 声音

`groups.lua` 描述要加载的文件组，`sounds.lua` 描述音效 id。组名和音效 id 使用 entry 前缀，
`parent_dir` 指向 `assets/sounds`。注册后释放这两个模块的缓存，避免长期保留大表。

```lua
-- assets/sounds/groups.lua
return {
	my_entry_game = {
		files = {"my_entry_attack.ogg"},
		parent_dir = "my_entry/assets/sounds",
	},
}
```

```lua
require("lib.klua.table")
local S = require("sound_db")
S:register_groups(require(ENTRY .. ".assets.sounds.groups"))
S:register_sounds(require(ENTRY .. ".assets.sounds.sounds"))
table.arrayensure(game.plugin_required_sounds, ENTRY .. "_game")
package.loaded[ENTRY .. ".assets.sounds.groups"] = nil
package.loaded[ENTRY .. ".assets.sounds.sounds"] = nil
```

## 动画、骨骼和语言

- 动画定义放 `data/animations.lua`，在 `animation_db:load` 之后注册。动画 key 和真实精灵前缀必须匹配。
- 骨骼文件放 `assets/exoskeletons/`，在所属声明的 `plugin_required_exoskeletons` 中登记。
- 语言文件返回扁平表，至少同步 `en.lua` 和 `zh-Hans.lua`。语言键使用 entry 前缀。
- 初始化时用 `i18n:merge_locales(i18n.current_locale or i18n.default_locale, ENTRY .. ".assets.strings")`。
  只有需要跟随语言切换即时重载时才 hook `load_locale`，并且必须实现可逆的卸载。

## 打包与检查

`.png` 源图可以放在本地 `.backup/`，不上传。插件发布时保留 `.dds`、`.astc`、图集描述符和实际运行时
资源。不要手写或整目录重排已有图集，先使用项目认可的图集工具。跨平台检查使用本仓库的
`tools/krdove_plugin.py asset-check`，它只检查引用关系，不声称完成压缩或上传。

## 资源交付 Checklist

- [ ] 已根据用户本体的场景加载器确认资源应挂在 game、map、game_gui 还是声明模块上。
- [ ] 每个图集描述符的 `a_name`、`a_size`、`f_quad`、`size` 和 `trim` 与实际页面一致。
- [ ] 桌面端 `.dds` 和 Android `.astc` 的 basename 一致，缺少平台格式时已明确记录原因。
- [ ] 每个自定义动画 key 的 prefix 和帧范围都能在图集描述符中找到。
- [ ] 每个声音组文件、音效 id、`source_group`、loop、gain 和模板事件都已交叉检查。
- [ ] 每个语言 key 在至少中文和英文文件中存在，表达式可以在对应上下文求值。
- [ ] 骨骼文件路径、格式和 `plugin_required_exoskeletons` 的 key 与加载器一致。
- [ ] 运行 `asset-check`，再在实际场景查看纹理、动画、声音、骨骼和语言切换。
- [ ] 打包前移除 `.backup`、临时图集、缓存和不被运行时引用的源文件。
