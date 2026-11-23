# 地图插件

地图插件的重点是数据文件，不需要把地图逻辑塞进入口。推荐结构如下：

```text
<entry>/
├── config.lua                 # category = "level"
├── <entry>.lua                # 只保存必要的 init
├── data/levels/<entry>.lua
├── data/levels/<entry>_data.lua
├── data/levels/<entry>_grid.lua
├── data/levels/<entry>_paths.lua
├── data/levels/<entry>_metadata.lua
├── data/waves/<entry>_waves_campaign.lua
├── data/waveconfigs/<entry>_waves_campaign_config.lua
└── assets/images/
```

入口可以只保存 `plugin_data`。不要为了看起来完整而写空的 `reload` 或 `unload`。地图编辑器生成的
`grid`、`paths`、实体列表和波次优先保留其格式，不要手写巨大矩阵或曲线。

`data/levels/<entry>.lua` 提供 `level:init(store)` 和 `level:update(store)`。`init` 中的模板修改只
作用于当前关卡，`update` 通过 `LU.insert_hero(store)` 和协程等待波次结束。`<entry>_data.lua` 注册
`plugin_required_textures`、实体、地形、导航网格和模式覆盖。战役波次文件是必需的，英雄和铁人波次可选。

元数据的 `category` 是 `normal`、`challenge` 或 `creative`，与插件 `config.lua` 的 `category = "level"`
不同。背景图描述符的 `a_name` 指向 `.dds`，同时提供 Android `.astc`。地图目录和所有 key 使用 entry
前缀，避免与其它自制关卡冲突。

地图插件只有在能够完整移除关卡注册和资源时才提供热卸载。通常省略可选热接口并让管理器重启，尤其是
地图已被当前场景或存档引用时。

## generation 分类

如果需求是添加一整套代际地图，而不是单个自制关卡，插件 `config.lua` 使用
`category = "generation"`，入口向 `generations.registry` 注册一个代际模块。代际模块通常调用
`kr1.generations.common.standard`，在 `gen.lua` 中提供地图点、动画、装饰、关卡数据、图鉴、通知、
关卡范围、音乐和 `resources.map`。具体实现仍需按当前目标代码重新编写和验证。

## Level / Generation 交付 Checklist

- [ ] 单地图插件使用 `category = "level"`，代际插件使用 `category = "generation"`。
- [ ] 已从用户本体确认 `generations.registry`、`kr1.generations.common` 和关卡加载器的当前字段。
- [ ] 单地图目录中的入口、关卡脚本、数据、网格、路径、元数据、战役波次和资源文件都带 entry 前缀。
- [ ] `data/levels/<entry>_data.lua` 的实体、地形、导航网格、模式覆盖和资源声明均能解析。
- [ ] `level:init(store)` 只做本图调整，`level:update(store)` 使用当前 `level_utils` 和协程约定。
- [ ] `campaign` 波次存在，`heroic`/`iron` 文件和编辑器配置与界面显示一致。
- [ ] 塔位、出怪点、防守点、背景图和路径编号能够在地图中对应起来。
- [ ] generation 模块的 `name`、`resource_root`、地图数据、`ranges`、音乐、图鉴、通知和升级线齐全。
- [ ] 已验证选关、地图加载、建塔、英雄、波次、三种模式、胜负、回到地图和存档进度。
- [ ] 地图或代际注册难以完整回滚时不实现热卸载接口。
