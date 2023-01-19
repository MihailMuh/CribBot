package com.mihalis.cribbot;

import com.mihalis.cribbot.telegram.Bot;
import jakarta.annotation.PostConstruct;
import lombok.AccessLevel;
import lombok.Setter;
import lombok.SneakyThrows;
import lombok.extern.java.Log;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.telegram.telegrambots.meta.TelegramBotsApi;
import org.telegram.telegrambots.updatesreceivers.DefaultBotSession;

@Log
@SpringBootApplication
public class CribBotApplication {
    @Setter(value = AccessLevel.PRIVATE, onMethod_ = {@Autowired})
    private Bot bot;

    public static void main(String[] args) {
        SpringApplication.run(CribBotApplication.class, args);
    }

    @SneakyThrows
    @PostConstruct
    private void registerTelegramBot() {
        TelegramBotsApi telegramBotsApi = new TelegramBotsApi(DefaultBotSession.class);
        telegramBotsApi.registerBot(bot);

        log.info("Telegram bot successfully registered!");
    }
}
