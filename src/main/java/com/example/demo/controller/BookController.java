package com.example.demo.controller;

import org.springframework.web.bind.annotation.*;
import java.util.*;
import com.example.demo.model.Book;
import org.springframework.web.bind.annotation.GetMapping;


@RestController
@RequestMapping("/api/books")
public class BookController {
     private List<Book> books = new ArrayList<>();
     private Long nextId = 1L;

     @GetMapping
     public List<Book> getAllBooks(){
        return books;
     }
    
    @GetMapping("/{id}")
    public Book getBookById(@PathVariable Long id) {
        return books.stream()
                .filter(book -> book.getId().equals(id))
            .findFirst()
            .orElse(null);
    }

    @PostMapping
    public Book addBook(@RequestBody Book book) {
        book.setId(nextId++);
        books.add(book);
        return book;
    }

    @DeleteMapping("/{id}")
    public String deleteBook(@PathVariable Long id) {
        boolean removed = books.removeIf(book -> book.getId().equals(id));
        if (removed) {
            return "Book with ID " + id + " deleted successfully";
        } else {
            return "Book with ID " + id + " not found";
        }
    }

     
     
}


