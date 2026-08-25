package com.leettracker.leettracker_api.config;

import java.time.Duration;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.cache.RedisCacheConfiguration;
import org.springframework.data.redis.cache.RedisCacheManager;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.serializer.JacksonJsonRedisSerializer;
import org.springframework.data.redis.serializer.RedisSerializationContext;
import org.springframework.data.redis.serializer.StringRedisSerializer;

import com.leettracker.leettracker_api.dto.AnalyticsSummaryResponse;
import com.leettracker.leettracker_api.dto.PracticeTopicPlan;

import tools.jackson.databind.JavaType;
import tools.jackson.databind.type.TypeFactory;

@Configuration
public class RedisConfig {
    @Bean
    public RedisCacheManager cacheManager(
            RedisConnectionFactory connectionFactory
    ) {

        JacksonJsonRedisSerializer<AnalyticsSummaryResponse> analyticsSerializer =
        new JacksonJsonRedisSerializer<>(AnalyticsSummaryResponse.class);

        JavaType practicePlanType = TypeFactory.createDefaultInstance()
            .constructCollectionType(List.class, PracticeTopicPlan.class);

        JacksonJsonRedisSerializer<List<PracticeTopicPlan>> practicePlanSerializer =
                new JacksonJsonRedisSerializer<>(practicePlanType);

        RedisCacheConfiguration defaultConfig =
                RedisCacheConfiguration
                        .defaultCacheConfig()

                        .entryTtl(
                                Duration.ofMinutes(10)
                        )

                        .serializeKeysWith(
                                RedisSerializationContext
                                        .SerializationPair
                                        .fromSerializer(
                                                new StringRedisSerializer()
                                        )
                        )

                        .serializeValuesWith(
                                RedisSerializationContext
                                        .SerializationPair
                                        .fromSerializer(
                                                analyticsSerializer
                                        )
                        );

        RedisCacheConfiguration practicePlanConfig =
                RedisCacheConfiguration
                        .defaultCacheConfig()

                        .entryTtl(
                                Duration.ofMinutes(30)
                        )

                        .serializeKeysWith(
                                RedisSerializationContext
                                        .SerializationPair
                                        .fromSerializer(
                                                new StringRedisSerializer()
                                        )
                        )

                        .serializeValuesWith(
                                RedisSerializationContext
                                        .SerializationPair
                                        .fromSerializer(
                                                practicePlanSerializer
                                        )
                        );
        
        Map<String, RedisCacheConfiguration> cacheConfigurations =
            new HashMap<>();

                cacheConfigurations.put(
                        "practicePlan",
                        practicePlanConfig
                );

                cacheConfigurations.put(
                        "analytics",
                        defaultConfig
                );
        return RedisCacheManager
                .builder(connectionFactory)
                .cacheDefaults(defaultConfig)
                .withInitialCacheConfigurations(
                    cacheConfigurations
                )
                .build();
    }
}
