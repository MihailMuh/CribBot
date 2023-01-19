package com.mihalis.cribbot.filesystem;

import lombok.SneakyThrows;
import lombok.val;
import org.apache.commons.io.FileUtils;

import java.io.File;
import java.util.List;
import java.util.regex.Pattern;

import static java.nio.charset.Charset.defaultCharset;

class TicketUtils {
    @SneakyThrows
    public static List<String> readLines(File file) {
        return FileUtils.readLines(file, defaultCharset());
    }

    public static List<String> readQuestions(File basePath, File term, File subject) {
        return readLines(new File(basePath.getAbsolutePath() + "/" +
                term.getName() + "/" + subject.getName() + ".txt"));
    }

    public static int getMinNumber(List<String> questions) {
        val matcher = Pattern.compile("\\d+").matcher(String.join("", questions));
        matcher.find();
        return Integer.parseInt(matcher.group(0));
    }

    public static File getTranslate(File destDir) {
        return new File(destDir.getAbsolutePath() + "/translate.json");
    }
}
