---
created: 2026-04-30
tags:
  - emulator
  - neo-geo
  - nds
---

# NeoDS 模拟器使用指南

NeoDS 是一款在 Nintendo DS 上运行 Neo Geo AES/MVS 游戏的模拟器，由 Ben Ingram 于 2008 年开发。

## 项目概述

### 核心功能

**已支持：**
- M68000 CPU（使用 Cyclone 核心）
- Z80 CPU（使用 DrZ80 核心）
- NeoGeo 所有保护/加密机制
- 图形系统
- ADPCM 音频
- PSG 音频

**未支持：**
- FM 音频
- 光栅效果
- 多人游戏
- 部分时序不够精确

### 技术架构

- **ARM7**: 负责音频处理（ADPCM、PSG）
- **ARM9**: 负责主模拟逻辑、图形渲染
- **图形渲染**: 使用 DS 3D 硬件绘制纹理四边形
- **数据流**: 从烧录卡持续流式加载图形、声音和程序代码

---

## ROM 转换工具：NeoDSConvert

### 编译方式

#### Windows（推荐）
NeoDSConvert 是一个 Visual Studio 项目：

1. 打开 `NeoDsConvert/NeoDsConvert.sln`
2. 在 Visual Studio 中构建项目
3. 输出 `NeoDSConvert.exe`

项目依赖已包含在源码中：
- **zlib 1.2.3**（`zlib-1.2.3/` 目录）
- **Minizip**（`Minizip/` 目录）

### 使用方法

#### 基本用法

将游戏 ROM 和 BIOS 与 `NeoDSConvert.exe` 放在同一目录：

```
C:\roms\
├── mslug.zip          # NeoGeo 游戏 ROM
├── neogeo.zip         # BIOS ROM
└── NeoDSConvert.exe   # 转换工具
```

运行转换：

```bash
# 转换当前目录下所有 ROM
NeoDSConvert.exe

# 转换指定游戏（带 BIOS 选项）
NeoDSConvert.exe -bios6 mslug
```

#### 命令行参数

| 参数 | BIOS 类型 | 地区 |
|------|-----------|------|
| `-bios0` | Euro | 欧洲 |
| `-bios1` | Euro-S1 | 欧洲 S1 |
| `-bios2` | US | 美国 |
| `-bios3` | US-E | 美国 E |
| `-bios4` | Asia | 亚洲 |
| `-bios5` | Japan | 日本 |
| `-bios6` | Japan-S2 | 日本 S2 |
| `-bios7` | Japan-S1 | 日本 S1 |
| `-bios8` | Uni-bios 1.0 | 通用 |
| `-bios9` | Uni-bios 1.1 | 通用 |
| `-bios10` | Debug | 调试 |
| `-bios11` | Asia-AES | 亚洲 AES 家用机 |

#### 推荐 BIOS

```bash
# 使用 Uni-bios（最佳兼容性）
NeoDSConvert.exe -bios8 mslug3

# 日本版（兼容性好）
NeoDSConvert.exe -bios6 mslug3
```

### 转换结果

成功后会在同一目录生成 `.neo` 文件：

```
C:\roms\
├── mslug3.neo         ← 转换后的 ROM（用于 NDS）
├── mslug3.zip         ← 原始 ROM
└── neogeo.zip         ← BIOS
```

---

## NeoDS 社区改进版本

### dACE 修改版（neoDS_021）

在 GBAtemp 社区中，用户 **dACE** 基于官方 v0.20 版本制作了改进版，解决了原版的一些限制：

#### 主要改进

1. **ROM 数量限制提升**
   - 从 64 个增加到 256 个 ROM

2. **ROM 目录支持**
   - ROM 可以存放在单独的目录中（通过 `_NeoDs.ini` 配置）
   - 不再强制要求放在烧录卡根目录

3. **配置文件整理**
   - 所有配置文件存储在 `fat:/data/neoDS/` 目录
   - 保持根目录整洁

4. **操作优化**
   - D-pad 左/右对应 PageUp/PageDown

#### 获取方式

