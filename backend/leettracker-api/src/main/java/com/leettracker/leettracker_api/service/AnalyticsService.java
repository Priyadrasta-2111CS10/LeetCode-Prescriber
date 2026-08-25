package com.leettracker.leettracker_api.service;

import java.util.List;

import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import com.leettracker.leettracker_api.dto.AnalyticsSummaryResponse;
import com.leettracker.leettracker_api.dto.DifficultyStatsResponse;
import com.leettracker.leettracker_api.dto.OverallStatsResponse;
import com.leettracker.leettracker_api.dto.TopicStatsResponse;
import com.leettracker.leettracker_api.model.User;
import com.leettracker.leettracker_api.repository.AnalyticsRepository;

@Service
public class AnalyticsService {
    private final AnalyticsRepository analyticsRepository;
    private final WeaknessDetector weaknessDetector;

    private final UserService userService;

    public AnalyticsService(
            AnalyticsRepository analyticsRepository,
            UserService userService,
            WeaknessDetector weaknessDetector
    ) {
        this.analyticsRepository = analyticsRepository;
        this.weaknessDetector = weaknessDetector;
        this.userService = userService;
    }

    public OverallStatsResponse getOverallStats(
            String username
    ) {

        User user =
                userService.getUser(
                        username
                );

        return analyticsRepository
                .getOverallStats(
                        user.getId()
                );
    }

    public List<DifficultyStatsResponse> getDifficultyStats(
        String username
) {

    User user =
            userService.getUser(
                    username
            );

    return analyticsRepository
            .getDifficultyStats(
                    user.getId()
            );
}

public List<TopicStatsResponse> getTopicStats(
        String username
) {

    User user =
            userService.getUser(
                    username
            );

    return analyticsRepository
            .getTopicStats(
                    user.getId()
            );
}

public List<TopicStatsResponse> getWeakTopics(
        String username
) {

    List<TopicStatsResponse> topicStats =
            getTopicStats(username);

    return weaknessDetector.detect(
            topicStats
    );
}

@Cacheable(
        value = "analytics",
        key = "#username"
)
public AnalyticsSummaryResponse getSummary(
        String username
) {

    AnalyticsSummaryResponse response = new AnalyticsSummaryResponse();

    response.setOverall(getOverallStats(username));
    response.setDifficulty( getDifficultyStats(username));
    response.setTopics(getTopicStats(username));
    response.setWeaknesses(getWeakTopics(username));
    return response;
}

}
