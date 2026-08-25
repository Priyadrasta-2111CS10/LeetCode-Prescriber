package com.leettracker.leettracker_api.dto;

import java.util.List;

public record PracticePlanResponse(
        String username,
        List<PracticeTopicPlan> plans
) {
}