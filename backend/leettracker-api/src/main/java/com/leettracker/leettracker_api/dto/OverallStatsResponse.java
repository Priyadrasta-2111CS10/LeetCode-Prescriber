package com.leettracker.leettracker_api.dto;

import lombok.Data;

@Data
public class OverallStatsResponse {
    private long totalAttempts;
    private long acceptedAttempts;
    private long uniqueProblemsAttempted;
    private long uniqueProblemsSolved;
    private double acceptanceRate;

}
