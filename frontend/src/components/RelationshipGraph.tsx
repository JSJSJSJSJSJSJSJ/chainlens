import { useMemo } from 'react';
import dagre from '@dagrejs/dagre';
import { ReactFlow, Background, Controls, MarkerType, BaseEdge, EdgeLabelRenderer, Handle, Position } from '@xyflow/react';
import type { NodeProps, EdgeProps, Node, Edge } from '@xyflow/react';
import type { Company, Graph, Relationship } from '../types';
import { roleLabels, roleColors, roles } from '../labels';
import '@xyflow/react/dist/style.css';

type CompanyNode = Node<{ company: Company; central: boolean }, 'company'>;
type RelationEdge = Edge<{ relation: Relationship; offset: number; onSelect: (id: string) => void }, 'relation'>;

function CompanyGraphNode({ data }: NodeProps<CompanyNode>) {
  return <div className={`graph-company ${data.central ? 'central-company' : ''}`}>
    <Handle type="target" position={Position.Left} /><Handle type="source" position={Position.Right} />
    <span className="graph-ticker">{data.company.ticker}</span><strong>{data.company.display_name}</strong><small>{data.central ? '研究中心' : data.company.exchange}</small>
  </div>;
}

function RelationshipEdge({ id, sourceX, sourceY, targetX, targetY, markerEnd, data, selected }: EdgeProps<RelationEdge>) {
  if (!data) return null;
  // Each parallel relationship gets its own curve and keyboard-focusable label.
  const centerX = (sourceX + targetX) / 2;
  const centerY = (sourceY + targetY) / 2 + data.offset;
  const path = `M ${sourceX},${sourceY} C ${centerX},${sourceY + data.offset * 1.33} ${centerX},${targetY + data.offset * 1.33} ${targetX},${targetY}`;
  return <>
    <BaseEdge id={id} path={path} markerEnd={markerEnd} style={{ stroke: roleColors[data.relation.queried_role], strokeWidth: selected ? 3 : 1.7 }} interactionWidth={20} />
    <EdgeLabelRenderer><button className={`graph-edge-label nodrag nopan ${selected ? 'selected' : ''}`} style={{ transform: `translate(-50%, -50%) translate(${centerX}px, ${centerY}px)`, borderColor: roleColors[data.relation.queried_role] }} title={data.relation.business_description} onClick={() => data.onSelect(id)} aria-label={`查看图中${data.relation.related_company?.display_name ?? data.relation.target_company.display_name}的${roleLabels[data.relation.queried_role]}关系`}>
      {roleLabels[data.relation.queried_role]} <span>{data.relation.score.total}</span>
    </button></EdgeLabelRenderer>
  </>;
}
const nodeTypes = { company: CompanyGraphNode };
const edgeTypes = { relation: RelationshipEdge };

export function RelationshipGraph({ data, companyId, selected, onSelect }: { data: Graph; companyId: string; selected: string | null; onSelect: (id: string) => void }) {
  const { nodes, edges } = useMemo(() => {
    const layout = new dagre.graphlib.Graph({ multigraph: true });
    layout.setGraph({ rankdir: 'LR', nodesep: 65, ranksep: 225, marginx: 35, marginy: 50 });
    layout.setDefaultEdgeLabel(() => ({}));
    for (const company of data.nodes) layout.setNode(company.id, { width: 180, height: 86 });
    for (const relation of data.edges) {
      layout.setEdge(relation.source_company_id, relation.target_company_id, {}, relation.id);
    }
    dagre.layout(layout);
    const nodes: CompanyNode[] = data.nodes.map(company => {
      const position = layout.node(company.id) as { x: number; y: number };
      return { id: company.id, type: 'company', position: { x: position.x - 90, y: position.y - 43 }, data: { company, central: company.id === companyId } };
    });
    const parallel = new Map<string, Relationship[]>();
    for (const relation of data.edges) {
      const pair = [relation.source_company_id, relation.target_company_id].sort().join('|');
      parallel.set(pair, [...(parallel.get(pair) ?? []), relation]);
    }
    const edges: RelationEdge[] = data.edges.map(relation => {
      const group = parallel.get([relation.source_company_id, relation.target_company_id].sort().join('|'))!;
      const offset = (group.findIndex(item => item.id === relation.id) - (group.length - 1) / 2) * 46;
      const symmetric = relation.relationship_type === 'partner' || relation.relationship_type === 'peer';
      return { id: relation.id, source: relation.source_company_id, target: relation.target_company_id, type: 'relation', selected: selected === relation.id, data: { relation, offset, onSelect }, markerEnd: symmetric ? undefined : { type: MarkerType.ArrowClosed, color: roleColors[relation.queried_role] }, ariaLabel: relation.business_description };
    });
    return { nodes, edges };
  }, [data, companyId, selected, onSelect]);

  return <div className="graph-section">
    <div className="graph-legend">{roles.map(role => <span key={role}><i style={{ background: roleColors[role] }} />{roleLabels[role]}</span>)}<span className="legend-direction">→ 供应方至采购方 / 投资方至被投资方；无箭头为对称关系</span></div>
    <div className="graph-canvas" role="region" aria-label="可交互关系图"><ReactFlow nodes={nodes} edges={edges} nodeTypes={nodeTypes} edgeTypes={edgeTypes} fitView minZoom={0.15} maxZoom={1.8} nodesDraggable={false} nodesConnectable={false} onEdgeClick={(_, edge) => onSelect(edge.id)} proOptions={{ hideAttribution: true }}><Background color="#d6ded9" gap={22} /><Controls showInteractive={false} /></ReactFlow></div>
    <p className="graph-scope">显示 {data.displayed} / {data.total} 条关系 · {data.scope_note}{data.truncated && `（图最多展示 ${data.limit} 条，请缩小筛选范围。）`} 点击关系标签查看证据，使用左下角按钮缩放。</p>
  </div>;
}
