package com.leettracker.leettracker_api.client;


import java.util.List;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

import com.leettracker.leettracker_api.dto.PracticeTopicPlan;

@Component
public class PythonPracticePlanClient {

    private final RestClient restClient;

    public PythonPracticePlanClient(
            @Qualifier("aiRestClientBuilder")
            RestClient.Builder builder,
            @Value("${leettracker.python.base-url}")
            String baseUrl
    ) {
        this.restClient = builder
                .baseUrl(baseUrl)
                .build();
    }

    public List<PracticeTopicPlan> getPracticePlan(
        String username
) {
    return restClient
            .get()
            .uri(
                    "/internal/users/{username}/practice-plan",
                    username
            )
            .retrieve()
            .body(
                    new ParameterizedTypeReference<
                            List<PracticeTopicPlan>
                    >() {}
            );
}
}