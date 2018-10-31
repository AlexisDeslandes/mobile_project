package com.example.ttetu.podocollect.models;

public class ArticleCouple {

    private String start;
    private String end;
    private int steps;

    public ArticleCouple(String start, String end, int steps) {
        this.start = start;
        this.end = end;
        this.steps = steps;
    }

    public String getStart() {
        return start;
    }

    public String getEnd() {
        return end;
    }

    public int getSteps() {
        return steps;
    }
}
