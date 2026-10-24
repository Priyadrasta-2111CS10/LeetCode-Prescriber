package com.leettracker.leettracker_api.controller;

import java.util.List;
import java.util.Map;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
git 
@RestController
@RequestMapping("/api/v1/problems")
public class ProblemController {

    private final JdbcTemplate jdbcTemplate;

    public ProblemController(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    @GetMapping
    public Map<String, Object> getProblems(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "50") int size) {

        if (page < 0 || size < 1 || size > 100) {
            throw new IllegalArgumentException(
                    "page must be >= 0 and size must be between 1 and 100");
        }

        Long total = jdbcTemplate.queryForObject(
                "SELECT COUNT(*) FROM problems",
                Long.class);

        List<Map<String, Object>> problems = jdbcTemplate.queryForList(
                """
                SELECT id, question_id, frontend_id, title,
                       title_slug, difficulty, topics::text AS topics,
                       is_paid_only, acceptance_rate
                FROM problems
                ORDER BY id
                LIMIT ? OFFSET ?
                """,
                size,
                page * size);

        return Map.of(
                "items", problems,
                "page", page,
                "size", size,
                "total", total == null ? 0L : total,
                "totalPages", total == null ? 0 : (int) Math.ceil(
                        (double) total / size));
    }
}