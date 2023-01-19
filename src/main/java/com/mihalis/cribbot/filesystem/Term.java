package com.mihalis.cribbot.filesystem;

import java.util.HashMap;

public class Term {
    private static final HashMap<String, Subject> subjects = new HashMap<>();

    public Subject subject(String subject) {
        return subjects.get(subject);
    }

    void addSubject(String subjectName, Subject subject) {
        subjects.put(subjectName, subject);
    }
}
