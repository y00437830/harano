package com.harano;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.NoSuchElementException;

/** Centralized exception handling for all REST controllers. */
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(NoSuchElementException.class)
    public ResponseEntity<Void> handleNotFound(NoSuchElementException e) {
        return ResponseEntity.notFound().build();
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<Void> handleConflict(IllegalArgumentException e) {
        return ResponseEntity.status(HttpStatus.CONFLICT).build();
    }

    @ExceptionHandler(IllegalStateException.class)
    public ResponseEntity<Void> handleStateConflict(IllegalStateException e) {
        return ResponseEntity.status(HttpStatus.CONFLICT).build();
    }
}
