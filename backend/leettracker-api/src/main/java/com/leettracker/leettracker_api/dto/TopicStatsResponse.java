package com.leettracker.leettracker_api.dto;

import lombok.Data;

@Data
public class TopicStatsResponse {
    private String topic;
    private long totalAttempts;
    private long acceptedAttempts;
    private long uniqueProblemsSolved;
    private double acceptanceRate;

}
