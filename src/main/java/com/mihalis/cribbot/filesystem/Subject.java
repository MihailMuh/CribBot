package com.mihalis.cribbot.filesystem;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.util.HashMap;
import java.util.Set;

@ToString
class Subject {
    private static final HashMap<Integer, Ticket> tickets = new HashMap<>();

    @Setter(value = AccessLevel.PACKAGE)
    @Getter
    private String questions = "";

    public Ticket ticket(int number) {
        return tickets.get(number);
    }

    public Set<Integer> ticketNumbers() {
        return tickets.keySet();
    }

    void addTicket(int ticketNumbers, Ticket ticket) {
        if (ticket != null) {
            tickets.put(ticketNumbers, ticket);
        }
    }
}
