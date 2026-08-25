package com.leettracker.leettracker_api.service;


import com.leettracker.leettracker_api.dto.TopicStatsResponse;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class WeaknessDetector {

    private static final int
            MIN_ATTEMPTS = 10;

    private static final double
            WEAK_ACCEPTANCE_RATE = 50.0;

    public List<TopicStatsResponse> detect(
            List<TopicStatsResponse> topicStats
    ) {

        return topicStats
                .stream()
                .filter(
                        stats ->
                                stats.getTotalAttempts()
                                        >= MIN_ATTEMPTS
                )
                .filter(
                        stats ->
                                stats.getAcceptanceRate()
                                        < WEAK_ACCEPTANCE_RATE
                )
                .toList();
    }
}
