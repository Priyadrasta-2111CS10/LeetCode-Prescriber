package com.leettracker.leettracker_api.service;

import java.util.List;

import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import com.leettracker.leettracker_api.client.PythonPracticePlanClient;
import com.leettracker.leettracker_api.dto.PracticePlanResponse;
import com.leettracker.leettracker_api.dto.PracticeTopicPlan;
import com.leettracker.leettracker_api.exception.PythonServiceException;

import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import io.github.resilience4j.retry.annotation.Retry;

@Service
public class PracticePlanService {

    private final PythonPracticePlanClient client;

    public PracticePlanService(
            PythonPracticePlanClient client
    ) {
        this.client = client;
    }

    @Cacheable(
        value = "practicePlan",
        key = "#username"
)
    @CircuitBreaker(
            name = "pythonPracticePlan",
            fallbackMethod = "fallback"
    )
    @Retry(
            name = "pythonPracticePlan"
    )
    public List<PracticeTopicPlan> generatePlan(
            String username
    ) {

        return client.getPracticePlan(
                username
        );
    }

    private PracticePlanResponse fallback(
            String username,
            Throwable throwable
    ) {

        throw new PythonServiceException(
                "Practice plan service is currently unavailable",
                throwable
        );
    }
}