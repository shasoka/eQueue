/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.workspaceselection.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
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
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import compose.icons.FeatherIcons
import compose.icons.feathericons.Hash
import compose.icons.feathericons.Info
import ru.shasoka.equeue.presentation.common.CancelButton
import ru.shasoka.equeue.presentation.common.FormField
import ru.shasoka.equeue.presentation.common.SubmitButon

@Composable
fun WorkspaceCreationDialog(
    onDismissRequest: () -> Unit,
    onConfirm: () -> Unit,
    onNameChange: (String) -> Unit,
    onAboutChange: (String) -> Unit,
) {
    var wsName by remember { mutableStateOf("") }
    var wsAbout by remember { mutableStateOf("") }
    var isNameInvalid by remember { mutableStateOf(false) }

    val focusManager = LocalFocusManager.current

    Dialog(onDismissRequest = onDismissRequest) {
        Box(contentAlignment = Alignment.Center) {
            Box(
                modifier = Modifier
                    .fillMaxWidth(0.8f)
                    .background(
                        color = MaterialTheme.colorScheme.surface,
                        shape = MaterialTheme.shapes.medium,
                    )
                    .padding(16.dp),
            ) {
                Column(
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                ) {
                    FormField(
                        placeholder = if (!isNameInvalid) "Как назовем?" else "Ну, пожалуйста...",
                        icon = FeatherIcons.Hash,
                        onTextChange = {
                            wsName = it
                            isNameInvalid = it.isBlank()
                            onNameChange(it)
                        },
                        keyboardOptions = KeyboardOptions.Default.copy(imeAction = ImeAction.Next),
                        keyboardActions = KeyboardActions(onNext = {
                            focusManager.moveFocus(
                                FocusDirection.Down
                            )
                        }),
                        modifier = Modifier.background(MaterialTheme.colorScheme.background)
                    )
                    FormField(
                        placeholder = "Описание",
                        icon = FeatherIcons.Info,
                        onTextChange = {
                            wsAbout = it
                            onAboutChange(it)
                        },
                        keyboardOptions = KeyboardOptions.Default.copy(imeAction = ImeAction.Done),
                        keyboardActions = KeyboardActions(onDone = { focusManager.clearFocus() }),
                    )
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                    ) {
                        CancelButton(
                            text = "Отмена",
                            onClick = onDismissRequest,
                        )
                        SubmitButon(
                            text = "Ехала! 🧨",
                            onClick = {
                                if (wsName.isBlank()) {
                                    isNameInvalid = true
                                } else {
                                    onConfirm()
                                }
                            },
                        )
                    }
                }
            }
        }
    }
}
