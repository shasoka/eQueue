/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.login

import android.util.Log
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.input.ImeAction
import kotlinx.coroutines.launch
import ru.shasoka.equeue.R
import ru.shasoka.equeue.presentation.Dimensions.SmallPadding
import ru.shasoka.equeue.presentation.common.HyperlinkText
import ru.shasoka.equeue.presentation.common.StartButton
import ru.shasoka.equeue.presentation.login.components.FormField
import ru.shasoka.equeue.util.Constants.RESET_PASS

@Composable
fun LoginScreen(
    event: (LoginEvent) -> Unit,
    modifier: Modifier = Modifier,
) {
    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }

    val focusManager = LocalFocusManager.current
    val usernameFocusRequester = remember { FocusRequester() }
    val passwordFocusRequester = remember { FocusRequester() }
    val coroutineScope = rememberCoroutineScope()

    var showAlert by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf("") }

    if (showAlert) {
        AlertDialog(
            onDismissRequest = { showAlert = false },
            confirmButton = {
                Button(onClick = { showAlert = false }) {
                    Text("Oк")
                }
            },
            text = { Text(errorMessage) },
        )
    }

    Box(
        modifier = modifier.fillMaxSize(),
        contentAlignment = Alignment.Center,
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
            modifier = Modifier
                .fillMaxWidth(0.7f)
                .fillMaxHeight(),
        ) {
            Image(
                painter = painterResource(id = R.drawable.logo),
                contentDescription = null,
                contentScale = ContentScale.Fit,
                modifier = Modifier
                    .fillMaxHeight(0.5f)
                    .padding(SmallPadding),
            )
            FormField(
                placeholder = "Введите логин ... ",
                icon = Icons.Default.Person,
                modifier =
                    Modifier
                        .padding(vertical = SmallPadding)
                        .focusRequester(usernameFocusRequester),
                onTextChange = { username = it },
                keyboardOptions =
                    KeyboardOptions.Default.copy(
                        imeAction = ImeAction.Next,
                    ),
                keyboardActions =
                    KeyboardActions(
                        onNext = {
                            coroutineScope.launch {
                                passwordFocusRequester.requestFocus()
                            }
                        },
                ),
            )
            FormField(
                placeholder = "Введите пароль ...",
                icon = Icons.Default.Lock,
                isSecret = true,
                modifier =
                    Modifier
                        .padding(vertical = SmallPadding)
                        .focusRequester(passwordFocusRequester),
                onTextChange = { password = it },
                keyboardOptions =
                    KeyboardOptions.Default.copy(
                        imeAction = ImeAction.Done,
                    ),
                keyboardActions =
                    KeyboardActions(
                        onDone = {
                            focusManager.clearFocus()
                    },
                ),
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
                    try {
                        event(LoginEvent.LoginUser(username, password))
                    } catch (e: Exception) {
                        errorMessage = e.message.toString()
                        showAlert = true
                        Log.d("HTTPException", errorMessage)
                    }
                },
                modifier = Modifier.padding(vertical = SmallPadding),
            )
        }
    }
}
