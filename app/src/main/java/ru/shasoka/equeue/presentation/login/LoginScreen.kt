/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.login

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.asPaddingValues
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.ime
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.navigation.NavController
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
	showAlert: Boolean,
	isLoading: Boolean,
	navController: NavController,
	modifier: Modifier = Modifier,
) {
	var username by remember { mutableStateOf("") }
	var password by remember { mutableStateOf("") }
	var prevUsername by remember { mutableStateOf("") }
	var prevPassword by remember { mutableStateOf("") }
	
	val focusManager = LocalFocusManager.current
	val usernameFocusRequester = remember { FocusRequester() }
	val passwordFocusRequester = remember { FocusRequester() }
	val coroutineScope = rememberCoroutineScope()
	
	val contentAlpha by animateFloatAsState(
		targetValue = if (isLoading) 0.1f else 1f,
		label = "",
	)
	
	if (showAlert) {
		AlertDialog(
			onDismissRequest = { event(LoginEvent.DisposeAlert) },
			confirmButton = {
				Button(
					onClick = { event(LoginEvent.DisposeAlert) },
				) {
					Text("Сэр, да, сэр! \uD83E\uDEE1")
				}
			},
			text = {
				Box {
					Text(
						"\uD83E\uDDD0 Неверный логин или пароль, попробуйте заново",
						style =
						MaterialTheme.typography.bodyMedium.copy(
							color = MaterialTheme.colorScheme.secondary,
							fontWeight = FontWeight.Bold,
						),
					)
				}
			},
			shape = MaterialTheme.shapes.medium,
		)
	}
	
	Box(
		modifier =
		modifier
			.fillMaxSize()
			.padding(WindowInsets.ime.asPaddingValues()),
		contentAlignment = Alignment.Center,
	) {
		AnimatedVisibility(
			visible = isLoading,
			enter = fadeIn(),
			exit = fadeOut(),
		) {
			CircularProgressIndicator()
		}
		
		Column(
			horizontalAlignment = Alignment.CenterHorizontally,
			verticalArrangement = Arrangement.Center,
			modifier =
			Modifier
				.fillMaxWidth(0.7f)
				.fillMaxHeight()
				.alpha(contentAlpha),
		) {
			Image(
				painter = painterResource(id = R.drawable.logo),
				contentDescription = null,
				contentScale = ContentScale.Fit,
				modifier =
				Modifier
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
				onTextChange = { newText ->
					if (newText != prevUsername) {
						if (newText.length - prevUsername.length > 1) {
							passwordFocusRequester.requestFocus()
						}
						prevUsername = newText
					}
					username = newText
				},
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
				onTextChange = { newText ->
					if (newText != prevPassword) {
						if (newText.length - prevPassword.length > 1) {
							focusManager.clearFocus()
						}
						prevPassword = newText
					}
					password = newText
				},
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
					coroutineScope.launch {
						event(LoginEvent.LoginUser(username, password, navController))
					}
				},
				modifier = Modifier.padding(vertical = SmallPadding),
			)
		}
	}
}
