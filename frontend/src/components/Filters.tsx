import { Search, SlidersHorizontal, RotateCcw } from 'lucide-react';
import type { Filters as FilterValues, RelationshipRole, FactStatus } from '../types';
import { roles, roleLabels, statusLabels } from '../labels';

interface Props { value: FilterValues; onChange: (value: FilterValues) => void; onReset: () => void; cutoff: string }
export function Filters({ value, onChange, onReset, cutoff }: Props) {
  const set = <K extends keyof FilterValues>(key: K, next: FilterValues[K]) => onChange({ ...value, [key]: next });
  return <section className="filter-panel" aria-label="关系筛选">
    <div className="filter-row">
      <label className="search-input"><Search size={18} /><span className="sr-only">关键词</span><input value={value.q} onChange={e => set('q', e.target.value)} placeholder="搜索公司、业务或关系…" type="search" /></label>
      <label className="filter-field">关系类型<select aria-label="关系类型" value={value.relationship_type} onChange={e => set('relationship_type', e.target.value as '' | RelationshipRole)}><option value="">全部类型</option>{roles.map(role => <option key={role} value={role}>{roleLabels[role]}</option>)}</select></label>
      <label className="filter-field">事实状态<select aria-label="事实状态" value={value.fact_status} onChange={e => set('fact_status', e.target.value as '' | FactStatus)}><option value="">全部状态</option>{Object.entries(statusLabels).map(([key, label]) => <option key={key} value={key}>{label}</option>)}</select></label>
      <label className="filter-field score-filter">最低置信度<div><input aria-label="最低置信度" type="number" min="0" max="100" value={value.min_confidence} onChange={e => set('min_confidence', Math.max(0, Math.min(100, Number(e.target.value))))} /><span>/ 100</span></div></label>
      <button className="icon-button reset-button" onClick={onReset} aria-label="重置全部筛选" title="重置全部筛选"><RotateCcw size={17} /></button>
    </div>
    <details className="time-filters"><summary><SlidersHorizontal size={14} />时间范围与排序{(value.known_at || value.valid_at) && <span className="active-dot">已启用</span>}</summary>
      <div className="time-filter-fields">
        <label className="filter-field">当时已公开的信息<input type="date" max={cutoff} value={value.known_at} onChange={e => set('known_at', e.target.value)} /></label>
        <label className="filter-field">关系有效日期<input type="date" max={cutoff} value={value.valid_at} onChange={e => set('valid_at', e.target.value)} /></label>
        <label className="filter-field">排序<select aria-label="排序" value={value.sort} onChange={e => set('sort', e.target.value as FilterValues['sort'])}><option value="confidence_desc">置信度从高到低</option><option value="company_asc">公司名称</option><option value="date_desc">关系时间从新到旧</option></select></label>
        <label className="checkbox-label"><input type="checkbox" checked={value.include_unknown_time} onChange={e => set('include_unknown_time', e.target.checked)} />有效日期筛选中纳入时间不确定项</label>
      </div>
      <p className="filter-explanation">“当时已公开”按来源发布日期筛选并重新评分，不代表当时已核验；“关系有效”按关系时间筛选。未知边界默认排除。日期不得晚于 {cutoff}。</p>
    </details>
  </section>;
}
