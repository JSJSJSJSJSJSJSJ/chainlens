# 验收记录

验收日期：**2026-09-16**。信息截止日：**2026-09-16**。数据集 `2026-09-16.v1`；评分规则 `1.0.0`。以下“通过”指本地实际执行结果，不表示 GitHub CI 已运行或资料已经由项目作者复核。

## 十项要求映射

| 要求 | 对应实现 | 实际验证 | 剩余边界 |
| --- | --- | --- | --- |
| 1. 研究范围 | 固定快照与上市身份目录；NVIDIA + 13 家，22 条关系 | 正式快照导入、统计及结构测试通过 | 精选样本，未穷尽供应链 |
| 2. 五类关系、方向与状态 | supplier/customer 相对转换；投资有向；partner/peer 对称；事实与人工复核独立 | 五类覆盖、反向查询、投资方向测试通过 | 正式关系均为限定范围 confirmed；推断/不足状态通过合成数据验证 |
| 3. 合法公开资料 | SEC、公司年报及官方公告；逐条 URL、定位、短摘录与限制 | 13 个原始关系 URL 已打开读取；14 个证据记录 | 许可未知则不分发全文；没有批量爬取授权 |
| 4. 证据与数据质量 | 多对多关联；独立来源 key 与摘录 hash 合并；反驳立场、未知时间、实体映射 | 重复来源、冲突、日期未知、母子链、非法引用和历史关系测试通过 | 未在真实样本中确立现实冲突；作者审核均 pending |
| 5. 可解释评分 | 独立 Score 表；确定性分项、版本、解释、时间；持续性另判 | 分项求和、重复不加分、冲突扣分、状态封顶、时效性及金额不影响评分测试通过 | 人为规则未做统计校准，不是投资建议 |
| 6. 公开 GitHub 与采集清洗说明 | README、研究日志、方法论、CI 工作流、Apache 代码许可证、忽略规则 | 本地文件、锁文件与资料清单齐全；未执行推送 | **GitHub 发布尚未完成**；已有远程地址不等于公开发布和推送授权 |
| 7. API 与 CLI | 全部七个 HTTP 端点及公司/关系/图/证据 CLI；共享 ResearchService | API/CLI JSON 一致、404/422、过滤分页稳定排序通过 | 面向小规模本地读服务，无账号系统 |
| 8. 可复现运行 | uv.lock、pnpm-lock.yaml、快照 manifest、幂等导入、独立数据库回溯 | 新 Python 虚拟环境使用锁文件离线重装成功；新空库首次 imported、再次 unchanged；前端冻结锁安装通过 | 首次安装依赖与浏览器需联网；源内容更新需独立人工研究 |
| 9. 测试与限制 | pytest、Ruff、TypeScript、Vitest、Vite、Playwright | **39 后端 + 5 组件 + 2 浏览器测试通过**；类型、构建、校验通过 | 本机 Windows/Chromium；未实际运行 Linux CI、Firefox、WebKit 或全面无障碍审核 |
| 10. AI 使用披露 | ai-usage.md、研究日志与 pending 标记 | 记录实际工具、用途、校验方法及作者待确认项 | AI 辅助核验不能代替作者审核 |

## 已运行检查

在 Windows、Python 3.12.14、Node.js 24.19.0、uv 0.11.28、pnpm 11.19.0 上验证。锁定核心版本：FastAPI 0.141.1、Pydantic 2.13.5、SQLAlchemy 2.0.54、Typer 0.27.2；React 19.2.0、TypeScript 5.9.3、Vite 7.3.1、Vitest 4.0.18、Playwright 1.58.1。

| 命令 / 检查 | 结果 |
| --- | --- |
| `uv sync --frozen --offline`，另设新的虚拟环境目录 | 成功，按锁安装31个包（使用首次联网安装后的本地缓存） |
| `pnpm --dir frontend install --frozen-lockfile --offline` | 成功，无锁文件漂移 |
| `uv run chainlens import-snapshot --json`，新库重复两次 | imported → unchanged；14家公司、22关系、14证据 |
| `uv run chainlens health --json` | 返回 ok、数据集/截止日/规则版本 |
| `uv run pytest -q` | **39 passed** |
| `uv run ruff check backend` | All checks passed |
| `uv run python scripts/snapshots.py verify --manifest data/snapshots/manifest.json` | valid=true，所有摘要匹配 |
| 同版本 `scripts/snapshots.py compare` | 三类记录均无新增、删除、修改 |
| `pnpm --dir frontend typecheck` | 通过 |
| `pnpm --dir frontend test` | **5 passed** |
| `pnpm --dir frontend build` | 成功；JS约443KB，gzip约145KB；未超默认构建警告阈值 |
| `pnpm --dir frontend e2e` | **2 passed**，真实后端和固定快照，无 API mock |
| `git diff --check` | 通过 |

本机 pnpm 不在 PATH，实际通过其已有运行时路径或 `scripts/frontend.ps1` 调用。部分前端命令因 Windows 沙箱不允许写入 Vite 缓存而首次失败，取得执行许可后完成测试；未把沙箱启动失败记录为通过。依赖安装和 Playwright 浏览器首次下载也显式在允许网络后执行。

后端有两条第三方弃用提示：Starlette TestClient 的 httpx 兼容层、AnyIO BlockingPortal 别名。它们未造成测试失败，暂不隐藏警告。Playwright 的 NO_COLOR/FORCE_COLOR 提示也不影响流程。

## 浏览器检查与修复

真实流程：页面载入 → 供应商过滤 → TSMC 详情 → SEC 证据与评分解释 → Esc 关闭 → 同条件关系图 → 点击图边 → 历史 ASUS 客户 → 关键词空结果 → 清除筛选 → 完整22边关系图。

手机流程：390×844 → 检查页面无全局横向溢出 → 键盘打开详情 → Esc 恢复焦点 → 输入截止日后的日期 → 显示后端统一错误 → 重置恢复。表格在自身容器内水平滚动，页面主体不横向溢出。

首轮发现并修复：筛选 select 的精确可访问名称匹配问题；表格隐藏标题绝对定位越过滚动容器，导致手机页面横向溢出。修复后两条浏览器流程通过。桌面、手机、证据抽屉与完整图的实际截图也已读取检查，没有把静态 mock 当作集成完成。

## 交付前仍需作者完成

1. 人工复核研究解释与上市主体映射；尤其是旧 ASUS 客户证据、历史投资与当前持股的区别。
2. 发布前检查第三方短摘录与来源条款，确认 GitHub 目标及推送授权，再提交、推送与验证远程 CI。
3. 如要部署公共站点，另行配置静态托管和 API 反向代理；当前交付已满足本地演示和复现，未声称生产部署完成。

评分样例与权重见 [methodology.md](methodology.md)，五分钟演示见 [interview-guide.md](interview-guide.md)。
