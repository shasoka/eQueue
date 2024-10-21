/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.onboarding

import androidx.annotation.DrawableRes
import ru.shasoka.equeue.R

data class Page(
    val title: String,
    val description: String,
    @DrawableRes val image: Int,
)

val pages =
    listOf(
        Page(
            title = "Добро пожаловать!",
            description =
                "eQueue поможет вам и вашей группе следить за предстоящими лабораторными," +
                    " информацией о предметах, очередями на сдачу и остальными важными событиями " +
                    "\uD83E\uDD13",
            image = R.drawable.onboarding_1,
        ),
        Page(
            title = "Приступим?",
            description =
                "Вы можете авторизоваться, используя учетные данные корпоративного " +
                    "сервиса «Мой СФУ». Не переживайте, никто ничего не украдет. " +
                    "Чувствуйте себя как дома, коллеги! \uD83E\uDD77\uD83C\uDFFB",
            image = R.drawable.onboarding_2,
        ),
    )
