package com.leettracker.leettracker_api.dto;

import lombok.Data;

@Data
public class DifficultyStatsResponse {
    private String difficulty;

    private long totalAttempts;

    private long acceptedAttempts;

    private long uniqueProblemsSolved;

    private double acceptanceRate;

}
