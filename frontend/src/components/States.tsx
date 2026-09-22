import { AlertCircle, LoaderCircle, SearchX } from 'lucide-react';

export function Loading({ text = '正在读取研究快照…' }: { text?: string }) {
  return <div className="state-panel" role="status"><LoaderCircle className="spin" size={24} /><p>{text}</p><span>结论、来源与评分同步加载</span></div>;
}
export function Failure({ message, onRetry }: { message: string; onRetry: () => void }) {
  return <div className="state-panel failure" role="alert"><AlertCircle size={26} /><h3>暂时无法读取数据</h3><p>{message}</p><button className="button" onClick={onRetry}>重新加载</button></div>;
}
export function Empty({ onReset }: { onReset: () => void }) {
  return <div className="state-panel"><SearchX size={30} /><h3>没有符合条件的关系</h3><p>试试减少筛选条件，或扩大时间范围。</p><button className="button" onClick={onReset}>清除筛选</button></div>;
}
