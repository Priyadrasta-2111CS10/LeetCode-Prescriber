package com.leettracker.leettracker_api.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.leettracker.leettracker_api.model.User;
import com.leettracker.leettracker_api.service.UserService;

@RestController
@RequestMapping("/api/v1/users")
public class UserController {

    private final UserService userService;

    public UserController(
            UserService userService
    ) {
        this.userService = userService;
    }

    @GetMapping("/{username}")
    public User getUser(
            @PathVariable String username
    ) {

        return userService.getUser(
                username
        );
    }
}
