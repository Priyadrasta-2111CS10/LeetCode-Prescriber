CREATE TABLE recommendation_history (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    problem_id BIGINT NOT NULL,
    topic VARCHAR(255) NOT NULL,
    recommended_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    plan_id VARCHAR(100)
);

CREATE INDEX idx_recommendation_history_user_date
ON recommendation_history(user_id, recommended_at);