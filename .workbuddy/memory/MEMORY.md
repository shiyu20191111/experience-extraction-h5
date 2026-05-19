# MEMORY.md - 长期记忆

## 项目关键信息

### 经验萃取H5项目
- **本地路径**: `/Users/zhangshiyu/WorkBuddy/2026-05-08-task-5/experience-extraction-h5/`
- **GitHub**: `shiyu20191111/experience-extraction-h5`
- **最新Tag**: `v0519-04`
- **线上地址**: `https://shiyu20191111.github.io/experience-extraction-h5/`

### 核心代码结构
- `index.html`: 主文件，包含完整流程（4步骤）
- 乱写检测函数：`_isGibberishGlobal()` 和 `_isSloppyTopicGlobal()` 为全局函数，`detectSloppy()` 调用它们
- `generateSuggestions()`: 生成修改建议，乱写时直接return，不生成常规建议
- `_sloppyResult`: 全局缓存乱写检测结果，供步骤4报名按钮和步骤3验证按钮使用

### 乱写检测逻辑（当前版本 v0519-04）
- 选题：纯数字 / 含敷衍词 / 中文字符<4 → 乱写
- 文本字段（萃取价值/弯路教训/期望效果/目标学员）：敷衍词 / 中文字符<3 → 乱写
- 触发条件：选题乱写 + ≥1个文本乱写，或 ≥2个文本乱写（选题正常）
- 三维度全100分 **不触发**乱写检测

### 关键版本记录
| Tag | 内容 |
|-----|------|
| v0519-04b | 修复返回按钮；删除"数据不会保存"提示；添加验证状态字段；乱写也保存数据 |
| v0519-04 | 无成功案例拦截；乱写建议具体到字段；乱写不可验证；验证按钮灰化 |
| v0519-03 | 删除参赛旅程口号；三维度100不触发重写；新增一言难尽等敷衍词 |
| v0519-02 | 提交报名维度 + 乱写词库升级 + 按钮灰化 |
| v0519-01 | 乱写检测初代版 |

### 重要修复记录（2026-05-19）
- **返回按钮bug**: 原来步骤3的"返回修改"按钮调用了 `goToStep2()`（会验证步骤1必填），改为 `goBackToStep2()`（只切换显示）
- **isGibberish函数名错误**: generateSuggestions中调用了不存在的 `isGibberish()`，应改为 `_isGibberishGlobal()`
- **验证状态字段**: `formData.verificationStatus` = "完成验证" 或 "需要重写"，无论是否乱写都保存数据
- **提示文字优化**: 删除"本次填写的数据不会被保存"表述

## 用户偏好
- 偏好AI端到端处理，不喜欢手动步骤
- 输出格式：结构化Markdown
- 测试要求：充分验证后交付
