# 逐条人工审核记录

整理日期：2026-09-22。整理者：Codex（AI）。

人工审核人：JOE 实际审核日期: 2026-09-22。

JOE已填写以下22条“本人判断”，并确认人工审核完成。Codex据此同步审核状态；本次同步未重新访问原始网页或PDF。阅读位置和记录一致性分析来自原AI草稿；“本人判断”保留审核人原文，AI分析不冒充审核人意见。

审核基于数据集`2026-09-16.v2`，完成结果发布为`2026-09-16.v3`；22条关系由`review_prepared`改为`approved`（人工审核通过）。原v1/v2保留，研究信息截止日仍为2026-09-16；证据获取时间、事实范围和评分规则不变。

## 整体方法判断

选择NVIDIA及这13家关联上市公司，是因为现有公开资料能覆盖晶圆代工、存储器、组装、历史客户、技术合作、投资和业务竞争等不同关系，也能展示同一公司同时具有合作与竞争角色。该选择适合检验证据追溯和关系建模，属于有意选择的样本，不能声称覆盖完整供应链或按公司重要性排名。我建议接受v1.0.0权重作为演示用启发式规则：直接证据30、来源可信度25、独立性10、时间明确度10、实体身份10、关系判定15，优先考虑证据是否支持具体结论；同源转载不加独立性，冲突来源应扣分。权重并未经过统计校准，直接性与关系判定可能相关，今后应通过标注样本和敏感性分析检验。分数适合说明所写结论的证据支持程度、辅助安排复核次序；不能说明公司重要性、投资价值、收入贡献、交易规模或事实成立概率。历史事件的高分也不能证明当前合作或持股仍然持续。该段是供本人确认的观点草稿，尚不代表本人已认同。

## 逐条记录

### tsmc-nvidia-supplier / TSMC 台积电与NVIDIA 英伟达：FY2026年报列名：TSMC提供晶圆代工。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `tsmc-nvidia-supplier`；证据 `ev-nv-fy26-manufacturing`
- 原始来源 URL：[ev-nv-fy26-manufacturing](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)
- 阅读位置：`ev-nv-fy26-manufacturing`：Item 1 Business, Manufacturing，印刷页8；依次为foundries、memory及assembly/testing/packaging段落。发布日另核对SEC filing index。
- 核验结果：现有记录的主体与方向为TSMC 台积电 → NVIDIA 英伟达；类型为`supplier`。时间：原文确认披露时的关系；未核验合同起止及2026-09-16是否持续，未知日期不补齐。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确，原文内容明确指出 NVIDIA 委派 TSMC 生成半导体晶圆。
- AI分析（保留供追溯，不作为本人判断）：现有研究记录将TSMC定位为晶圆代工方，供应方向应为TSMC→NVIDIA。保存的短摘录本身只列存储器厂商，接受此条仍需回到Manufacturing的foundries段确认TSMC具名及上下文；不能仅凭这段短摘录完成签署。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：采购量、金额及业务占比未披露或未核验。

### samsung-nvidia-supplier / Samsung 三星电子与NVIDIA 英伟达：FY2026年报列名：三星电子提供晶圆代工及存储器。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `samsung-nvidia-supplier`；证据 `ev-nv-fy26-manufacturing`
- 原始来源 URL：[ev-nv-fy26-manufacturing](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)
- 阅读位置：`ev-nv-fy26-manufacturing`：Item 1 Business, Manufacturing，印刷页8；依次为foundries、memory及assembly/testing/packaging段落。发布日另核对SEC filing index。
- 核验结果：现有记录的主体与方向为Samsung 三星电子 → NVIDIA 英伟达；类型为`supplier`。时间：原文确认披露时的关系；未核验合同起止及2026-09-16是否持续，未知日期不补齐。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确，原文内容明确指出 NVIDIA 委派 Samsung 生成半导体晶圆，以及购买内存。
- AI分析（保留供追溯，不作为本人判断）：存储器采购短摘录明确具名Samsung，支持三星→NVIDIA；但本条还包含晶圆代工，应在foundries段单独核实。两项业务不能因存储器采购已具名就视为同时核实，也不能由此推断HBM型号或供应份额。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：采购量、金额及业务占比未披露或未核验。

