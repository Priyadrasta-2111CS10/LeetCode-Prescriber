package com.leettracker.leettracker_api.client;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;
import com.leettracker.leettracker_api.dto.SyncResult;
import com.leettracker.leettracker_api.exception.PythonServiceException;


@Component
public class PythonSyncClient {
        private final RestClient restClient;

    public PythonSyncClient(
            RestClient.Builder builder,
            @Value("${leettracker.python.base-url}")
            String baseUrl
    ) {

        this.restClient = builder
                .baseUrl(baseUrl)
                .build();
    }

    public SyncResult syncUser(
            String username
    ) {

        try {

            return restClient
                    .post()
                    .uri(
                            "/internal/users/{username}/sync",
                            username
                    )
                    .retrieve()
                    .body(SyncResult.class);

        } catch (Exception exc) {

            throw new PythonServiceException(
                    "Failed to synchronize user "
                            + username
                            + " using Python service",
                    exc
            );
        }
    }
}