import type { FactStatus, Filters, RelationshipRole } from './types';

export const roles: RelationshipRole[] = ['supplier', 'customer', 'partner', 'investor_or_investee', 'peer'];
export const roleLabels: Record<RelationshipRole, string> = { supplier: '供应商', customer: '客户', partner: '合作伙伴', investor_or_investee: '投资关系', peer: '可比公司' };
export const roleColors: Record<RelationshipRole, string> = { supplier: '#168467', customer: '#4b75a6', partner: '#97823c', investor_or_investee: '#9766aa', peer: '#73818e' };
export const statusLabels: Record<FactStatus, string> = { confirmed: '事实已证实', inferred: '有据推断', unknown: '证据不足' };
export const temporalLabels = { historical: '历史关系', current: '截至截止日有效', unknown: '持续性未确定' };
export const validityLabels = { supported: '当前持续性有依据', historical_only: '仅支持历史关系', unestablished: '当前持续性未确立' };
export const defaultFilters: Filters = { q: '', relationship_type: '', min_confidence: 0, fact_status: '', known_at: '', valid_at: '', include_unknown_time: false, sort: 'confidence_desc' };
export const dateLabel = (date: string | null) => date ? date.slice(0, 10) : '未知';
