package com.mihalis.cribbot.commands;

import com.mihalis.cribbot.telegram.Bot;
import com.mihalis.cribbot.telegram.PostMessage;
import lombok.SneakyThrows;
import lombok.extern.java.Log;
import org.springframework.stereotype.Component;
import org.telegram.telegrambots.meta.api.objects.Message;

@Log
@Component
public class StartCommand extends BaseCommand {
    private static final String greeting = """
            Привет!
            Это бот, который отправляет решения на билеты (если они есть :)) по конкретному экзамену

            Список доступных команд:
            /start - запустить это приветственное сообщение
            /term - задать семестр экзамена
            /subject - задать предмет для экзамена
            /tickets - получить список вопросов
            /upload - загрузить решения на вопрос экзамена
            /support - поддержать автора :)

            Для получения решения нужно писать только НОМЕР вопроса
            """;

    public StartCommand() {
        super("start", "Запустить приветственный диалог");
    }

    @Override
    @SneakyThrows
    public void answer(Bot bot, Message message) {
        PostMessage sendMessage = new PostMessage(message);
        sendMessage.setText(greeting);

        bot.executeAsync(sendMessage);
    }
}
