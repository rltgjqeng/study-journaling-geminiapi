-- 서버 DB (web_db.db)에서 사용할 스키마

-- 질문 테이블 (question.db에 사용)
CREATE TABLE IF NOT EXISTS question (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    highlight TEXT NOT NULL,
    memo TEXT DEFAULT '',
    source TEXT NOT NULL
);

-- 이벤트 후보 테이블 (question_candidate.db에 사용)
CREATE TABLE IF NOT EXISTS question_candidate (
    id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    source TEXT NOT NULL,
    question_text TEXT NOT NULL,
    confirmed INTEGER DEFAULT 0
);
