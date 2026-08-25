package com.leettracker.leettracker_api.service;

import org.springframework.stereotype.Service;

import com.leettracker.leettracker_api.model.User;
import com.leettracker.leettracker_api.repository.UserRepository;

@Service
public class UserService {

    private final UserRepository userRepository;

    public UserService(
            UserRepository userRepository
    ) {
        this.userRepository = userRepository;
    }

    public User getUser(
            String username
    ) {

        return userRepository
                .findByUsername(username)
                .orElseThrow(
                        () -> new RuntimeException(
                                "User not found: "
                                        + username
                        )
                );
    }
}