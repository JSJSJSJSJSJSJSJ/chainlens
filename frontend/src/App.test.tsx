import { act, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import App from './App';
import { useResource } from './hooks/useResource';
import { detail, relation, evidence } from './test/fixtures';

vi.mock('./components/RelationshipGraph', () => ({ RelationshipGraph: () => <div>测试图占位</div> }));
const response = (data: unknown, ok = true) => ({ ok, status: ok ? 200 : 503, json: async () => data }) as Response;
function installFetch(options: { empty?: boolean; noEvidence?: boolean; fail?: boolean } = {}) {
  return vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (options.fail) return response({ error: { message: '测试服务不可用' } }, false);
    if (url.endsWith('/companies/nvidia')) return response(detail);
    if (url.includes('/evidence')) return response({ items: options.noEvidence ? [] : [evidence], total: options.noEvidence ? 0 : 1 });
    if (url.includes('/relationships/test-relation')) return response(relation);
    return response({ items: options.empty ? [] : [relation], total: options.empty ? 0 : 1, page: 1, page_size: 10 });
  }));
}
describe('研究工作台（合成数据）', () => {
  it('loads data, shares filter query, opens details and evidence, closes with Escape', async () => {
    installFetch(); const user = userEvent.setup(); render(<App />);
    expect(screen.getByRole('status')).toHaveTextContent('正在读取研究快照');
    await screen.findByRole('button', { name: '查看合成供应商的供应商关系' });
    await user.selectOptions(screen.getByLabelText('关系类型'), 'supplier');
    await waitFor(() => expect(fetch).toHaveBeenCalledWith(expect.stringContaining('relationship_type=supplier'), expect.anything()));
    await user.click(await screen.findByRole('button', { name: '查看合成供应商的供应商关系' }));
    const dialog = await screen.findByRole('dialog');
    expect(await within(dialog).findByRole('link', { name: /合成证据公告/ })).toHaveAttribute('href', 'https://example.com/synthetic');
    expect(within(dialog).getByText('合成第1段', { exact: false })).toBeVisible();
    await user.keyboard('{Escape}'); expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: '关系图谱' }));
    await waitFor(() => expect(fetch).toHaveBeenCalledWith(expect.stringMatching(/graph\?.*relationship_type=supplier/), expect.anything()));
  });
  it('shows empty results and can clear filters', async () => {
    installFetch({ empty: true }); render(<App />);
    expect(await screen.findByText('没有符合条件的关系')).toBeVisible();
    await userEvent.click(screen.getByRole('button', { name: '清除筛选' }));
    expect(screen.getByLabelText('关键词')).toHaveValue('');
  });
  it('shows a request error and retry succeeds', async () => {
    installFetch({ fail: true }); render(<App />);
    expect(await screen.findByRole('alert')).toHaveTextContent('测试服务不可用');
    installFetch(); await userEvent.click(screen.getByRole('button', { name: '重新加载' }));
    expect(await screen.findByRole('button', { name: '查看合成供应商的供应商关系' })).toBeVisible();
  });
  it('handles missing evidence without presenting a source', async () => {
    installFetch({ noEvidence: true }); render(<App />);
    await userEvent.click(await screen.findByRole('button', { name: '查看合成供应商的供应商关系' }));
    expect(await screen.findByText(/尚无可展示证据/)).toBeVisible();
  });
  it('a slow obsolete response cannot overwrite the latest request', async () => {
    let resolveOld!: (value: Response) => void;
    vi.stubGlobal('fetch', vi.fn((url: string) => url === '/old' ? new Promise<Response>(resolve => { resolveOld = resolve; }) : Promise.resolve(response({ value: 'new' }))));
    function Probe({ path }: { path: string }) { const state = useResource<{ value: string }>(path); return <span>{state.data?.value ?? 'loading'}</span>; }
    const view = render(<Probe path="/old" />); view.rerender(<Probe path="/new" />);
    expect(await screen.findByText('new')).toBeVisible();
    await act(async () => resolveOld(response({ value: 'old' })));
    expect(screen.queryByText('old')).not.toBeInTheDocument(); expect(screen.getByText('new')).toBeVisible();
  });
});
