package com.leettracker.leettracker_api.repository;

import java.util.List;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import com.leettracker.leettracker_api.dto.DifficultyStatsResponse;
import com.leettracker.leettracker_api.dto.OverallStatsResponse;
import com.leettracker.leettracker_api.dto.TopicStatsResponse;


@Repository
public class AnalyticsRepository {
    private final JdbcTemplate jdbcTemplate;

    public AnalyticsRepository(
            JdbcTemplate jdbcTemplate
    ) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public OverallStatsResponse getOverallStats(
            long userId
    ) {

        String sql = """
            SELECT
                COUNT(*) AS total_attempts,

                COUNT(*) FILTER (
                    WHERE status = 'Accepted'
                ) AS accepted_attempts,

                COUNT(
                    DISTINCT problem_id
                ) AS unique_problems_attempted,

                COUNT(
                    DISTINCT problem_id
                ) FILTER (
                    WHERE status = 'Accepted'
                ) AS unique_problems_solved

            FROM submission_attempts

            WHERE user_id = ?
            """;

        return jdbcTemplate.queryForObject(
                sql,
                (rs, rowNum) -> {

                    OverallStatsResponse response =
                            new OverallStatsResponse();

                    long total =
                            rs.getLong(
                                    "total_attempts"
                            );

                    long accepted =
                            rs.getLong(
                                    "accepted_attempts"
                            );

                    response.setTotalAttempts(
                            total
                    );

                    response.setAcceptedAttempts(
                            accepted
                    );

                    response.setUniqueProblemsAttempted(
                            rs.getLong(
                                    "unique_problems_attempted"
                            )
                    );

                    response.setUniqueProblemsSolved(
                            rs.getLong(
                                    "unique_problems_solved"
                            )
                    );

                    response.setAcceptanceRate(
                            total == 0
                                    ? 0.0
                                    : accepted * 100.0 / total
                    );

                    return response;
                },
                userId
        );
    }

    public List<DifficultyStatsResponse> getDifficultyStats(
        long userId
) {

    String sql = """
        SELECT
            p.difficulty,

            COUNT(sa.id) AS total_attempts,

            COUNT(sa.id) FILTER (
                WHERE sa.status = 'Accepted'
            ) AS accepted_attempts,

            COUNT(
                DISTINCT sa.problem_id
            ) FILTER (
                WHERE sa.status = 'Accepted'
            ) AS unique_problems_solved

        FROM submission_attempts sa

        JOIN problems p
            ON p.id = sa.problem_id

        WHERE sa.user_id = ?

        GROUP BY p.difficulty

        ORDER BY
            CASE p.difficulty
                WHEN 'Easy' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'Hard' THEN 3
            END
        """;

    return jdbcTemplate.query(
            sql,
            (rs, rowNum) -> {

                DifficultyStatsResponse response =
                        new DifficultyStatsResponse();

                long total =
                        rs.getLong(
                                "total_attempts"
                        );

                long accepted =
                        rs.getLong(
                                "accepted_attempts"
                        );

                response.setDifficulty(
                        rs.getString(
                                "difficulty"
                        )
                );

                response.setTotalAttempts(
                        total
                );

                response.setAcceptedAttempts(
                        accepted
                );

                response.setUniqueProblemsSolved(
                        rs.getLong(
                                "unique_problems_solved"
                        )
                );

                response.setAcceptanceRate(
                        total == 0
                                ? 0.0
                                : accepted * 100.0 / total
                );

                return response;
            },
            userId
    );

}

public List<TopicStatsResponse> getTopicStats(
        long userId
) {

    String sql = """
        SELECT
            topic,

            COUNT(sa.id)
                AS total_attempts,

            COUNT(sa.id) FILTER (
                WHERE sa.status = 'Accepted'
            ) AS accepted_attempts,

            COUNT(
                DISTINCT sa.problem_id
            ) FILTER (
                WHERE sa.status = 'Accepted'
            ) AS unique_problems_solved

        FROM submission_attempts sa

        JOIN problems p
            ON p.id = sa.problem_id

        CROSS JOIN LATERAL
            jsonb_array_elements_text(
                p.topics
            ) AS topic

        WHERE sa.user_id = ?

        GROUP BY topic

        ORDER BY
            COUNT(sa.id) DESC
        """;

    return jdbcTemplate.query(
            sql,
            (rs, rowNum) -> {

                TopicStatsResponse response =
                        new TopicStatsResponse();

                long total =
                        rs.getLong(
                                "total_attempts"
                        );

                long accepted =
                        rs.getLong(
                                "accepted_attempts"
                        );

                response.setTopic(
                        rs.getString("topic")
                );

                response.setTotalAttempts(
                        total
                );

                response.setAcceptedAttempts(
                        accepted
                );

                response.setUniqueProblemsSolved(
                        rs.getLong(
                                "unique_problems_solved"
                        )
                );

                response.setAcceptanceRate(
                        total == 0
                                ? 0.0
                                : accepted * 100.0 / total
                );

                return response;
            },
            userId
    );
}
}

