export type RelationshipRole = 'supplier' | 'customer' | 'partner' | 'investor_or_investee' | 'peer';
export type FactStatus = 'confirmed' | 'inferred' | 'unknown';
export interface Company {
  id: string; legal_name: string; display_name: string; aliases: string[];
  ticker: string; exchange: string; listing_status: string; parent_id: string | null; identity_notes: string;
}
export interface Dataset {
  dataset_version: string; research_cutoff: string; score_version: string; created_at: string;
  description: string; gaps: string[];
}
export interface CompanyDetail extends Company {
  summary: { relationship_count: number; evidence_count: number; related_company_count: number; distribution: Record<RelationshipRole, number> };
  dataset: Dataset;
}
export interface Score {
  total: number; rule_version: string; calculated_at: string;
  components: { key: string; label: string; points: number; max_points: number; reason: string }[];
  explanation: string; current_validity: 'supported' | 'historical_only' | 'unestablished';
}
export interface Relationship {
  id: string; source_company_id: string; target_company_id: string;
  relationship_type: Exclude<RelationshipRole, 'customer'>; queried_role: RelationshipRole;
  business_description: string; fact_status: FactStatus; valid_from: string | null; valid_to: string | null;
  temporal_status: 'historical' | 'current' | 'unknown'; continuity_note: string; uncertainty: string;
  human_review_status: 'pending' | 'review_prepared' | 'approved'; entity_resolution: 'exact' | 'mapped' | 'uncertain';
  comparison_dimension: string | null; quantitative_context: string | null;
  evidence_links: { evidence_id: string; stance: 'supports' | 'contradicts'; directness: 'direct' | 'indirect' }[];
  source_company: Company; target_company: Company; related_company: Company | null;
  evidence_count: number; independent_source_count: number; score: Score;
}
export interface Evidence {
  id: string; title: string; source_url: string; publisher: string; published_at: string | null;
  retrieved_at: string; evidence_locator: string; excerpt: string; interpretation: string;
  source_type: 'regulatory' | 'company' | 'media'; independence_key: string;
  content_sha256: string; access_restrictions: string; redistribution_notes: string;
  stance: 'supports' | 'contradicts'; directness: 'direct' | 'indirect';
}
export interface Page<T> { items: T[]; total: number; page: number; page_size: number }
export interface Graph { nodes: Company[]; edges: Relationship[]; total: number; displayed: number; truncated: boolean; limit: number; scope_note: string }
export interface Filters {
  q: string; relationship_type: '' | RelationshipRole; min_confidence: number;
  fact_status: '' | FactStatus; known_at: string; valid_at: string; include_unknown_time: boolean;
  sort: 'confidence_desc' | 'company_asc' | 'date_desc';
}
