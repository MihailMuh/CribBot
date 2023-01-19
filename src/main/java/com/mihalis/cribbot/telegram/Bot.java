package com.mihalis.cribbot.telegram;

import com.mihalis.cribbot.filesystem.CribData;
import com.mihalis.cribbot.commands.StartCommand;
import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.telegram.telegrambots.bots.DefaultBotOptions;
import org.telegram.telegrambots.extensions.bots.commandbot.TelegramLongPollingCommandBot;
import org.telegram.telegrambots.meta.api.objects.Update;

@Getter
@Component
public class Bot extends TelegramLongPollingCommandBot {
    @Value("${spring.telegram.bot.username}")
    private String botUsername;

    @Value("${spring.telegram.bot.token}")
    private String botToken;

    public Bot(DefaultBotOptions defaultBotOptions, StartCommand startCommand, CribData cribData) {
        super(defaultBotOptions);

        registerAll(startCommand);
    }

    @Override
    public void processNonCommandUpdate(Update update) {

    }
}
