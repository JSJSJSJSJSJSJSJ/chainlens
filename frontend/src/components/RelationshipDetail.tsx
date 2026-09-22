import { useEffect, useRef, useState } from 'react';
import { X, ArrowUpRight, BookOpen, ShieldCheck, Clock3, FileText } from 'lucide-react';
import { useResource } from '../hooks/useResource';
import type { Evidence, Relationship } from '../types';
import { dateLabel, statusLabels, temporalLabels, validityLabels } from '../labels';
import { Direction } from './RelationshipTable';
import { Loading, Failure } from './States';

export function RelationshipDetail({ id, knownAt, onClose }: { id: string; knownAt: string; onClose: () => void }) {
  const [revision, setRevision] = useState(0);
  const query = knownAt ? `?known_at=${encodeURIComponent(knownAt)}` : '';
  const relation = useResource<Relationship>(`/api/relationships/${encodeURIComponent(id)}${query}`, revision);
  const evidence = useResource<{ items: Evidence[]; total: number }>(`/api/relationships/${encodeURIComponent(id)}/evidence${query}`, revision);
  const panel = useRef<HTMLElement>(null);
  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null;
    panel.current?.focus();
    const oldOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') onClose();
      if (event.key !== 'Tab') return;
      const items = panel.current?.querySelectorAll<HTMLElement>('button:not([disabled]), a[href], summary, input, select, [tabindex="0"]');
      if (!items?.length) return;
      const first = items[0]; const last = items[items.length - 1];
      if (event.shiftKey && (document.activeElement === first || document.activeElement === panel.current)) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    };
    document.addEventListener('keydown', onKey);
    return () => { document.body.style.overflow = oldOverflow; document.removeEventListener('keydown', onKey); previous?.focus(); };
  }, [onClose]);

  return <div className="drawer-backdrop" onMouseDown={event => { if (event.target === event.currentTarget) onClose(); }}>
    <aside className="detail-drawer" role="dialog" aria-modal="true" aria-labelledby="detail-title" tabIndex={-1} ref={panel}>
      <header className="drawer-header"><div><span className="eyebrow">RELATIONSHIP RECORD</span><h2 id="detail-title">关系研究档案</h2></div><button className="icon-button" onClick={onClose} aria-label="关闭关系详情"><X size={21} /></button></header>
      {knownAt && <p className="time-context">基于 {knownAt} 及之前已公开的证据重新评分。</p>}
      {relation.loading ? <Loading text="正在读取关系详情…" /> : relation.error ? <Failure message={relation.error} onRetry={() => setRevision(value => value + 1)} /> : relation.data && <div className="drawer-content">
        <div className="detail-intro"><Direction relation={relation.data} /><h3>{relation.data.business_description}</h3><div className="detail-badges"><span className={`status-label status-${relation.data.fact_status}`}>{statusLabels[relation.data.fact_status]}</span><span className="review-tag">待人工复核</span><span className="soft-tag">{temporalLabels[relation.data.temporal_status]}</span></div></div>
        <section className="detail-section"><h3><Clock3 size={17} />时间与结论边界</h3><dl className="detail-grid"><div><dt>关系开始</dt><dd>{dateLabel(relation.data.valid_from)}</dd></div><div><dt>关系结束</dt><dd>{dateLabel(relation.data.valid_to)}</dd></div><div><dt>当前持续性</dt><dd>{validityLabels[relation.data.score.current_validity]}</dd></div><div><dt>实体映射</dt><dd>{{ exact: '对应上市主体', mapped: '已映射母子公司', uncertain: '主体仍不确定' }[relation.data.entity_resolution]}</dd></div></dl><p>{relation.data.continuity_note}</p><div className="note-box"><strong>不确定性</strong><p>{relation.data.uncertainty || '当前记录未补充不确定性说明，仍需人工复核。'}</p></div>{relation.data.comparison_dimension && <p><strong>可比业务维度：</strong>{relation.data.comparison_dimension}</p>}<p><strong>量化信息：</strong>{relation.data.quantitative_context || '未建立可比金额或规模；缺少金额本身不等于关系不可信。'}</p></section>
        <section className="detail-section"><h3><ShieldCheck size={17} />可解释置信度 <span className="detail-score">{relation.data.score.total}<small>/100</small></span></h3><p className="muted">评估证据对具体结论的支持程度，不是投资价值、业务重要性或统计概率。</p><div className="score-components">{relation.data.score.components.map(component => <details key={component.key}><summary><span>{component.label}</span><b>{component.points} / {component.max_points}</b></summary><p>{component.reason}</p></details>)}</div><p>{relation.data.score.explanation}</p><p className="metadata-line">规则 v{relation.data.score.rule_version} · 计算于 {relation.data.score.calculated_at}</p></section>
        <section className="detail-section evidence-section"><h3><BookOpen size={17} />证据来源 <span className="section-count">{relation.data.evidence_count}</span></h3><p className="muted">{relation.data.independent_source_count} 个独立来源组；同一公告转载不增加独立性。</p>
          {evidence.loading ? <Loading text="正在加载证据…" /> : evidence.error ? <Failure message={evidence.error} onRetry={() => setRevision(value => value + 1)} /> : evidence.data?.items.length ? evidence.data.items.map(item => <EvidenceCard key={item.id} evidence={item} />) : <p className="note-box">该查询范围内尚无可展示证据，请勿仅依据关系标题作出判断。</p>}
        </section>
        <details className="identity-details"><summary>查看两端上市主体与别名</summary>{[relation.data.source_company, relation.data.target_company].map(company => <div key={company.id}><strong>{company.legal_name}</strong><p>{company.exchange} · {company.ticker} · {company.listing_status === 'listed' ? '上市公司' : company.listing_status}</p><p>别名：{company.aliases.join('、') || '无'}；母公司 ID：{company.parent_id || '无'}</p><p>{company.identity_notes}</p></div>)}</details>
        <p className="record-id">记录 ID · {relation.data.id}</p>
      </div>}
    </aside>
  </div>;
}

