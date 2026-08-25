package com.leettracker.leettracker_api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Data;

@Data
public class SyncResult {

    private String username;

    @JsonProperty("new_attempts")
    private int newAttempts;

    @JsonProperty("existing_attempts")
    private int existingAttempts;

    @JsonProperty("new_solved_problems")
    private int newSolvedProblems;

    @JsonProperty("total_attempts_processed")
    private int totalAttemptsProcessed;
}