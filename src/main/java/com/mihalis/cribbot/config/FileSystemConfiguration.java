package com.mihalis.cribbot.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.io.File;

@Configuration
public class FileSystemConfiguration {
    @Bean(name = "baseDir")
    public File getBaseDir() {
        return new File("");
    }

    @Bean(name = "photoDir")
    public File getPhotoDir(@Autowired File baseDir) {
        return new File(baseDir.getAbsolutePath() + "/photo");
    }

    @Bean(name = "ticketNumbersDir")
    public File getTicketNumbersDir(@Autowired File baseDir) {
        return new File(baseDir.getAbsolutePath() + "/ticket_numbers");
    }
}
