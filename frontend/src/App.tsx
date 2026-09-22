import { useCallback, useState } from 'react';
import { Activity, ArrowUpRight, Database, GitBranch, Layers3, List, Network, ScanLine } from 'lucide-react';
import { filterQuery } from './api';
import { useResource } from './hooks/useResource';
import type { CompanyDetail, Filters as FilterValues, Graph, Page, Relationship } from './types';
import { roles, roleLabels, roleColors } from './labels';
import { Filters } from './components/Filters';
import { RelationshipTable } from './components/RelationshipTable';
import { RelationshipGraph } from './components/RelationshipGraph';
import { RelationshipDetail } from './components/RelationshipDetail';
import { Loading, Failure, Empty } from './components/States';

const defaults: FilterValues = { q: '', relationship_type: '', min_confidence: 0, fact_status: '', known_at: '', valid_at: '', include_unknown_time: false, sort: 'confidence_desc' };

export default function App() {
  const [filters, setFilters] = useState(defaults);
  const [page, setPage] = useState(1);
  const [tab, setTab] = useState<'list' | 'graph'>('list');
  const [selected, setSelected] = useState<string | null>(null);
  const [revision, setRevision] = useState(0);
  const company = useResource<CompanyDetail>('/api/companies/nvidia', revision);
  const query = filterQuery(filters);
  const list = useResource<Page<Relationship>>(company.data ? `/api/companies/nvidia/relationships?${query}&page=${page}&page_size=10` : null, revision);
  const graph = useResource<Graph>(company.data && tab === 'graph' ? `/api/companies/nvidia/graph?${query}` : null, revision);
  const changeFilters = (value: FilterValues) => { setFilters(value); setPage(1); setSelected(null); };
  const reset = () => changeFilters({ ...defaults });
  const close = useCallback(() => setSelected(null), []);
  const select = useCallback((id: string) => setSelected(id), []);
  const retry = () => setRevision(value => value + 1);
  const resource = tab === 'list' ? list : graph;

  return <div className="app-shell">
    <a href="#research" className="skip-link">跳至研究数据</a>
    <header className="topbar"><a className="brand" href="/"><span className="brand-mark"><ScanLine size={24} /></span><strong>ChainLens <span>链鉴</span></strong></a><nav aria-label="主导航"><a className="nav-active" href="#research">研究工作台</a><a href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer">API 文档 <ArrowUpRight size={13} /></a></nav><span className="snapshot-pill"><span />固定研究快照</span></header>
    <main>
      <div className="breadcrumb">研究工作台 <span>/</span> 半导体与人工智能 <span>/</span> NVIDIA</div>
      {company.loading ? <Loading /> : company.error ? <Failure message={company.error} onRetry={retry} /> : company.data && <>
        <section className="company-overview" aria-label="公司概览"><div className="overview-copy"><div className="eyebrow">EVIDENCE-FIRST COMPANY RESEARCH</div><h1>{company.data.display_name}<span className="ticker-badge">{company.data.exchange}: {company.data.ticker}</span></h1><p className="company-legal">{company.data.legal_name}</p><p className="overview-description">看见关系，更看见依据。<br />从公开披露出发，追溯每一条供应、合作与投资关系。</p><div className="overview-meta"><span><Database size={14} />{company.data.dataset.dataset_version}</span><span>全部待人工复核</span></div></div><div className="cutoff-card"><span className="eyebrow">RESEARCH CUTOFF</span><strong>{company.data.dataset.research_cutoff}</strong><p>研究信息截止日期</p><div className="cutoff-rule" /><small>历史事实 ≠ 当前持续关系<br />置信度 ≠ 投资价值或概率</small></div></section>
        <section className="stats-grid" aria-label="数据规模"><Stat label="关联上市公司" value={company.data.summary.related_company_count} unit="家" icon={<Network size={19} />} /><Stat label="具体关系结论" value={company.data.summary.relationship_count} unit="条" icon={<GitBranch size={19} />} /><Stat label="结构化证据" value={company.data.summary.evidence_count} unit="份" icon={<Layers3 size={19} />} /><Stat label="关系研究维度" value={roles.length} unit="类" icon={<Activity size={19} />} /></section>
        <section className="distribution" aria-label="五类关系分布">{roles.map(role => <button key={role} className={filters.relationship_type === role ? 'distribution-item active' : 'distribution-item'} onClick={() => changeFilters({ ...filters, relationship_type: filters.relationship_type === role ? '' : role })} aria-pressed={filters.relationship_type === role}><i style={{ background: roleColors[role] }} /><span>{roleLabels[role]}</span><strong>{company.data!.summary.distribution[role]}</strong></button>)}</section>
        <details className="limitations"><summary>研究边界与数据限制 <span>阅读后使用</span></summary><p>{company.data.dataset.description}</p><ul>{company.data.dataset.gaps.map(gap => <li key={gap}>{gap}</li>)}</ul><p>公开资料的有限样本，不代表完整市场覆盖。仅用于研究与工程演示，不构成投资建议。</p></details>
        <section id="research" className="research-panel"><div className="section-heading"><div><span className="eyebrow">RELATIONSHIP EXPLORER</span><h2>关系研究 <span>{resource.data?.total ?? '—'}</span></h2></div><div className="view-switch" role="group" aria-label="展示方式"><button aria-pressed={tab === 'list'} onClick={() => setTab('list')}><List size={16} />关系列表</button><button aria-pressed={tab === 'graph'} onClick={() => setTab('graph')}><Network size={16} />关系图谱</button></div></div><Filters value={filters} onChange={changeFilters} onReset={reset} cutoff={company.data.dataset.research_cutoff} />
          <div aria-live="polite">{resource.loading ? <Loading text="正在更新关系…" /> : resource.error ? <Failure message={resource.error} onRetry={retry} /> : resource.data?.total === 0 ? <Empty onReset={reset} /> : tab === 'list' && list.data ? <RelationshipTable data={list.data} selected={selected} onSelect={select} onPage={setPage} /> : tab === 'graph' && graph.data ? <RelationshipGraph data={graph.data} companyId="nvidia" selected={selected} onSelect={select} /> : null}</div>
        </section>
      </>}
      <footer><span>ChainLens · 让判断有据可循</span><span>公开证据 · 确定性评分 · 待人工复核</span></footer>
    </main>
    {selected && <RelationshipDetail id={selected} knownAt={filters.known_at} onClose={close} />}
  </div>;
}

function Stat({ label, value, unit, icon }: { label: string; value: number; unit: string; icon: React.ReactNode }) {
  return <div className="stat-card"><div className="stat-label">{label}{icon}</div><div className="stat-number">{value}<span>{unit}</span></div></div>;
}
