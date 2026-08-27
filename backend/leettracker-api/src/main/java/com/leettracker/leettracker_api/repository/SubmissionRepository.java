package com.leettracker.leettracker_api.repository;

import java.time.Duration;
import java.time.Instant;
import java.util.List;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import com.leettracker.leettracker_api.dto.RecentSubmissionResponse;

@Repository
public class SubmissionRepository {

    private final JdbcTemplate jdbcTemplate;

    public SubmissionRepository(
            JdbcTemplate jdbcTemplate
    ) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public List<RecentSubmissionResponse> getRecentSubmissions(
            long userId,
            int limit
    ) {

        // p.topics->>0 takes the first tag as a single representative
        // label — a problem can carry several tags, but the dashboard
        // shows one badge per submission.
        String sql = """
            SELECT
                p.title,
                sa.status,
                p.topics ->> 0 AS topic,
                sa.submitted_at

            FROM submission_attempts sa

            JOIN problems p
                ON p.id = sa.problem_id

            WHERE sa.user_id = ?

            ORDER BY sa.submitted_at DESC

            LIMIT ?
            """;

        return jdbcTemplate.query(
                sql,
                (rs, rowNum) -> {

                    RecentSubmissionResponse response =
                            new RecentSubmissionResponse();

                    response.setTitle(
                            rs.getString("title")
                    );

                    response.setStatus(
                            rs.getString("status")
                    );

                    response.setTopic(
                            rs.getString("topic")
                    );

                    Instant submittedAt =
                            rs.getTimestamp("submitted_at")
                                    .toInstant();

                    response.setWhen(
                            formatRelativeTime(submittedAt)
                    );

                    return response;
                },
                userId,
                limit
        );
    }

    private String formatRelativeTime(Instant submittedAt) {

        Duration elapsed = Duration.between(
                submittedAt,
                Instant.now()
        );

        long minutes = elapsed.toMinutes();

        if (minutes < 1) {
            return "just now";
        }

        if (minutes < 60) {
            return minutes + "m ago";
        }

        long hours = elapsed.toHours();

        if (hours < 24) {
            return hours + "h ago";
        }

        long days = elapsed.toDays();

        if (days < 30) {
            return days + "d ago";
        }

        long months = days / 30;

        return months + "mo ago";
    }
}
