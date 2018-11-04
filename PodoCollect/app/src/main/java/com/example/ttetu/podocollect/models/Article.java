package com.example.ttetu.podocollect.models;

import java.io.Serializable;

public class Article implements Serializable {

    private int id;
    private String name;

    public Article(int id, String name) {
        this.id = id;
        this.name = name;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }
}
