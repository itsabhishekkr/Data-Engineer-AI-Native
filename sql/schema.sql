CREATE TABLE news_events_clean (
    record_id TEXT PRIMARY KEY,
    title TEXT,
    description TEXT,
    category TEXT,
    event_type TEXT,
    company_name TEXT,
    person_name TEXT,
    source_url TEXT,
    market TEXT,
    event_date DATE,
    cleaned_timestamp TIMESTAMP
);

CREATE TABLE quality_verdicts (
    verdict_id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id TEXT,
    check_name TEXT,
    check_type TEXT,
    verdict TEXT,
    confidence REAL,
    reason TEXT,
    suggested_value TEXT,
    model_name TEXT,
    prompt_version TEXT,
    latency_ms INTEGER,
    estimated_cost_usd REAL,
    created_at TIMESTAMP
);

CREATE TABLE human_review_queue (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id TEXT,
    issue_type TEXT,
    reason TEXT,
    priority TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP
);

CREATE TABLE dq_daily_metrics (
    metric_date DATE,
    check_name TEXT,
    check_type TEXT,
    total_records INTEGER,
    passed_records INTEGER,
    failed_records INTEGER,
    review_records INTEGER,
    avg_confidence REAL,
    avg_latency_ms REAL,
    total_cost_usd REAL
);