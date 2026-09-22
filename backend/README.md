# 后端开发说明

后端使用 FastAPI 提供 HTTP API，Typer 提供 CLI，两者共用业务服务。

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用工厂、生命周期和路由注册
│   ├── cli.py                  # Typer 命令入口
│   ├── api/
│   │   ├── router.py           # 汇总路由
│   │   ├── dependencies.py     # 请求级数据库会话和服务注入
│   │   ├── exception_handlers.py # HTTP 异常响应
│   │   └── endpoints/
│   │       ├── health.py       # 健康检查
│   │       ├── companies.py    # 公司、公司关系列表和关系图
│   │       └── relationships.py # 关系详情和证据
│   ├── models/                # SQLAlchemy 表模型
│   │   ├── company.py
│   │   ├── dataset.py
│   │   ├── evidence.py
│   │   ├── relationship.py     # 关系及关系与证据的关联表
│   │   └── score.py
│   ├── schemas/               # Pydantic 输入校验
│   │   ├── common.py           # 公共类型、枚举和校验基类
│   │   ├── company.py
│   │   ├── evidence.py
│   │   ├── relationship.py
│   │   ├── query.py            # 查询筛选条件
│   │   └── snapshot.py         # 快照完整性与跨实体校验
│   ├── services/
│   │   ├── research_service.py # 查询、时间过滤、分页和图数据
│   │   ├── import_service.py   # 快照校验与原子事务导入
│   │   └── scoring.py          # 证据评分规则
│   ├── core/
│   │   ├── config.py           # 环境变量与默认路径
│   │   └── errors.py           # HTTP 与 CLI 共用的业务异常
│   └── db/
│       ├── base.py             # SQLAlchemy 声明式基类
│       ├── session.py          # 引擎、SQLite 配置与建表
│       └── crud.py             # 通用数据库查询
└── tests/
    ├── conftest.py             # 合成数据、隔离数据库与 API fixture
    └── test_research.py         # 导入、查询、评分、HTTP 与 CLI 测试
```

各应用包均包含 `__init__.py`，上图省略重复项。路由负责解析 HTTP 参数并调用服务；业务规则集中于 `services`，普通数据库查询放在 `db/crud.py`。快照替换的完整事务保留在 `import_service.py`，便于审查其写入顺序和回滚边界。`models/__init__.py` 统一注册所有表，确保首次建表与跨模型关系解析完整。

## 运行与验证

在**仓库根目录**执行：

```sh
uv sync --frozen
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
uv run chainlens health --json
uv run pytest
uv run ruff check backend
```

Python 包由 `chainlens` 调整为 `app`，旧的 `chainlens.main:app` 启动路径改为 `app.main:app`；CLI 命令名仍为 `chainlens`，也可使用 `uv run python -m app.cli`。已有环境在更新代码后先执行 `uv sync --frozen`，以更新安装入口。

依赖仍统一维护于仓库根目录的 `pyproject.toml` 和 `uv.lock`。环境变量示例见根目录 `.env.example`；程序直接读取进程环境，不自动加载 `.env`。默认数据库和快照路径均相对于仓库根目录解析，不受启动目录影响。API 路径、参数、响应及数据库表结构保持不变。
