package com.leettracker.leettracker_api.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.leettracker.leettracker_api.dto.AnalyticsSummaryResponse;
import com.leettracker.leettracker_api.dto.DifficultyStatsResponse;
import com.leettracker.leettracker_api.dto.OverallStatsResponse;
import com.leettracker.leettracker_api.dto.TopicStatsResponse;
import com.leettracker.leettracker_api.service.AnalyticsService;

@RestController
@RequestMapping("/api/v1/users")
public class AnalyticsController {

    private final AnalyticsService analyticsService;

    public AnalyticsController(
            AnalyticsService analyticsService
    ) {
        this.analyticsService =
                analyticsService;
    }

    @GetMapping("/{username}/analytics")
    public OverallStatsResponse getOverallStats(
            @PathVariable String username) {

        return analyticsService
                .getOverallStats(
                        username
                );
    }

    @GetMapping(
        "/{username}/analytics/difficulty"
)
public List<DifficultyStatsResponse> getDifficultyStats(
        @PathVariable String username) {

    return analyticsService
            .getDifficultyStats(
                    username
            );
}

@GetMapping("/{username}/analytics/topics")
public List<TopicStatsResponse> getTopicStats(
        @PathVariable String username
) {

    return analyticsService
            .getTopicStats(
                    username
            );
}

@GetMapping(
        "/{username}/analytics/weaknesses"
)
public List<TopicStatsResponse> getWeakTopics(
        @PathVariable String username
) {

    return analyticsService
            .getWeakTopics(
                    username
            );
}

@GetMapping("/{username}/analytics/summary")
public AnalyticsSummaryResponse getSummary(
        @PathVariable String username) {

    return analyticsService.getSummary(username);
        }
}