function EvidenceCard({ evidence }: { evidence: Evidence }) {
  // Snapshot URLs are data: only render ordinary HTTP(S) links as navigable sources.
  const safeUrl = /^https?:\/\//i.test(evidence.source_url) ? evidence.source_url : null;
  return <article className={`evidence-card ${evidence.stance === 'contradicts' ? 'conflicting' : ''}`}>
    <div className="evidence-top"><span><FileText size={14} />{{ regulatory: '监管披露', company: '公司官方', media: '媒体报道' }[evidence.source_type]}</span><span className={evidence.stance === 'contradicts' ? 'conflict-label' : 'support-label'}>{evidence.stance === 'contradicts' ? '反驳 / 冲突' : '支持结论'} · {evidence.directness === 'direct' ? '直接' : '间接'}</span></div>
    <h4>{safeUrl ? <a href={safeUrl} target="_blank" rel="noopener noreferrer">{evidence.title}<ArrowUpRight size={15} /></a> : evidence.title}</h4><p className="evidence-publisher">{evidence.publisher} · 发布于 {dateLabel(evidence.published_at)}</p>
    <blockquote>{evidence.excerpt}</blockquote><p className="evidence-locator"><strong>原文定位</strong> {evidence.evidence_locator}</p><p className="evidence-interpretation"><strong>研究解释</strong> {evidence.interpretation}</p>
    <details><summary>获取信息、独立性与使用限制</summary><dl><dt>实际获取时间</dt><dd>{evidence.retrieved_at}</dd><dt>独立来源组</dt><dd>{evidence.independence_key}</dd><dt>访问限制</dt><dd>{evidence.access_restrictions}</dd><dt>再分发说明</dt><dd>{evidence.redistribution_notes}</dd><dt>摘录 SHA-256</dt><dd className="hash">{evidence.content_sha256}</dd></dl></details>
  </article>;
}
