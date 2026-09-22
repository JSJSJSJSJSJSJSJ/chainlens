# ChainLens 内部数据与 API 契约

研究截止日 `2026-09-16`。标识符为稳定英文短 ID。所有响应为 JSON，所有日期为 ISO 8601；未知日期为 null。

## 固定快照

`data/snapshots/2026-09-16.v1.json` 顶层为 `metadata`, `companies`, `evidence`, `relationships`。

- metadata: dataset_version, research_cutoff, score_version (`1.0.0`), created_at, description, gaps (string[])
- company: id, legal_name, display_name, aliases (string[]), ticker, exchange, listing_status (`listed`), parent_id (nullable), identity_notes
- evidence: id, title, source_url, publisher, published_at (date|null), retrieved_at (datetime), evidence_locator, excerpt, interpretation, source_type (`regulatory`|`company`|`media`), independence_key, content_sha256 (excerpt UTF-8), access_restrictions, redistribution_notes
- relationship: id, source_company_id, target_company_id, relationship_type (`supplier`|`partner`|`investor_or_investee`|`peer`), business_description, fact_status (`confirmed`|`inferred`|`unknown`), valid_from (date|null), valid_to (date|null), temporal_status (`historical`|`current`|`unknown`), continuity_note, uncertainty, human_review_status (`pending`), entity_resolution (`exact`|`mapped`|`uncertain`), comparison_dimension (string|null), quantitative_context (string|null), evidence_links ([{evidence_id, stance: `supports`|`contradicts`, directness: `direct`|`indirect`}]).

supplier 内部始终为供应方 → 采购方，查询供应方时对外角色为 customer，查询采购方时为 supplier。投资为投资方 → 被投资方。partner/peer 为对称关系。使用产品不等于直接采购，历史投资不等于当前持股。

## 查询

`GET /api/health` → {status, dataset_version, research_cutoff, score_version}

`GET /api/companies?q=&page=1&page_size=20` → {items: Company[], total, page, page_size}

`GET /api/companies/{id}` → Company 加 `summary: {relationship_count, evidence_count, related_company_count, distribution: {supplier,customer,partner,investor_or_investee,peer}}`, `dataset: metadata`

`GET /api/companies/{id}/relationships` 参数 q, relationship_type (对外角色), min_confidence (0–100), fact_status, known_at (date), valid_at (date), include_unknown_time (bool, default false), page (>=1), page_size (1–100), sort (`confidence_desc`|`company_asc`|`date_desc`, default confidence_desc)。稳定排序追加 ID。

known_at: 仅使用 published_at 不晚于该日期的证据；至少一个支持证据在该日期已发表才纳入，并以该证据子集重新评分；不声称当时已核验。valid_at: 已知 valid_from <= 日期且已知 valid_to >= 日期；开放结束区间仅 temporal_status=current 且日期 <= research_cutoff 才可确定覆盖。未知边界只有 include_unknown_time=true 才纳入，并显示不确定性。参数日期不得晚于研究截止日。

列表返回 {items: RelationshipView[], total, page, page_size}。

RelationshipView 包含 relationship 全字段，加 source_company 和 target_company 完整对象，related_company（相对查询中心；独立详情 null）, queried_role（相对查询中心；独立详情为内部类型）, evidence_count, independent_source_count, score。

score: {total, rule_version, calculated_at, components: [{key, label, points, max_points, reason}], explanation, current_validity: `supported`|`historical_only`|`unestablished`}。

`GET /api/companies/{id}/graph` 使用列表相同筛选参数（不使用分页），返回 {nodes: Company[], edges: RelationshipView[], total, displayed, truncated, limit: 100, scope_note}。先稳定排序，截断到 100 条后产生节点，计数显式展示。

`GET /api/relationships/{id}` → RelationshipView；可选 known_at 与列表语义相同。

`GET /api/relationships/{id}/evidence` → {items: (Evidence 加 stance,directness)[], total}；可选 known_at。

错误统一为 {error: {code, message, details}}；输入非法 422，资源不存在 404。

前端使用 /api 相对路径，由 Vite 代理到 127.0.0.1:8000；默认中心公司 ID `nvidia`。

CLI: `python -m chainlens.cli import-snapshot`, `companies`, `company nvidia`, `relationships nvidia`, `graph nvidia`, `evidence RELATIONSHIP_ID`，查询提供 --json，与 API 共用服务。Python 包位于 backend/chainlens，测试 backend/tests，根目录 pyproject.toml/uv.lock；frontend 使用 pnpm-lock.yaml。
