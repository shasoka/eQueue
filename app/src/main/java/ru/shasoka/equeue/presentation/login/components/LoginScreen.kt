/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.login.components

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Person
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.tooling.preview.Preview
import ru.shasoka.equeue.R
import ru.shasoka.equeue.presentation.Dimensions.SmallPadding
import ru.shasoka.equeue.presentation.common.HyperlinkText
import ru.shasoka.equeue.presentation.common.StartButton
import ru.shasoka.equeue.ui.theme.EQueueTheme
import ru.shasoka.equeue.util.Constants.RESET_PASS

@Composable
fun LoginScreen(modifier: Modifier = Modifier) {
    Box(
        modifier = modifier.fillMaxSize(),
        contentAlignment = Alignment.Center,
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
            modifier = Modifier.fillMaxWidth(0.7f).fillMaxHeight(),
        ) {
            Image(
                painter = painterResource(id = R.drawable.logo),
                contentDescription = null,
                contentScale = ContentScale.Fit,
                modifier = Modifier.fillMaxHeight(0.5f).padding(SmallPadding),
            )
            FormField(
                placeholder = "Введите логин ... ",
                icon = Icons.Default.Person,
                modifier = Modifier.padding(vertical = SmallPadding),
            )
            FormField(
                placeholder = "Введите пароль ...",
                icon = Icons.Default.Lock,
                isSecret = true,
                modifier = Modifier.padding(vertical = SmallPadding),
            )
            HyperlinkText(
                fullText = "Забыли пароль? Вам сюда \uD83E\uDEA4",
                linkText = listOf("Вам сюда \uD83E\uDEA4"),
                hyperlinks = listOf(RESET_PASS),
                modifier = Modifier.padding(vertical = SmallPadding),
            )
            StartButton(
                text = "Войти",
                onClick = {
                    TODO()
                },
                modifier = Modifier.padding(vertical = SmallPadding),
            )
        }
    }
}

@Preview(showBackground = true)
@Composable
private fun LoginScreenPreview() {
    EQueueTheme(dynamicColor = false) {
        LoginScreen()
    }
}
