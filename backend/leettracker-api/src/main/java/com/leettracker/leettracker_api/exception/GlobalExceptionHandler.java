package com.leettracker.leettracker_api.exception;

import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {
     @ExceptionHandler(
            PythonServiceException.class
    )
    public ResponseEntity<?> handlePythonServiceError(
            PythonServiceException exception
    ) {

        return ResponseEntity
                .status(
                        HttpStatus.SERVICE_UNAVAILABLE
                )
                .body(
                        Map.of(
                                "error",
                                "PYTHON_SERVICE_UNAVAILABLE",
                                "message",
                                exception.getMessage()
                        )
                );
    }

}
