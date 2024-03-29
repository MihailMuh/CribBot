package com.mihalis.cribbot.commands;

import com.mihalis.cribbot.telegram.Bot;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.extern.java.Log;
import org.telegram.telegrambots.extensions.bots.commandbot.commands.IBotCommand;
import org.telegram.telegrambots.meta.api.objects.Message;
import org.telegram.telegrambots.meta.bots.AbsSender;

@Getter
@Log
@AllArgsConstructor
public abstract class BaseCommand implements IBotCommand {
    private String commandIdentifier;

    private String description;

    public abstract void answer(Bot bot, Message message);

    @Override
    public void processMessage(AbsSender sender, Message message, String... arguments) {
        answer((Bot) sender, message);
        log.info("@" + message.getChat().getUserName() + ": /" + commandIdentifier + " - successfully");
    }
}