### sk-hynix-nvidia-supplier / SK hynix 海力士与NVIDIA 英伟达：FY2026年报列名：NVIDIA向SK hynix采购存储器。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `sk-hynix-nvidia-supplier`；证据 `ev-nv-fy26-manufacturing`
- 原始来源 URL：[ev-nv-fy26-manufacturing](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)
- 阅读位置：`ev-nv-fy26-manufacturing`：Item 1 Business, Manufacturing，印刷页8；依次为foundries、memory及assembly/testing/packaging段落。发布日另核对SEC filing index。
- 核验结果：现有记录的主体与方向为SK hynix 海力士 → NVIDIA 英伟达；类型为`supplier`。时间：原文确认披露时的关系；未核验合同起止及2026-09-16是否持续，未知日期不补齐。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确，原文内容明确指出 NVIDIA 从 SK hynix 海力士购买内存。
- AI分析（保留供追溯，不作为本人判断）：保存的短摘录明确写明向SK Hynix采购存储器，主体、供应方向及类型与记录一致，因此草稿建议接受有限的采购事实。未披露合同区间就保留未知，不能把年报发布日期当作供货起始日。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：采购量、金额及业务占比未披露或未核验。

### micron-nvidia-supplier / Micron 美光与NVIDIA 英伟达：FY2026年报列名：NVIDIA向Micron采购存储器。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `micron-nvidia-supplier`；证据 `ev-nv-fy26-manufacturing`, `ev-micron-2024`
- 原始来源 URL：[ev-nv-fy26-manufacturing](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)；[ev-micron-2024](https://investors.micron.com/news/press-release/2024/Micron-Commences-Volume-Production-of-Industry-Leading-HBM3E-Solution-to-Accelerate-the-Growth-of-AI-02-26-2024/default.aspx)
- 阅读位置：`ev-nv-fy26-manufacturing`：Item 1 Business, Manufacturing，印刷页8；依次为foundries、memory及assembly/testing/packaging段落。发布日另核对SEC filing index。；`ev-micron-2024`：发布日期下首段，24GB 8H HBM3E与NVIDIA H200。
- 核验结果：现有记录的主体与方向为Micron 美光 → NVIDIA 英伟达；类型为`supplier`。时间：原文确认披露时的关系；未核验合同起止及2026-09-16是否持续，未知日期不补齐。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确，原文内容明确指出 NVIDIA 从 Micron 美光购买内存。
- AI分析（保留供追溯，不作为本人判断）：NVIDIA年报保存的短摘录具名Micron，可支持采购方向；Micron的HBM3E用于H200声明只作间接补充。两者支持力度不同，不能把产品采用等同直接采购，也不能由额外来源推定采购规模。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：采购量、金额及业务占比未披露或未核验。

### hon-hai-nvidia-supplier / Hon Hai 鸿海与NVIDIA 英伟达：FY2026年报列名：鸿海提供组装、测试及封装服务。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `hon-hai-nvidia-supplier`；证据 `ev-nv-fy26-manufacturing`
- 原始来源 URL：[ev-nv-fy26-manufacturing](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)
- 阅读位置：`ev-nv-fy26-manufacturing`：Item 1 Business, Manufacturing，印刷页8；依次为foundries、memory及assembly/testing/packaging段落。发布日另核对SEC filing index。
- 核验结果：现有记录的主体与方向为Hon Hai 鸿海 → NVIDIA 英伟达；类型为`supplier`。时间：原文确认披露时的关系；未核验合同起止及2026-09-16是否持续，未知日期不补齐。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确，原文内容明确指出 Nvidia 与 Hon Hai 鸿海合作，其负责最终产品的组装、测试和包装。
- AI分析（保留供追溯，不作为本人判断）：现有研究记录将鸿海列为组装、测试及封装服务方，供应方向合理；但共享短摘录仅包含存储器厂商，需要阅读assembly/testing/packaging段确认鸿海及涉及主体，不能以存储器摘录替代该业务核实。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：采购量、金额及业务占比未披露或未核验。

### nvidia-asus-supplier-historical / NVIDIA 英伟达与ASUS 华硕：ASUS 2017年报具名列出Nvidia为芯片供应商；ASUS为历史采购方。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `nvidia-asus-supplier-historical`；证据 `ev-asus-2017-supply`
- 原始来源 URL：[ev-asus-2017-supply](https://www.asus.com/event/Investor/Content/attachment_en/20180604192723447041905_en.pdf)
- 阅读位置：`ev-asus-2017-supply`：印刷页106，PDF第110页，V. Overview of business operation → (III) Supply of major raw materials，Chips行；封面Printed on April 18, 2018。
- 核验结果：现有记录的主体与方向为NVIDIA 英伟达 → ASUS 华硕；类型为`supplier`。时间：仅确认2017年报所记录的历史供应事实。未披露合同起止，因此不将2017年整年或印刷日伪装成有效区间。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确，2025年台北国际电脑展也包含合作伙伴包含 VSUS。
- AI分析（保留供追溯，不作为本人判断）：现有2017年报记录只足以支持历史芯片采购，内部方向应为NVIDIA→ASUS，查询NVIDIA时ASUS显示为客户。较新的显示器合作和匿名供应商披露均不能单独证明当前直接采购，因此建议保留历史条目；实际采购区间及年报公开发布日期继续留空。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：2025年报的匿名供应商不可消歧为NVIDIA；不能证明截至研究截止日仍有直接采购。

### nvidia-tsmc-culitho / NVIDIA 英伟达与TSMC 台积电：2024-03-18宣布TSMC与NVIDIA开展cuLitho生产工作流合作。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `nvidia-tsmc-culitho`；证据 `ev-culitho-2024`
- 原始来源 URL：[ev-culitho-2024](https://nvidianews.nvidia.com/news/tsmc-synopsys-nvidia-culitho)
- 阅读位置：`ev-culitho-2024`：正文第1—3段及 Semiconductor Leaders Advance cuLitho Platform。
- 核验结果：现有记录的主体与方向为NVIDIA 英伟达 ↔ TSMC 台积电（对称关系）；类型为`partner`。时间：本条结论限定为当日已发生的合作公告事件；同日起止仅界定事件，不表示合作当日终止，也不证明未来项目已落地。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确。
- AI分析（保留供追溯，不作为本人判断）：现有材料记录的是TSMC参与cuLitho生产工作流合作，适合归为对称合作关系；不能把工作流采用当作对NVIDIA的直接采购。2024-03-18仅界定公告事件，后续部署与收入不在该证据可直接支持的范围。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：持续期限、后续执行与收入贡献未完整核验。

### nvidia-synopsys-culitho / NVIDIA 英伟达与Synopsys 新思科技：2024-03-18宣布Synopsys与NVIDIA开展cuLitho计算光刻合作。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `nvidia-synopsys-culitho`；证据 `ev-culitho-2024`
- 原始来源 URL：[ev-culitho-2024](https://nvidianews.nvidia.com/news/tsmc-synopsys-nvidia-culitho)
- 阅读位置：`ev-culitho-2024`：正文第1—3段及 Semiconductor Leaders Advance cuLitho Platform。
- 核验结果：现有记录的主体与方向为NVIDIA 英伟达 ↔ Synopsys 新思科技（对称关系）；类型为`partner`。时间：本条结论限定为当日已发生的合作公告事件；同日起止仅界定事件，不表示合作当日终止，也不证明未来项目已落地。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确。
- AI分析（保留供追溯，不作为本人判断）：Synopsys在同一cuLitho公告中承担计算光刻合作角色，宜与TSMC分别建边以保留不同主体。本条与2025年工程设计合作内容和日期不同，不应合并为无时间边界的笼统战略合作。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：持续期限、后续执行与收入贡献未完整核验。

### nvidia-synopsys-engineering / NVIDIA 英伟达与Synopsys 新思科技：2025-12-01宣布扩大工程设计、CUDA加速与数字孪生合作。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `nvidia-synopsys-engineering`；证据 `ev-snps-2025`
- 原始来源 URL：[ev-snps-2025](https://nvidianews.nvidia.com/news/nvidia-and-synopsys-announce-strategic-partnership-to-revolutionize-engineering-and-design)
- 阅读位置：`ev-snps-2025`：Key Highlights三项；正文第2段；Joint Development to Enable Future of Engineering on Accelerated Computing。
- 核验结果：现有记录的主体与方向为NVIDIA 英伟达 ↔ Synopsys 新思科技（对称关系）；类型为`partner`。时间：本条结论限定为当日已发生的合作公告事件；同日起止仅界定事件，不表示合作当日终止，也不证明未来项目已落地。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确。
- AI分析（保留供追溯，不作为本人判断）：2025年公告的工程设计、CUDA加速及数字孪生合作具备具体业务内容，足以作为合作事件候选；同一公告中的股权投资另列方向性关系，避免把投资金额误当作合作收入或采购承诺。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：持续期限、后续执行与收入贡献未完整核验。

### nvidia-asus-display / NVIDIA 英伟达与ASUS 华硕：ASUS 2025年报披露与NVIDIA推出G-SYNC Pulsar显示器的合作。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `nvidia-asus-display`；证据 `ev-asus-2025-partner`
- 原始来源 URL：[ev-asus-2025-partner](https://www.asus.com/EVENT/Investor/Content/attachment_en/2025_Annual_Report_en.pdf)
- 阅读位置：`ev-asus-2025-partner`：印刷页2，PDF第6页，gaming段落；另印刷页121原材料供应段与页122注释（2026-03-31印刷）。
- 核验结果：现有记录的主体与方向为NVIDIA 英伟达 ↔ ASUS 华硕（对称关系）；类型为`partner`。时间：年报回顾事实，准确合作日和结束日未知；不从财年回顾推定整年有效。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确。
- AI分析（保留供追溯，不作为本人判断）：年报回顾G-SYNC Pulsar显示器合作，支持具体产品合作候选；不支持新增当前采购关系。实际合作日与公开发布日期均未建立，不能以财年或印刷日期填充，因此建议保留历史描述及未知时间。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：合同内容、合作具体发生日和收入规模均未核验。

### nvidia-intel-development / NVIDIA 英伟达与Intel 英特尔：2025-09-18宣布共同开发通过NVLink连接的定制数据中心与PC产品。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `nvidia-intel-development`；证据 `ev-intel-2025`
- 原始来源 URL：[ev-intel-2025](https://nvidianews.nvidia.com/news/nvidia-and-intel-to-develop-ai-infrastructure-and-personal-computing-products)
- 阅读位置：`ev-intel-2025`：正文第1—5段，custom data center and PC products、NVLink以及监管交割条件。
- 核验结果：现有记录的主体与方向为NVIDIA 英伟达 ↔ Intel 英特尔（对称关系）；类型为`partner`。时间：本条结论限定为当日已发生的合作公告事件；同日起止仅界定事件，不表示合作当日终止，也不证明未来项目已落地。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确。
- AI分析（保留供追溯，不作为本人判断）：共同开发NVLink连接产品的声明支持研发合作事件；产品仍有交付条件，不能表述为已经完成交付。同文投资存在交割条件，不能以此新增已完成投资记录；合作和同行关系也可以同时成立。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：产品交付尚有未来条件；本公告所述投资非交割证明，未据此添加投资完成记录。

### nvidia-coreweave-factories / NVIDIA 英伟达与CoreWeave：2026-01-26宣布扩大AI工厂、软件验证与计算平台合作。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `nvidia-coreweave-factories`；证据 `ev-crwv-2026-partner`
- 原始来源 URL：[ev-crwv-2026-partner](https://nvidianews.nvidia.com/news/nvidia-and-coreweave-strengthen-collaboration-to-accelerate-buildout-of-ai-factories)
- 阅读位置：`ev-crwv-2026-partner`：正文首段、infrastructure/software/platform alignment及四项合作事项。
- 核验结果：现有记录的主体与方向为NVIDIA 英伟达 ↔ CoreWeave（对称关系）；类型为`partner`。时间：本条结论限定为当日已发生的合作公告事件；同日起止仅界定事件，不表示合作当日终止，也不证明未来项目已落地。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确。
- AI分析（保留供追溯，不作为本人判断）：扩大AI工厂、软件验证和计算平台合作有明确业务范围，适合记录2026-01-26公告事件。2030年前超过5GW属于目标，不可写成已建成容量；投资交易与合作发布分别建模有助于保留时间差异。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：持续期限、后续执行与收入贡献未完整核验。

### nvidia-microsoft-foundry / NVIDIA 英伟达与Microsoft 微软：2023-11-15双方公告在Microsoft Azure上推出NVIDIA AI foundry服务。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `nvidia-microsoft-foundry`；证据 `ev-ms-nvidia-2023`, `ev-ms-ignite-2023`
- 原始来源 URL：[ev-ms-nvidia-2023](https://nvidianews.nvidia.com/news/nvidia-introduces-generative-ai-foundry-service-on-microsoft-azure-for-enterprises-and-startups-worldwide)；[ev-ms-ignite-2023](https://blogs.microsoft.com/blog/2023/11/15/microsoft-ignite-2023-ai-transformation-and-the-technology-driving-change/)
- 阅读位置：`ev-ms-nvidia-2023`：正文首段、Satya Nadella引语及NVIDIA DGX Cloud Now Available on Microsoft Azure Marketplace。；`ev-ms-ignite-2023`：Announcing NVIDIA AI foundry service小节，两段。
- 核验结果：现有记录的主体与方向为NVIDIA 英伟达 ↔ Microsoft 微软（对称关系）；类型为`partner`。时间：本条结论限定为当日已发生的合作公告事件；同日起止仅界定事件，不表示合作当日终止，也不证明未来项目已落地。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确。
- AI分析（保留供追溯，不作为本人判断）：双方材料共同指向Azure上的AI foundry发布，主体映射微软、合作类型及公告事件日相互一致。两方发布属于同一信息链，不宜重复计算独立性；运行NVIDIA产品也不直接证明微软向NVIDIA采购GPU。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：Azure为微软业务；两方同次发布按同一信息链计数；不证明微软直接GPU采购额。

### nvidia-alphabet-cloud / NVIDIA 英伟达与Alphabet / Google：2025-04-09宣布Google Cloud与NVIDIA开展Gemini及Blackwell保密计算合作。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `nvidia-alphabet-cloud`；证据 `ev-google-2025`
- 原始来源 URL：[ev-google-2025](https://blogs.nvidia.com/blog/google-cloud-next-agentic-ai-reasoning/)
- 阅读位置：`ev-google-2025`：正文首段及Google Cloud负责人引语；Google Distributed Cloud/Blackwell。
- 核验结果：现有记录的主体与方向为NVIDIA 英伟达 ↔ Alphabet / Google（对称关系）；类型为`partner`。时间：本条结论限定为当日已发生的合作公告事件；同日起止仅界定事件，不表示合作当日终止，也不证明未来项目已落地。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确。
- AI分析（保留供追溯，不作为本人判断）：披露主体Google Cloud映射上市母公司Alphabet需要保留mapped标记，不能表述为Alphabet直接签约采购。Gemini与Blackwell保密计算支持合作事件候选，但计划可用与已交付须分开。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：Google Cloud归属Alphabet；可用性含计划表述，未核验后续交付或直接采购。

### nvidia-amazon-cloud / NVIDIA 英伟达与Amazon 亚马逊：2025-12-02宣布AWS与NVIDIA扩大NVLink Fusion和云平台合作。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `nvidia-amazon-cloud`；证据 `ev-aws-2025`
- 原始来源 URL：[ev-aws-2025](https://blogs.nvidia.com/blog/aws-partnership-expansion-reinvent/)
- 阅读位置：`ev-aws-2025`：正文首段及NVLink Fusion/Trainium4段落。
- 核验结果：现有记录的主体与方向为NVIDIA 英伟达 ↔ Amazon 亚马逊（对称关系）；类型为`partner`。时间：本条结论限定为当日已发生的合作公告事件；同日起止仅界定事件，不表示合作当日终止，也不证明未来项目已落地。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确。
- AI分析（保留供追溯，不作为本人判断）：AWS的NVLink Fusion与云平台合作可以映射至上市母公司Amazon展示，同时应保留主体映射限制。云服务采用GPU及未来产品计划不等同Amazon直接采购，故仅建议接受有限合作事件。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：AWS归属Amazon；产品计划、GPU部署与直接采购法律关系不能等同。

### nvidia-coreweave-investment / NVIDIA 英伟达与CoreWeave：CoreWeave披露于2026-01-23完成向NVIDIA发行A类普通股的投资交易。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `nvidia-coreweave-investment`；证据 `ev-crwv-2026-investment`
- 原始来源 URL：[ev-crwv-2026-investment](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000044/crwv-20260123.htm)
- 阅读位置：`ev-crwv-2026-investment`：Item 3.02 Unregistered Sales of Equity Securities，第1段；Item 8.01 collaboration。
- 核验结果：现有记录的主体与方向为NVIDIA 英伟达 → CoreWeave；类型为`investor_or_investee`。时间：记录已完成认购的历史事件，同日起止为交易事件日，不表示持股当日卖出；截止日持股余额未知。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确。
- AI分析（保留供追溯，不作为本人判断）：8-K记录已完成向NVIDIA发行A类普通股，投资方向应为NVIDIA→CoreWeave；2026-01-23为交易事件日，不能替换成后续合作公告日。同日起止用于事件定位，不表示当日卖出，也无法推出截止日持仓。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：不能由这次认购推定当前股数、持股比例或后续增减持。

### nvidia-synopsys-investment / NVIDIA 英伟达与Synopsys 新思科技：2025-12-01公告披露NVIDIA已投资Synopsys普通股。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `nvidia-synopsys-investment`；证据 `ev-snps-2025`
- 原始来源 URL：[ev-snps-2025](https://nvidianews.nvidia.com/news/nvidia-and-synopsys-announce-strategic-partnership-to-revolutionize-engineering-and-design)
- 阅读位置：`ev-snps-2025`：Key Highlights三项；正文第2段；Joint Development to Enable Future of Engineering on Accelerated Computing。
- 核验结果：现有记录的主体与方向为NVIDIA 英伟达 → Synopsys 新思科技；类型为`investor_or_investee`。时间：公告使用已投资表述，故确认历史投资；确切交割日期未明，不把公告日填成交割日；截止日持股未知。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确。
- AI分析（保留供追溯，不作为本人判断）：公告使用已投资表述，可以支持历史股权投资候选；投资与工程设计合作应分别记录。未明确交割日就保留空值，不能机械使用2025-12-01公告日，更不能把20亿美元当作当前持股市值。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：未核验确切交割日、截止日持股数量与后续交易。

### nvidia-amd-peer / NVIDIA 英伟达与AMD 超威半导体：年报将AMD列为GPU及AI加速计算竞争方。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `nvidia-amd-peer`；证据 `ev-nv-fy26-competition`
- 原始来源 URL：[ev-nv-fy26-competition](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)
- 阅读位置：`ev-nv-fy26-competition`：Item 1 Business, Competition，印刷页9，current competitors首两项。
- 核验结果：现有记录的主体与方向为NVIDIA 英伟达 ↔ AMD 超威半导体（对称关系）；类型为`peer`。时间：原文确认披露时的关系；未核验合同起止及2026-09-16是否持续，未知日期不补齐。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确。
- AI分析（保留供追溯，不作为本人判断）：现有年报研究记录将AMD 超威半导体列为竞争方，可比维度限定为“独立/集成GPU与AI加速计算软硬件”，因此建议接受该业务维度的对称同行关系。竞争关系不是供货方向，也不意味着所有业务互相替代；与合作边并存并不矛盾。仍需核对Competition原文中该主体及对应业务分组，不从共同出现推断竞争程度或公司排名。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：只比较所列业务维度；不表示全部业务互为替代，亦不构成投资价值排序。

### nvidia-intel-peer / NVIDIA 英伟达与Intel 英特尔：年报将Intel列为GPU及AI加速计算竞争方。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `nvidia-intel-peer`；证据 `ev-nv-fy26-competition`
- 原始来源 URL：[ev-nv-fy26-competition](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)
- 阅读位置：`ev-nv-fy26-competition`：Item 1 Business, Competition，印刷页9，current competitors首两项。
- 核验结果：现有记录的主体与方向为NVIDIA 英伟达 ↔ Intel 英特尔（对称关系）；类型为`peer`。时间：原文确认披露时的关系；未核验合同起止及2026-09-16是否持续，未知日期不补齐。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确。
- AI分析（保留供追溯，不作为本人判断）：现有年报研究记录将Intel 英特尔列为竞争方，可比维度限定为“独立/集成GPU与AI加速计算软硬件”，因此建议接受该业务维度的对称同行关系。竞争关系不是供货方向，也不意味着所有业务互相替代；与合作边并存并不矛盾。仍需核对Competition原文中该主体及对应业务分组，不从共同出现推断竞争程度或公司排名。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：只比较所列业务维度；不表示全部业务互为替代，亦不构成投资价值排序。

### nvidia-microsoft-peer / NVIDIA 英伟达与Microsoft 微软：年报将Microsoft列为自研AI计算平台竞争方。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `nvidia-microsoft-peer`；证据 `ev-nv-fy26-competition`
- 原始来源 URL：[ev-nv-fy26-competition](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)
- 阅读位置：`ev-nv-fy26-competition`：Item 1 Business, Competition，印刷页9，current competitors首两项。
- 核验结果：现有记录的主体与方向为NVIDIA 英伟达 ↔ Microsoft 微软（对称关系）；类型为`peer`。时间：原文确认披露时的关系；未核验合同起止及2026-09-16是否持续，未知日期不补齐。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确。
- AI分析（保留供追溯，不作为本人判断）：现有年报研究记录将Microsoft 微软列为竞争方，可比维度限定为“云服务商自研AI/加速计算软硬件平台”，因此建议接受该业务维度的对称同行关系。竞争关系不是供货方向，也不意味着所有业务互相替代；与合作边并存并不矛盾。仍需核对Competition原文中该主体及对应业务分组，不从共同出现推断竞争程度或公司排名。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：只比较所列业务维度；不表示全部业务互为替代，亦不构成投资价值排序。

### nvidia-alphabet-peer / NVIDIA 英伟达与Alphabet / Google：年报将Alphabet列为自研AI计算平台竞争方。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `nvidia-alphabet-peer`；证据 `ev-nv-fy26-competition`
- 原始来源 URL：[ev-nv-fy26-competition](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)
- 阅读位置：`ev-nv-fy26-competition`：Item 1 Business, Competition，印刷页9，current competitors首两项。
- 核验结果：现有记录的主体与方向为NVIDIA 英伟达 ↔ Alphabet / Google（对称关系）；类型为`peer`。时间：原文确认披露时的关系；未核验合同起止及2026-09-16是否持续，未知日期不补齐。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确。
- AI分析（保留供追溯，不作为本人判断）：现有年报研究记录将Alphabet / Google列为竞争方，可比维度限定为“云服务商自研AI/加速计算软硬件平台”，因此建议接受该业务维度的对称同行关系。竞争关系不是供货方向，也不意味着所有业务互相替代；与合作边并存并不矛盾。仍需核对Competition原文中该主体及对应业务分组，不从共同出现推断竞争程度或公司排名。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：只比较所列业务维度；不表示全部业务互为替代，亦不构成投资价值排序。

### nvidia-amazon-peer / NVIDIA 英伟达与Amazon 亚马逊：年报将Amazon列为自研AI计算平台竞争方。

- 审核人：JOE；AI草稿整理及状态同步：Codex
- 实际审核日期：2026-09-22
- 审核对象：数据集 `2026-09-16.v2`；关系 `nvidia-amazon-peer`；证据 `ev-nv-fy26-competition`
- 原始来源 URL：[ev-nv-fy26-competition](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)
- 阅读位置：`ev-nv-fy26-competition`：Item 1 Business, Competition，印刷页9，current competitors首两项。
- 核验结果：现有记录的主体与方向为NVIDIA 英伟达 ↔ Amazon 亚马逊（对称关系）；类型为`peer`。时间：原文确认披露时的关系；未核验合同起止及2026-09-16是否持续，未知日期不补齐。上述为AI记录一致性分析；人工结论见下方“本人判断”。
- 本人判断：正确。
- AI分析（保留供追溯，不作为本人判断）：现有年报研究记录将Amazon 亚马逊列为竞争方，可比维度限定为“云服务商自研AI/加速计算软硬件平台”，因此建议接受该业务维度的对称同行关系。竞争关系不是供货方向，也不意味着所有业务互相替代；与合作边并存并不矛盾。仍需核对Competition原文中该主体及对应业务分组，不从共同出现推断竞争程度或公司排名。
- 修改内容：关系事实内容无；审核流程状态由`review_prepared`改为`approved`，结果见v3。
- 剩余不确定性：只比较所列业务维度；不表示全部业务互为替代，亦不构成投资价值排序。

