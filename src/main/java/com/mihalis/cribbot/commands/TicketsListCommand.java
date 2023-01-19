package com.mihalis.cribbot.commands;

import com.mihalis.cribbot.telegram.Bot;
import org.telegram.telegrambots.meta.api.objects.Message;

public class TicketsListCommand extends BaseCommand {
    public TicketsListCommand() {
        super("tickets", "Получить список вопросов");
    }

    @Override
    public void answer(Bot bot, Message message) {

    }
}
