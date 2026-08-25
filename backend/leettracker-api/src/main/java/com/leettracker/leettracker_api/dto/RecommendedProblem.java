package com.leettracker.leettracker_api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public record RecommendedProblem(
        String title,

        @JsonProperty("title_slug")
        String titleSlug,

        String reason,
        String priority,

        @JsonProperty("suggested_order")
        Integer suggestedOrder) {
}