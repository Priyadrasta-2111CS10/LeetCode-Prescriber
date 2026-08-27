package com.leettracker.leettracker_api.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.leettracker.leettracker_api.dto.RecentSubmissionResponse;
import com.leettracker.leettracker_api.model.User;
import com.leettracker.leettracker_api.repository.SubmissionRepository;

@Service
public class SubmissionService {

    private final SubmissionRepository submissionRepository;
    private final UserService userService;

    public SubmissionService(
            SubmissionRepository submissionRepository,
            UserService userService
    ) {
        this.submissionRepository = submissionRepository;
        this.userService = userService;
    }

    public List<RecentSubmissionResponse> getRecentSubmissions(
            String username,
            int limit
    ) {

        User user = userService.getUser(username);

        return submissionRepository.getRecentSubmissions(
                user.getId(),
                limit
        );
    }
}
