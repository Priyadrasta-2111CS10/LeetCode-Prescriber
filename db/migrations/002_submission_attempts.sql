CREATE TABLE submission_attempts (
    id BIGSERIAL PRIMARY KEY,

    leetcode_submission_id VARCHAR(100) NOT NULL UNIQUE,

    user_id BIGINT NOT NULL,

    problem_id BIGINT NOT NULL,

    status VARCHAR(100) NOT NULL,

    language VARCHAR(50),

    runtime VARCHAR(100),

    memory VARCHAR(100),

    submitted_at TIMESTAMPTZ NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT submission_attempts_user_fk
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT submission_attempts_problem_fk
        FOREIGN KEY (problem_id)
        REFERENCES problems(id)
        ON DELETE RESTRICT
);


CREATE INDEX idx_submission_attempts_user_time
ON submission_attempts(user_id, submitted_at DESC);


CREATE INDEX idx_submission_attempts_problem
ON submission_attempts(problem_id);


CREATE INDEX idx_submission_attempts_status
ON submission_attempts(status);