改进版可通过 filetrip 下载：[neoDS_021](http://www.mediafire.com/file/zy6k4s6pp9741wr/NeoDS_0.2.1.rar/file)

源码托管在 GitHub：https://github.com/Yardape8000/NeoDS

![[assets/2026/NeoDS-模拟器使用指南/IMG-20260430171341273.png]]

---

## NeoDSConvert 执行过程详解

### 转换流程

1. **扫描阶段**
   - 程序启动后遍历内置的游戏列表（约 150+ 个游戏）
   - 输出 `"Looking for xxx..."` 提示正在查找每个游戏
   - 对每个游戏尝试打开对应的 `.zip` 文件

2. **ROM 加载阶段**
   ```
   Looking for mslug3...
   Opening ROM file: 261-p1.bin      ← 开始读取 ZIP 内文件
   Loading ROM data: offs=0 len=10000 mask=FF group=1 skip=0 reverse=0
   Verifying length (10000) and checksums
   Verify finished                     ← 校验通过
   Closing ROM file
   ```

3. **后处理阶段**
   ```
   Post-processing region 81
   + datawidth=1 little=1
   + Byte swapping region              ← 字节序转换
   ```
   - 对不同区域进行字节序转换和数据重组
   - 优化精灵图和 Tile 数据格式

4. **写入 .neo 文件**
   - 将处理后的数据写入单一 `.neo` 文件
   - 包含所有必要的区域数据和元信息

### 常见问题排查

#### 转换失败：没有生成 .neo 文件

**可能原因：**

1. **BIOS 文件不完整** ⚠️ 最常见
   ```
   Opening ROM file: aes-bios.bin
   Missing file
   Opening ROM file: sfix.sfx
   Missing file
   ```

   **解决：** 获取完整的 MAME 兼容 `neogeo.zip`，必须包含：
   - `neo-geo.rom` (主 BIOS)
   - `sfix.sfx`
   - `sm1.sm1`
   - `000-lo.lo`

2. **游戏名称不正确**
   ```bash
   # 使用正确的 MAME ROM 名称
   NeoDSConvert.exe -bios6 mslug3    # 正确：标准名称
   NeoDSConvert.exe -bios6 mslug3h   # 错误：hack 版本可能不被支持
   ```

3. **ZIP 文件内部结构问题**
   - NeoDSConvert 需要 ZIP 内的文件名与 MAME 定义完全匹配
   - 例如：`mslug3.zip` 内必须包含 `261-p1.bin`、`261-c1.bin` 等

4. **缺少父 ROM**
   - 某些 hack/修改版本需要原始 ROM 作为父级
   - 解决：使用标准 ROM 名称，或同时提供父 ROM ZIP

#### 转换成功但游戏无法运行

| 症状 | 可能原因 |
|------|----------|
| 黑屏 | ROM 不完整或使用了不支持的 hack 版本 |
| 卡在某画面 | 加密/保护机制未正确处理 |
| 无声音 | FM 音频未被模拟（正常） |
| 图形错乱 | BIOS 不匹配或 Tile 数据有问题 |

### 验证源 ROM

在转换前用 MAME 验证：

```bash
# 先用 MAME 测试
mame64 mslug3

# 如果 MAME 也无法运行，说明 ROM 本身有问题
```

### 批量转换技巧

```bash
# 不带参数运行会转换所有找到的游戏
NeoDSConvert.exe -bios6

# 观察输出中哪些游戏成功转换
# 成功的标志是最后没有 "Missing file" 错误
```

### 转换日志解读

**成功转换的典型输出：**
```
Looking for sengoku3...
Opening ROM file: 000-lo.lo
Loading ROM data: offs=0 len=10000 ...
Verifying length (10000) and checksums
Verify finished
Closing ROM file
...（多个文件加载）...
Post-processing region 9A
+ datawidth=2 little=0
+ Byte swapping region
← 此处会生成 sengoku3.neo
```

**失败转换的典型输出：**
```
Looking for mslug3...
Opening ROM file: 261-p1.bin
Missing file                    ← 关键错误
← 不会生成 .neo 文件
```

---

## 在 NDS 上使用

### 准备工具

**必需：**
- Nintendo DS (Lite)
- DLDI 兼容的烧录卡

**可选：**
- Slot2 扩展内存卡（如 SuperCard lite），可提升性能

### 加载到烧录卡

1. 为 `NeoDS.nds` 打上 DLDI 补丁（如需要）
2. 将以下文件复制到烧录卡根目录：
   - `NeoDS.nds`（模拟器主程序）
   - `*.neo`（转换后的 ROM）

### 控制方式

| NDS 按键 | NeoGeo 功能 |
|----------|-------------|
| 方向键 | 方向键 |
| A, B, X, Y | 面 buttons |
| Start | Start |
| Select | 投币 |

### GUI 设置（触控笔操作）

- **Video:** Normal（裁剪）或 Scaled（完整缩放）
- **CPU Clock:** 可降频以提升性能
- **Screen Off:** 关闭下屏
- **Load rom:** 加载新游戏

> **注意：** 无音频模式可提升帧率，但需重新加载游戏才能恢复声音。部分游戏在无音频模式下会冻结。

---

## NeoGeo BIOS 说明

### BIOS 版本

NeoDS 支持 12 种不同的 BIOS：

| 编号 | 名称 | 地区 | 说明 |
|------|------|------|------|
| 0 | Euro | 欧洲 | 欧洲版 |
| 1 | Euro-S1 | 欧洲 | 欧洲 S1 版 |
| 2 | US | 美国 | 美国版 |
| 3 | US-E | 美国 | 美国 E 版 |
| 4 | Asia | 亚洲 | 亚洲版 |
| 5 | Japan | 日本 | 日本版 |
| 6 | Japan-S2 | 日本 | 日本 S2 版 |
| 7 | Japan-S1 | 日本 | 日本 S1 版 |
| 8 | Uni-bios 1.0 | 通用 | 通用 BIOS 1.0 ⭐ |
| 9 | Uni-bios 1.1 | 通用 | 通用 BIOS 1.1 ⭐ |
| 10 | Debug | - | 调试 BIOS |
| 11 | Asia-AES | 亚洲 | 亚洲 AES 家用机版 |

⭐ 推荐使用 Uni-bios，兼容性最好

### BIOS 文件组成

完整的 `neogeo.zip`（MAME 标准）包含：

```
neogeo.zip
├── neo-geo.rom      (主 BIOS，2MB)
├── sfix.sfx         (SFIX ROM，128KB)
├── sm1.sm1          (SM1 ROM，128KB)
├── 000-lo.lo        (LO ROM，64KB)
├── sp-s2.sp1        (可选，日本 S2)
├── sp-s1.sp1        (可选，日本 S1)
├── sp-euro.sp1      (可选，欧洲)
└── vs-bios.rom      (可选，US/EU)
```

### BIOS 更新状态

- **不会频繁更新**：NeoGeo 是 1990 年的硬件，BIOS 是从真实芯片中提取的
- **MAME 驱动稳定**：NeoGeo BIOS 定义已经多年稳定
- **只需一个完整的 neogeo.zip** 即可转换所有游戏

---

## UniBIOS 详解

### 什么是 UniBIOS

UniBIOS 是由 Anthony Young 开发的 NeoGeo 通用 BIOS，旨在替代官方 NeoGeo BIOS，提供更强大的功能和更好的兼容性。它支持 AES（家用机版）和 MVS（街机版）双模式。

官方网站：http://unibios.free.fr/

### UniBIOS 主要功能

#### 1. 区域自由启动
- 可以运行任何地区的游戏卡带
- 自动检测并适配游戏区域
- 解决原版 BIOS 的区域锁定问题

#### 2. 作弊码支持
- 内置金手指功能
- 可在游戏中启用/禁用作弊
- 支持自定义作弊码

#### 3. CD/DAC 音乐测试
- 允许播放游戏中的音乐曲目
- 适用于支持 CD 音轨的 NeoGeo CD 游戏

#### 4. 内存查看器
- 实时查看游戏内存状态
- 用于调试和开发

#### 5. DIP 开关设置
- 可配置街机模式的 DIP 设置
- 调整难度、投币数等参数

#### 6. 多 BIOS 兼容
- 整合了多个官方 BIOS 版本
- 包括日本、美国、欧洲等地区的 BIOS
- 可以在启动时选择使用的 BIOS 版本

### UniBIOS 在模拟器中的优势

**为什么推荐使用 UniBIOS：**

1. **最佳兼容性**：能运行几乎所有 NeoGeo 游戏，不受区域限制
2. **功能丰富**：内置作弊码、DIP 设置等实用功能
3. **简化配置**：无需为不同区域的游戏切换不同的 BIOS
4. **开发友好**：提供调试工具，适合自制软件开发

### UniBIOS 版本选择

UniBIOS 针对不同硬件平台提供了两个版本：

| 版本 | 适用平台 | 说明 |
|------|----------|------|
| **v4.0** | MVS / AES | 街机基板 / 家用机卡带系统 ⭐ |
| **v3.3** | CD | NeoGeo CD 系统 |

**对于 NeoDS 模拟器：**
- ✅ **推荐使用 v4.0 (MVS/AES)**
- ❌ v3.3 (CD) 不适用于 NeoDS

**原因：**
- NeoDS 模拟的是卡带版 NeoGeo (AES/MVS)
- v4.0 针对卡带游戏优化，提供更好的兼容性
- v3.3 专为 CD 音轨设计，NeoDS 不支持 CD 功能

### UniBIOS 文件

常见的 UniBIOS ROM 文件：
- `uni-bios_1_0.rom` - 早期版本（NeoDS 内置）
- `uni-bios_1_1.rom` - 改进版本（NeoDS 内置）
- `uni-bios_4_0.rom` - 最新 v4.0 版本（推荐用于 MVS/AES）

在 NeoDS 中，使用以下参数启用 UniBIOS：
- `-bios8` → Uni-bios 1.0
- `-bios9` → Uni-bios 1.1

### 获取 UniBIOS

UniBIOS 可以从其官方网站下载：http://unibios.free.fr/

**下载建议：**
- 选择 **"Download v4.0 for MVS / AES"**
- 将下载的 BIOS 文件放入 `neogeo.zip` 中
- 或在转换时使用 `-bios8` / `-bios9` 参数

---

## NeoDSConvert 实战经验总结

### 目录结构要求（关键）⭐

```
工作目录/
├── NeoDSConvert.exe      ← 必须在当前目录
├── neogeo.zip            ← BIOS（必须完整）
├── mslug3.zip            ← 游戏 ROM
└── （其他游戏.zip）
```

**重要注意事项：**
1. **ROM 文件名区分大小写**：在 Linux/macOS 下尤其注意
2. **ZIP 内部文件名必须匹配 MAME 定义**：不能随意修改 ZIP 内的文件名
3. **BIOS 和游戏 ROM 必须在同一目录**

### 推荐的工作流程

```bash
# 1. 创建工作目录
mkdir neods_work && cd neods_work

# 2. 复制工具
cp /path/to/NeoDSConvert.exe .
cp /path/to/neogeo.zip .
cp /path/to/mslug3.zip .

# 3. 验证文件存在
ls -la *.zip NeoDSConvert.exe

# 4. 先尝试单个游戏
NeoDSConvert.exe -bios6 mslug3

# 5. 检查是否生成 .neo
ls -la *.neo

# 6. 成功后批量转换
NeoDSConvert.exe -bios6
```

### BIOS 完整性检查

解压 `neogeo.zip` 后应该看到类似这样的文件列表：

```
neogeo.zip contents:
├── neo-geo.rom        (2MB)   ← 主 BIOS
├── sfix.sfx           (128KB) ← SFIX
├── sm1.sm1            (128KB) ← SM1
├── 000-lo.lo          (64KB)  ← LO
├── sp-s2.sp1          (128KB) ← 日本 S2 BIOS
├── sp-euro.sp1        (128KB) ← 欧洲 BIOS
└── vs-bios.rom        (128KB) ← US/EU BIOS
```

如果缺少关键文件（如 `sfix.sfx`、`sm1.sm1`），转换会失败。

### 常见错误信息解读

| 错误信息 | 含义 | 解决方法 |
|----------|------|----------|
| `Missing file` | ZIP 内找不到需要的文件 | 检查 ZIP 内容或更换 ROM |
| `Bad file` | ZIP 损坏或加密 | 重新下载 ROM |
| `Can't find parent: xxx` | 缺少父 ROM | 提供父 ROM ZIP 或使用标准版 |
| `Failed to open parent: xxx` | 父 ROM 打开失败 | 父 ROM 文件损坏或不完整 |

### 性能优化建议

1. **使用 Slot2 扩展内存**
   - 如果有支持 RAM 的 Slot2 卡（如 SuperCard lite）
   - NeoDS 会自动利用额外内存缓存更多数据
   - 可显著提升某些游戏的性能

2. **CPU 降频**
   - 在 GUI 中降低 CPU 频率
   - 对于不依赖全速运行的游戏可以提高帧率

3. **关闭音频**
   - 加载时选择无音频模式
   - 牺牲声音换取性能（部分游戏会冻结）

### Hack ROM 处理

Hack 版本（如 `mslug3h`、`kf2k3pl`）的转换要点：

1. **确认父 ROM 存在**：大多数 hack 需要原版 ROM
2. **使用正确的名称**：参考 MAME 的 ROM 定义
3. **兼容性不确定**：部分 hack 使用了未模拟的特性

**推荐的 hack ROM 来源：**
- PicoDrive/MAME 兼容的 ROM 集合
- 专门用于其他模拟器的 NeoGeo ROM

### 调试技巧

```bash
# 查看详细的转换日志
NeoDSConvert.exe -bios6 mslug3 2>&1 | tee convert.log

# 搜索关键错误
grep -i "missing\|error\|fail" convert.log

# 检查生成的文件
file *.neo
hexdump -C mslug3.neo | head -20
```

---

## 社区常见问题汇总（GBAtemp）

### ROM 存储位置问题

**原始版本限制：**
- ROM 必须放在烧录卡根目录
- 配置文件也写在根目录

**解决方案：**
- 使用 dACE 修改版（neoDS_021），支持自定义 ROM 目录
- 或通过 `_NeoDs.ini` 配置 ROM 路径

### ROM 数量限制

**原始版本：** 最多 64 个 ROM
**改进版本：** 最多 256 个 ROM

### 缩放显示问题

社区用户反馈希望默认启用缩放显示，该设置可以按游戏存储在 cfg 文件中。

### 已知转换成功的 ROM 数量

根据社区讨论，大多数 MAME 兼容的 NeoGeo ROM 都可以成功转换，但具体数量取决于：
- BIOS 完整性
- ROM 版本匹配度
- 是否使用了正确的 MAME ROM 集合

---

## 已知可运行的游戏

根据实际测试，以下游戏可以成功转换和运行：

![[assets/2026/NeoDS-模拟器使用指南/IMG-20260430171341310.png]]

### 合金弹头系列
- `mslug` - 合金弹头 1 ✅
- `mslug2` - 合金弹头 2 ✅
- `mslug3` - 合金弹头 3 ✅
- `mslug4` - 合金弹头 4 ✅
- `mslug5` - 合金弹头 5 ✅

### 拳皇系列
- `kof94` ~ `kof2003` - 拳皇系列多部作品 ✅

### 侍魂系列
- `samsho` ~ `samsho5` - 侍魂系列多部作品 ✅

### 其他 SNK 经典
- `sengoku3` - 战国传承 3 ✅
- `garou` - 饿狼传说：月之使徒 ✅
- `rbff` 系列 - _real_ & _Fatal Fury_ 系列 ✅
- `aof` 系列 - 龙虎之拳系列 ✅
- `ssideki` 系列 - 超兽机神断空我 ✅

### 注意事项
- 部分 hack/修改版本可能需要额外的父 ROM
- 某些使用特殊保护的游戏可能无法正常运行
- FM 音频未被模拟，依赖 FM 音效的游戏会有声音缺失

---

## 参考资料

- 官方文档：`readme.txt`
- 源码路径：`NeoDsConvert/NeoDsConvert/`
- MAME 项目：https://www.mamedev.org/
- GBAtemp 讨论：
    - [NeoDS Update 帖子](https://gbatemp.net/threads/neods-update.374204/)
    - [NeoDS Names & Compatibility List](https://gbatemp.net/threads/neods-names-compatibility-list.102177/)
    - [NeoDS - A Guide to Using One of the Greatest DS Emulators](https://gbatemp.net/threads/neods-a-guide-to-using-one-of-the-greatest-ds-emulators.291225/)
- GBADev 论坛：https://www.gbadev.org/

