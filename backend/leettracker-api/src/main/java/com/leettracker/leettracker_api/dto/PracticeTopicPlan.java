package com.leettracker.leettracker_api.dto;

import java.util.List;

public record PracticeTopicPlan(
        String topic,
        String goal,
        List<RecommendedProblem> problems) {
}
