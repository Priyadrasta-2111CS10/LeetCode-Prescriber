package com.leettracker.leettracker_api.config;

import org.apache.hc.client5.http.config.RequestConfig;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.util.Timeout;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.web.client.RestClient;

@Configuration
public class RestClientConfig {
    @Primary
    public RestClient.Builder restClientBuilder() {
        return RestClient.builder()
                .requestFactory(
                        createRequestFactory(10)
                );
    }

    @Bean
    public RestClient.Builder aiRestClientBuilder() {
        return RestClient.builder()
                .requestFactory(
                        createRequestFactory(120)
                );
    }

    private HttpComponentsClientHttpRequestFactory
        createRequestFactory(int responseTimeoutSeconds) {

    RequestConfig requestConfig =
            RequestConfig.custom()
                    .setConnectionRequestTimeout(
                            Timeout.ofSeconds(3)
                    )
                    .setConnectTimeout(
                            Timeout.ofSeconds(3)
                    )
                    .setResponseTimeout(
                            Timeout.ofSeconds(
                                    responseTimeoutSeconds
                            )
                    )
                    .build();

    CloseableHttpClient httpClient =
            HttpClients.custom()
                    .setDefaultRequestConfig(
                            requestConfig
                    )
                    .build();

    return new HttpComponentsClientHttpRequestFactory(
            httpClient
    );
}
}