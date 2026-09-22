# 研究日志与资料缺口

信息截止日 **2026-09-16**；数据集 `2026-09-16.v1`。首次来源读取发生在 2026-09-16 09:38–09:43 UTC，具体时间逐条保存在证据记录；主任务在同日约 15:10–15:17 UTC 再次打开关系来源的正文并检查关键段落。获取时间不等于信息发布日期，也不代表用户完成了人工审核。

## 覆盖与证据结论

共 14 家上市主体（NVIDIA 加 13 家关联公司）、22 条关系、14 个证据记录，对应 13 个不同来源 URL。所有关系均是范围受限的 confirmed 结论，全部 `human_review_status=pending`。没有为展示状态而人为补造 inferred、unknown 或冲突条目；这些状态与异常组合由隔离的合成测试覆盖。

| 相对 NVIDIA 的角色 | 数量 | 内容 |
| --- | ---: | --- |
| supplier | 5 | TSMC、Samsung、SK hynix、Micron、Hon Hai |
| customer | 1 | ASUS，限 2017 年报具名历史供货证据 |
| partner | 9 | TSMC、Synopsys 两项不同合作事件、ASUS、Intel、CoreWeave、Microsoft、Alphabet、Amazon |
| investor_or_investee | 2 | NVIDIA 对 CoreWeave、Synopsys 的已披露历史投资 |
| peer | 5 | AMD、Intel 的 GPU/加速计算；Microsoft、Alphabet、Amazon 的自研 AI 计算平台 |

上市身份与业务映射单独记录在 [company-identities.json](../data/company-identities.json)，包括普通股/ADS、Google Cloud/Alphabet、AWS/Amazon、Azure/Microsoft 和 Foxconn/Hon Hai 的区分。母公司 `parent_id=null` 表示目录内未另建母节点，不表示现实中没有控股股东。SK hynix 交易所归属仍列为作者二次复核事项。

## 已打开的原始关系来源

