import { ArrowUpRight, ChevronLeft, ChevronRight } from 'lucide-react';
import type { Page, Relationship } from '../types';
import { dateLabel, roleLabels, statusLabels, temporalLabels } from '../labels';

export function Direction({ relation }: { relation: Relationship }) {
  const symmetric = relation.relationship_type === 'partner' || relation.relationship_type === 'peer';
  return <span className="direction">{relation.source_company.display_name} <span aria-label={symmetric ? '对称关系' : '指向'}>{symmetric ? '↔' : '→'}</span> {relation.target_company.display_name}</span>;
}
export function RelationshipTable({ data, selected, onSelect, onPage }: { data: Page<Relationship>; selected: string | null; onSelect: (id: string) => void; onPage: (page: number) => void }) {
  const pageCount = Math.max(1, Math.ceil(data.total / data.page_size));
  return <>
    <div className="table-scroll"><table className="relationship-table"><thead><tr><th>关联公司 / 业务关系</th><th>类型与方向</th><th>事实状态</th><th>置信度</th><th>证据</th><th>关系时间</th><th><span className="sr-only">详情</span></th></tr></thead>
      <tbody>{data.items.map(relation => <tr key={relation.id} className={selected === relation.id ? 'selected' : ''}>
        <td><button className="company-link" onClick={() => onSelect(relation.id)} aria-label={`查看${relation.related_company?.display_name ?? relation.target_company.display_name}的${roleLabels[relation.queried_role]}关系`}><span className="company-avatar">{(relation.related_company?.ticker ?? relation.target_company.ticker).slice(0, 2)}</span><span><strong>{relation.related_company?.display_name ?? relation.target_company.display_name}</strong><small>{relation.related_company?.exchange} · {relation.related_company?.ticker}</small></span></button><p className="business-snippet" title={relation.business_description}>{relation.business_description}</p></td>
        <td><span className={`role-tag role-${relation.queried_role}`}>{roleLabels[relation.queried_role]}</span><Direction relation={relation} /></td>
        <td><span className={`status-label status-${relation.fact_status}`}>{statusLabels[relation.fact_status]}</span><small className="muted block">待人工复核</small></td>
        <td><div className="score-value">{relation.score.total}<span>/100</span></div><div className="score-track"><span style={{ width: `${relation.score.total}%` }} /></div></td>
        <td><span className="evidence-number">{relation.evidence_count}</span><small className="muted block">{relation.independent_source_count} 个独立来源</small></td>
        <td><span className="date-text">{dateLabel(relation.valid_from)}</span><small className="muted block">{temporalLabels[relation.temporal_status]}</small></td>
        <td><button className="icon-button" onClick={() => onSelect(relation.id)} aria-label={`打开关系 ${relation.id}`}><ArrowUpRight size={17} /></button></td>
      </tr>)}</tbody>
    </table></div>
    <div className="pagination"><span>显示 {(data.page - 1) * data.page_size + 1}–{Math.min(data.page * data.page_size, data.total)} 条，共 {data.total} 条</span><div><button className="icon-button" onClick={() => onPage(data.page - 1)} disabled={data.page <= 1} aria-label="上一页"><ChevronLeft size={17} /></button><span>{data.page} / {pageCount}</span><button className="icon-button" onClick={() => onPage(data.page + 1)} disabled={data.page >= pageCount} aria-label="下一页"><ChevronRight size={17} /></button></div></div>
  </>;
}
