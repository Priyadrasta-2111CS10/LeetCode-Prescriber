CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,

    username VARCHAR(100) NOT NULL UNIQUE,

    ranking INTEGER,
    real_name VARCHAR(255),
    about_me TEXT,
    school VARCHAR(255),
    country_name VARCHAR(100),
    company VARCHAR(255),
    job_title VARCHAR(255),

    github_url TEXT,
    twitter_url TEXT,
    linkedin_url TEXT,
    avatar_url TEXT,

    websites JSONB,
    skill_tags JSONB,

    reputation INTEGER,
    solution_count INTEGER,
    category_discuss_count INTEGER,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE TABLE problems (
    id BIGSERIAL PRIMARY KEY,

    question_id VARCHAR(50) NOT NULL UNIQUE,
    frontend_id VARCHAR(50) NOT NULL,

    title VARCHAR(500) NOT NULL,
    title_slug VARCHAR(500) NOT NULL UNIQUE,

    difficulty VARCHAR(20) NOT NULL,

    topics JSONB NOT NULL DEFAULT '[]',

    is_paid_only BOOLEAN NOT NULL DEFAULT FALSE,

    acceptance_rate NUMERIC(6, 3),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT problems_difficulty_check
        CHECK (
            difficulty IN (
                'Easy',
                'Medium',
                'Hard'
            )
        ),

    CONSTRAINT problems_acceptance_rate_check
        CHECK (
            acceptance_rate IS NULL
            OR (
                acceptance_rate >= 0
                AND acceptance_rate <= 100
            )
        )
);


CREATE TABLE submissions (
    id BIGSERIAL PRIMARY KEY,

    leetcode_submission_id VARCHAR(100) NOT NULL UNIQUE,

    user_id BIGINT NOT NULL,

    problem_id BIGINT NOT NULL,

    submitted_at TIMESTAMPTZ NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT submissions_user_fk
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT submissions_problem_fk
        FOREIGN KEY (problem_id)
        REFERENCES problems(id)
        ON DELETE RESTRICT
);


CREATE TABLE sync_metadata (
    id BIGSERIAL PRIMARY KEY,

    user_id BIGINT NOT NULL UNIQUE,

    last_sync_started_at TIMESTAMPTZ,

    last_sync_completed_at TIMESTAMPTZ,

    last_submission_timestamp TIMESTAMPTZ,

    last_submission_id VARCHAR(100),

    sync_status VARCHAR(20) NOT NULL DEFAULT 'SUCCESS',

    last_error TEXT,

    CONSTRAINT sync_metadata_user_fk
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT sync_status_check
        CHECK (
            sync_status IN (
                'RUNNING',
                'SUCCESS',
                'FAILED'
            )
        )
);

CREATE INDEX IF NOT EXISTS idx_submissions_user_id
ON submissions(user_id);

CREATE INDEX IF NOT EXISTS idx_submissions_problem_id
ON submissions(problem_id);

CREATE INDEX IF NOT EXISTS idx_submissions_submitted_at
ON submissions(submitted_at DESC);

CREATE INDEX IF NOT EXISTS idx_submissions_user_time
ON submissions(user_id, submitted_at DESC);