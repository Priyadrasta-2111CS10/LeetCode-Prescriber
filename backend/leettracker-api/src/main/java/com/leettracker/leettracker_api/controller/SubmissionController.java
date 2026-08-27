package com.leettracker.leettracker_api.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.leettracker.leettracker_api.dto.RecentSubmissionResponse;
import com.leettracker.leettracker_api.service.SubmissionService;

@RestController
@RequestMapping("/api/v1/users")
public class SubmissionController {

    private final SubmissionService submissionService;

    public SubmissionController(
            SubmissionService submissionService
    ) {
        this.submissionService = submissionService;
    }

    @GetMapping("/{username}/submissions/recent")
    public List<RecentSubmissionResponse> getRecentSubmissions(
            @PathVariable String username,
            @RequestParam(defaultValue = "10") int limit
    ) {

        return submissionService.getRecentSubmissions(
                username,
                limit
        );
    }
}
