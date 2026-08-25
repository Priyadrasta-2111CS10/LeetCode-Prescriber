package com.leettracker.leettracker_api.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.leettracker.leettracker_api.dto.PracticeTopicPlan;
import com.leettracker.leettracker_api.service.PracticePlanService;

@RestController
@RequestMapping("/api/v1/users")
public class PracticePlanController {

    private final PracticePlanService practicePlanService;

    public PracticePlanController(
            PracticePlanService practicePlanService
    ) {
        this.practicePlanService =
                practicePlanService;
    }

    @GetMapping(
            "/{username}/practice-plan"
    )
    public List<PracticeTopicPlan> getPracticePlan(
            @PathVariable String username
    ) {

        return practicePlanService.generatePlan(
                username
        );
    }
}