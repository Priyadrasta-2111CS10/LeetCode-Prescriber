package com.leettracker.leettracker_api.controller;

import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.leettracker.leettracker_api.dto.SyncResult;
import com.leettracker.leettracker_api.service.SyncService;

@RestController
@RequestMapping("/api/v1/users")
public class SyncController {

    private final SyncService syncService;

    public SyncController(SyncService syncService) {
        this.syncService = syncService;
    }

    @PostMapping("/{username}/sync")
    public SyncResult sync(
            @PathVariable String username
    ) {

        return syncService.syncUser(
                username
        );
    }
}
