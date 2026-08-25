package com.leettracker.leettracker_api.dto;

import java.util.List;

import lombok.Data;

@Data
public class AnalyticsSummaryResponse {
    private OverallStatsResponse overall;
    private List<DifficultyStatsResponse> difficulty;
    private List<TopicStatsResponse> topics;
    private List<TopicStatsResponse> weaknesses;

}
