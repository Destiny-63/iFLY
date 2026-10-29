# 个人主页数据说明

个人主页（`/profile`）从以下 JSON 文件读取数据，可直接编辑以配置展示内容。

## profile.json

- **user**：用户信息（姓名、邮箱、等级 key、加入日期、简介等）；`bio`、`memberLevel` 等可配置多语种对象。
- **model**：当前使用的模型配置（模型名、API 地址、Key 脱敏、Token 总量/已用/剩余、会员到期、会员等级等）。真实密钥只放在项目根目录的 `.env`，不要把 AppId、API Key、API Secret 写进这个文件。
- **tokenUsage**：近几日 Token 消耗，用于「Token 消耗趋势」面积图；每项为 `{ date, input, output }`。

## stats.json

- **recentExams**：最近考试列表，用于「最近考试」卡片；每项为 `{ date, type, score, totalQuestions }`。
- **practiceByType**：各题型练习次数，用于「题型练习量」进度条；每项为 `{ type, count, label? }`，`label` 支持多语种。
- **scoreTrend**：分数趋势，用于「分数趋势」折线图；每项为 `{ date, score }`。
- **dailyPractice**：每日练习数，用于「每日练习」柱状图；每项为 `{ day, count }`。

修改保存后刷新个人主页即可生效。
