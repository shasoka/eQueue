/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.workspaceselection.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusDirection
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import ru.shasoka.equeue.presentation.common.FormField

@Composable
fun WorkspaceCreationDialog(
    onDismissRequest: () -> Unit,
    modifier: Modifier = Modifier,
) {
    var wsName by remember { mutableStateOf("") }
    var wsSemester by remember { mutableStateOf("") }
    var wsAbout by remember { mutableStateOf("") }
    val focusManager = LocalFocusManager.current

    Dialog(onDismissRequest = onDismissRequest) {
        Box(
            modifier =
                Modifier
                    .fillMaxSize()
                    .background(color = Color.Black.copy(alpha = 0.5f))
                    .clickable { focusManager.clearFocus() },
            contentAlignment = Alignment.Center,
        ) {
            Box(
                modifier =
                    Modifier
                        .fillMaxWidth(0.8f)
                        .background(
                            color = MaterialTheme.colorScheme.surface,
                            shape = MaterialTheme.shapes.medium,
                        ).padding(16.dp), // Внутренние отступы
            ) {
                Column(
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                ) {
                    FormField(
                        placeholder = "Невероятное название ...",
                        icon = null,
                        onTextChange = { wsName = it },
                        keyboardOptions =
                            KeyboardOptions.Default.copy(imeAction = ImeAction.Next),
                        keyboardActions =
                            KeyboardActions(
                                onNext = { focusManager.moveFocus(FocusDirection.Down) },
                            ),
                    )
                    FormField(
                        placeholder = "Текущий семестр ...",
                        icon = null,
                        onTextChange = { wsSemester = it },
                        keyboardOptions =
                            KeyboardOptions.Default.copy(imeAction = ImeAction.Next),
                        keyboardActions =
                            KeyboardActions(
                                onNext = { focusManager.moveFocus(FocusDirection.Down) },
                            ),
                    )
                    FormField(
                        placeholder = "Краткое описание ...",
                        icon = null,
                        onTextChange = { wsAbout = it },
                        keyboardOptions =
                            KeyboardOptions.Default.copy(imeAction = ImeAction.Done),
                        keyboardActions =
                            KeyboardActions(
                                onDone = { focusManager.clearFocus() },
                            ),
                    )
                }
            }
        }
    }
}
