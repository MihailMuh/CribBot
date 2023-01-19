package com.mihalis.cribbot.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.telegram.telegrambots.bots.DefaultBotOptions;

@Configuration
public class BotConfiguration {
    @Bean
    public DefaultBotOptions getBotConfiguration() {
        DefaultBotOptions options = new DefaultBotOptions();
        options.setMaxThreads(3);

        return options;
    }
}
