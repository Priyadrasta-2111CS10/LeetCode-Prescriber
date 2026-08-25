package com.leettracker.leettracker_api.service;

import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Caching;
import org.springframework.stereotype.Service;

import com.leettracker.leettracker_api.client.PythonSyncClient;
import com.leettracker.leettracker_api.dto.SyncResult;

import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import io.github.resilience4j.retry.annotation.Retry;

@Service
public class SyncService {

        private final PythonSyncClient pythonSyncClient;

        public SyncService(
                        PythonSyncClient pythonSyncClient) {
                this.pythonSyncClient = pythonSyncClient;
        }

        @Caching(
        evict = {
                @CacheEvict(
                        value = "analytics",
                        key = "#username"
                ),
                @CacheEvict(
                        value = "practicePlan",
                        key = "#username"
                )
                }
        )
        @CircuitBreaker(name = "pythonSync", fallbackMethod = "syncFallback")
        @Retry(name = "pythonsync")
        public SyncResult syncUser(
                        String username) {

                return pythonSyncClient.syncUser(
                                username);
        }
}