| 原始来源 | 原文定位与用途 | 发布日 |
| --- | --- | --- |
| [NVIDIA FY2026 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm) | Item 1 Manufacturing 印刷页8：五家供应商；Competition 页9：五家同行。两个片段共用原始 URL 和发行人独立来源组。 | 2026-02-25 |
| [cuLitho 官方公告](https://nvidianews.nvidia.com/news/tsmc-synopsys-nvidia-culitho) | 前三段及 Semiconductor Leaders 章节：TSMC、Synopsys 合作；不推定收入规模。 | 2024-03-18 |
| [ASUS 2017 年报](https://www.asus.com/event/Investor/Content/attachment_en/20180604192723447041905_en.pdf) | 印刷页106 / PDF第110页，原材料供应商表 Chips 行：支持 ASUS 历史采购方角色。 | 未知 |
| [ASUS 2025 年报](https://www.asus.com/EVENT/Investor/Content/attachment_en/2025_Annual_Report_en.pdf) | 印刷页2 / PDF第6页，G-SYNC Pulsar 合作；原材料供应商未具名，不能据此证明当前直接采购。 | 未知 |
| [CoreWeave 8-K](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000044/crwv-20260123.htm) | Item 3.02：2026-01-23 认购完成；公告日与交易日分开。 | 2026-01-26 |
| [CoreWeave 扩大合作公告](https://nvidianews.nvidia.com/news/nvidia-and-coreweave-strengthen-collaboration-to-accelerate-buildout-of-ai-factories) | 首段与合作事项：确认合作公告，2030年目标不记为已完成产能。 | 2026-01-26 |
| [Synopsys 投资与合作公告](https://nvidianews.nvidia.com/news/nvidia-and-synopsys-announce-strategic-partnership-to-revolutionize-engineering-and-design) | Highlights 和正文：支持工程合作及历史投资两条结论。公告未明确投资交割日，valid_from/to 保持空。 | 2025-12-01 |
| [Intel 联合研发公告](https://nvidianews.nvidia.com/news/nvidia-and-intel-to-develop-ai-infrastructure-and-personal-computing-products) | 前五段：确认研发合作；投资有监管及交割条件，未作为已完成投资录入。 | 2025-09-18 |
| [AWS 合作扩展](https://blogs.nvidia.com/blog/aws-partnership-expansion-reinvent/) | 首段与 NVLink Fusion 章节：确认合作公告，不等同直接采购法律关系。 | 2025-12-02 |
| [NVIDIA Azure AI foundry 公告](https://nvidianews.nvidia.com/news/nvidia-introduces-generative-ai-foundry-service-on-microsoft-azure-for-enterprises-and-startups-worldwide) | 首段及双方负责人说明：支持 AI foundry 合作。 | 2023-11-15 |
| [Microsoft Ignite 原文](https://blogs.microsoft.com/blog/2023/11/15/microsoft-ignite-2023-ai-transformation-and-the-technology-driving-change/) | Announcing NVIDIA AI foundry service 章节：补充合作方视角；同次信息链保守去重。 | 2023-11-15 |
| [Google Cloud 合作](https://blogs.nvidia.com/blog/google-cloud-next-agentic-ai-reasoning/) | 首段：Blackwell/Gemini 本地部署合作。映射到 Alphabet，不证明母公司签约。 | 2025-04-09 |
| [Micron HBM3E 公告](https://investors.micron.com/news/press-release/2024/Micron-Commences-Volume-Production-of-Industry-Leading-HBM3E-Solution-to-Accelerate-the-Growth-of-AI-02-26-2024/default.aspx) | 首段：计划用于 H200；作为间接补充，直接采购结论主要来自 NVIDIA 年报。 | 2024-02-26 |

对应的证据 ID、每条关联立场和直接性、实际读取时间、完整定位、短摘录、hash、访问与再分发说明见 [固定快照](../data/snapshots/2026-09-16.v1.json)。同一原始 URL 的英文摘录合计不超过25词；内容摘要仅覆盖摘录，未保存或声称保存原始全文。

## 判定与去重记录

检索用于发现官方资料，关系判断基于打开的正文。新闻稿、年报、业务页面的实体名与身份目录对照后再关联稳定公司 ID。供应关系内部使用供应方指向采购方；ASUS 的内部边为 NVIDIA → ASUS，查询 NVIDIA 时显示 customer。

所有 NVIDIA 年报与新闻稿默认归入 `issuer:nvidia`，不能把同一发行人的多个 URL 视作独立见证。Microsoft 的同次发布跟随该事件信息链保守合并；CoreWeave 的联合新闻稿与相同事件披露也不重复计算独立性。Micron 的原始公司披露具有不同信息来源，但仅作为较早的间接佐证，并非证明截止日现状。

合作边的同日起止表示“该日公告事件”，不是合作当日终止。Synopsys 投资未取得确切交割日，不能将新闻发布时间作为交易日；CoreWeave 的 8-K 明确记载完成日，因此使用具体事件日期。peer 对应具名业务维度，不表示所有产品互为替代。

## 已知缺口与下一次人工复核

- ASUS 年报印刷日期可以读取，但公开发布日期未可靠确定，保留 null；`known_at` 会排除这两份证据。客户样本较旧，优先补充近期具名采购披露。
- 不知道供应合同完整起止、近期持股变动或大多数收入贡献；不补造有效区间、金额或当前持续性。
- 本次研究没有确立同一事实同一时期的真实来源冲突；冲突扣分仅通过合成测试验证。来源缺失不当作反驳。
- 来源可访问并不等于已取得全文再分发权，许可未确认的内容不分发全文。作者发布前仍需复核摘录与来源条款。
- 覆盖经过选择而非穷尽；没有在本快照中出现的公司或关系不等于不存在。动态身份页面也不能作为完整历史证券主数据。

更新流程为“独立在线核查 → 人工维护候选 JSON → 新版本封存 → hash 与结构验证 → 版本比较 → 显式导入”，见 [方法论](methodology.md)。没有会绕过访问控制的自动采集器，也没有需要在线服务才能启动的隐式采集任务。
