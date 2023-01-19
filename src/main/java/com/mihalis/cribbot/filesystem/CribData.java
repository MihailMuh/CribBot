package com.mihalis.cribbot.filesystem;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.SneakyThrows;
import lombok.val;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.File;
import java.util.HashMap;
import java.util.List;

import static java.util.Objects.requireNonNull;

//structure of CribData:
//{
//  "term1":{
//      "matanalysis":{
//          "tickets":{
//              45:{
//                  "is_additional":False,
//                  "photos":[Path("45_1.jpg"),Path("45_2.jpg")],
//              },
//              46:{
//                  "is_additional":True,
//                  "photos":[Path("46_1.jpg"),Path("46_2.jpg")],
//              },
//          },
//          "ticket_numbers":"12 - сложение функций\n....."
//      }
//  },
//}

@Component
public class CribData {
    private static final HashMap<String, Term> terms = new HashMap<>();

    private static final HashMap<String, String> translate = new HashMap<>();

    @SneakyThrows
    @Autowired
    public CribData(File photoDir, File ticketNumbersDir) {
        for (File termDir : requireNonNull(photoDir.listFiles(File::isDirectory))) {
            Term term = new Term();

            for (File subjectDir : requireNonNull(termDir.listFiles())) {
                val questions = TicketUtils.readQuestions(ticketNumbersDir, termDir, subjectDir);

                term.addSubject(subjectDir.getName(), createSubject(questions, subjectDir));
            }

            terms.put(termDir.getName(), term);
        }

        parseTranslateFile(photoDir);
    }

    public Term term(String term) {
        return terms.get(term);
    }

    public String translate(String term) {
        return translate.get(term);
    }

    private Subject createSubject(List<String> questions, File subjectDir) {
        val questionsString = new StringBuilder();
        val subject = new Subject();
        int minNumber = TicketUtils.getMinNumber(questions);
        int maxNumber = minNumber + questions.size();

        for (int numberToFind = minNumber; numberToFind < maxNumber; numberToFind++) {
            Ticket ticket = createTicket(questions, numberToFind, subjectDir);
            subject.addTicket(numberToFind, ticket);

            if (ticket != null) {
                // append smile
                questionsString.append("\uD83E\uDEE1 ");
            }
            questionsString.append(questions.get(numberToFind - minNumber));
        }

        subject.setQuestions(questionsString.toString());
        return subject;
    }

    @SneakyThrows
    private void parseTranslateFile(File photoDir) {
        ObjectMapper objectMapper = new ObjectMapper();
        translate.putAll(objectMapper.readValue(TicketUtils.getTranslate(photoDir), HashMap.class));
    }

    private Ticket createTicket(List<String> questions, int numberToFind, File subjectDir) {
        for (String question : questions) {
            var ticketNumber = question.split(". ")[0];
            char star = ticketNumber.charAt(0);
            var number = ticketNumber.substring(star == '*' ? 1 : 0);

            if (ticketNumber.equals(String.valueOf(numberToFind))) {
                return new Ticket(star == '*',
                        subjectDir.listFiles(file -> file.getName().startsWith(number)));
            }
        }
        return null;
    }
}
