/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.groupselection

import android.app.Activity
import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.asPaddingValues
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.ime
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import ru.shasoka.equeue.data.remote.dto.GroupRead
import ru.shasoka.equeue.presentation.common.HyperlinkNAV
import ru.shasoka.equeue.presentation.common.SearchBar
import ru.shasoka.equeue.presentation.common.SelectionBackground
import ru.shasoka.equeue.presentation.groupselection.components.SearchResult
import ru.shasoka.equeue.util.Alerts
import ru.shasoka.equeue.util.ConnAlerts
import ru.shasoka.equeue.util.Constants.SEARCH_RESULT_HEIGHT
import ru.shasoka.equeue.util.DataAlerts
import ru.shasoka.equeue.util.DbAlerts
import ru.shasoka.equeue.util.Dimensions.SmallPadding
import ru.shasoka.equeue.util.keyboardAsState

@Composable
fun GroupSelectionScreen(
    groups: List<GroupRead>,
    isLoading: Boolean,
    showGroupsLoadingAlert: Boolean,
    showConnectionAlert: Boolean,
    showDbErrorAlert: Boolean,
    event: (GroupSelectionEvent) -> Unit,
    navController: NavController,
    modifier: Modifier = Modifier,
) {
    // TODO move to viewModel
    var searchQuery by remember { mutableStateOf("") }
    var filteredGroups by remember { mutableStateOf<List<GroupRead>>(emptyList()) }
    var proceedDialog by remember { mutableStateOf(false) }
    var correctGroupSelected by remember { mutableStateOf(false) }

    val keyboardController = LocalSoftwareKeyboardController.current
    val keyboardOpen by keyboardAsState()
    val focusManager = LocalFocusManager.current

    val contentAlpha by animateFloatAsState(
        targetValue = if (searchQuery.isNotEmpty() && keyboardOpen) 0f else 0.5f,
        label = "",
    )
    val globalAlpha by animateFloatAsState(
        targetValue = if (isLoading) 0.1f else 1f,
        label = "",
    )

    val context = LocalContext.current
    val activity = context as? Activity

    if (showGroupsLoadingAlert) {
        AlertDialog(
            onDismissRequest = {
                event(
                    GroupSelectionEvent.DisposeAlert(
                        Alerts.Data(DataAlerts.DATA_LOADING),
                    ),
                )
            },
            confirmButton = {
                Button(
                    onClick = {
                        event(
                            GroupSelectionEvent.DisposeAlert(
                                Alerts.Data(DataAlerts.DATA_LOADING),
                            ),
                        )
                    },
                ) {
                    Text("Сэр, да, сэр! \uD83E\uDEE1")
                }
            },
            text = {
                Box {
                    Text(
                        "\uD83D\uDE16 Не смогли загрузить список групп",
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

    if (showConnectionAlert) {
        AlertDialog(
            onDismissRequest = {
                event(
                    GroupSelectionEvent.DisposeAlert(
                        Alerts.Connection(ConnAlerts.BASE_CONNECTION),
                    ),
                )
            },
            confirmButton = {
                Button(
                    onClick = {
                        event(
                            GroupSelectionEvent.DisposeAlert(
                                Alerts.Connection(ConnAlerts.BASE_CONNECTION),
                            ),
                        )
                    },
                ) {
                    Text("Печально... \uD83E\uDEE1")
                }
            },
            text = {
                Box {
                    Text(
                        "\uD83D\uDE14 Произошла так называемая \"ошибка\"",
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

    if (showDbErrorAlert) {
        AlertDialog(
            onDismissRequest = {
                event(
                    GroupSelectionEvent.DisposeAlert(
                        Alerts.Db(DbAlerts.DB_ERROR),
                    ),
                )
            },
            confirmButton = {
                Button(
                    onClick = {
                        event(
                            GroupSelectionEvent.DisposeAlert(
                                Alerts.Db(DbAlerts.DB_ERROR),
                            ),
                        )
                    },
                ) {
                    Text("Жаль!.. \uD83E\uDEE1")
                }
            },
            text = {
                Box {
                    Text(
                        "\uD83D\uDE25 Не смог тебя разлогинить",
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

    if (proceedDialog) {
        AlertDialog(
            onDismissRequest = { proceedDialog = false },
            confirmButton = {
                if (correctGroupSelected) {
                    Button(
                        onClick = {
                            proceedDialog = false
                            event(
                                GroupSelectionEvent.JoinGroup(
                                    groups.first { it.name == searchQuery },
                                    navController,
                                ),
                            )
                        },
                    ) {
                        Text("Так точно \uD83E\uDEE1")
                    }
                } else {
                    Button(
                        onClick = {
                            proceedDialog = false
                        },
                    ) {
                        Text("Сэр, да, сэр! \uD83E\uDEE1")
                    }
                }
            },
            dismissButton = {
                if (correctGroupSelected) {
                    Button(
                        onClick = { proceedDialog = false },
                    ) {
                        Text("Отмена")
                    }
                }
            },
            title = {
                if (correctGroupSelected) {
                    Text("Подтверждение")
                } else {
                    Text("Группа не найдена")
                }
            },
            text = {
                if (correctGroupSelected) {
                    Text("Вы уверены, что хотите присоединиться к группе $searchQuery?")
                } else {
                    Text("Вы ввели некорректную группу. Попробуйте ещё раз.")
                }
            },
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
		
        BackHandler {
            activity?.finish()
        }

        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
            modifier =
                Modifier
                    .fillMaxWidth(0.7f)
                    .fillMaxHeight()
                    .alpha(globalAlpha),
        ) {
            Box(
                contentAlignment = Alignment.BottomCenter,
                modifier = Modifier.fillMaxWidth(),
            ) {
                SelectionBackground(
                    contentAlpha = contentAlpha,
                    text = "Коллега спрашивает коллегу: «Какова твоя группа, коллега?»\n\uD83E\uDD28",
                )

                this@Column.AnimatedVisibility(
                    visible = searchQuery.isNotEmpty() && keyboardOpen,
                ) {
                    filteredGroups =
                        groups.filter {
                            it.name.contains(
                                searchQuery,
                                ignoreCase = true,
                            )
                        }
                    val visibleItems = filteredGroups.take(5)
                    val lazyColumnHeight = (visibleItems.size * SEARCH_RESULT_HEIGHT).dp

                    LazyColumn(
                        horizontalAlignment = Alignment.Start,
                        verticalArrangement = Arrangement.Bottom,
                        modifier =
                            Modifier
                                .fillMaxWidth()
                                .height(lazyColumnHeight)
                                .background(
                                    color = MaterialTheme.colorScheme.inverseOnSurface,
                                    shape = RoundedCornerShape(6.dp),
                                ).border(
                                    width = 1.dp,
                                    color = MaterialTheme.colorScheme.inverseOnSurface,
                                    shape = RoundedCornerShape(6.dp),
                                ),
                    ) {
                        if (filteredGroups.isEmpty()) {
                            item {
                                SearchResult(
                                    text = "Ничего не найдено",
                                    onClick = {},
                                )
                            }
                        } else {
                            items(filteredGroups) { group ->
                                SearchResult(
                                    text = group.name,
                                    onClick = {
                                        keyboardController?.hide()
                                        focusManager.clearFocus()
                                        searchQuery = group.name
                                    },
                                )
                            }
                        }
                    }
                }
            }

            SearchBar(
                placeholder = "КИ21-16 ...",
                onTextChange = {
                    searchQuery = it
                },
                onClick = {
                    if (searchQuery in groups.map { it.name }) {
                        correctGroupSelected = true
                        proceedDialog = true
                    } else {
                        correctGroupSelected = false
                        proceedDialog = true
                    }
                },
                textState = searchQuery,
                keyboardOptions =
                    KeyboardOptions.Default.copy(
                        imeAction = ImeAction.Done,
                    ),
                keyboardActions =
                    KeyboardActions(
                        onDone = {
                            keyboardController?.hide()
                        },
                    ),
            )

            HyperlinkNAV(
                text = "Сменить аккаунт \uD83D\uDEAA",
                modifier = Modifier.padding(vertical = SmallPadding),
                onClick = { event(GroupSelectionEvent.ChangeAccount(navController)) },
            )
        }
    }
}
