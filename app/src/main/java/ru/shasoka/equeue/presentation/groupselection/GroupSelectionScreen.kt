/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.groupselection

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.asPaddingValues
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.ime
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
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
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import ru.shasoka.equeue.R
import ru.shasoka.equeue.presentation.Dimensions.MediumPadding
import ru.shasoka.equeue.presentation.Dimensions.SmallPadding
import ru.shasoka.equeue.presentation.groupselection.components.SearchBar

@Composable
fun GroupSelectionScreen(modifier: Modifier = Modifier) {
    var searchQuery by remember { mutableStateOf("") }
    val groups = listOf("Group A", "Group B", "Group C", "Group D") // Пример списка групп
	
    val contentAlpha by animateFloatAsState(
        targetValue = if (searchQuery.isEmpty()) 0.5f else 0f,
        label = "",
    )
	
    Box(
        modifier =
            modifier
                .fillMaxSize()
                .padding(WindowInsets.ime.asPaddingValues()),
        contentAlignment = Alignment.Center,
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
            modifier = Modifier.fillMaxWidth(0.7f).fillMaxHeight(),
        ) {
            Image(
                painter = painterResource(id = R.drawable.sfu_u),
                contentDescription = null,
                contentScale = ContentScale.Fit,
                modifier =
                    Modifier
                        .alpha(0.25f)
                        .padding(SmallPadding),
            )
            Box(
                modifier =
                    Modifier
                        .fillMaxWidth()
                        .padding(all = MediumPadding),
                contentAlignment = Alignment.Center,
            ) {
                Text(
                    text = "Коллега спрашивает коллегу: «Какова твоя группа, коллега?»\n\uD83E\uDD28",
                    style =
                        MaterialTheme.typography.bodyLarge.copy(
                            color = MaterialTheme.colorScheme.onBackground.copy(alpha = contentAlpha),
                        ),
                    textAlign = TextAlign.Center,
                )
            }
            SearchBar(
                placeholder = "Поиск...",
                onTextChange = { searchQuery = it },
                keyboardOptions =
                    KeyboardOptions.Default.copy(
                        imeAction = ImeAction.Done,
                    ),
                keyboardActions =
                    KeyboardActions(
                        onDone = {
                            // Действие при завершении ввода
                        },
                    ),
                modifier =
                    Modifier
                        .padding(16.dp)
                        .fillMaxWidth(),
            )
            Spacer(modifier = Modifier.height(16.dp))
            if (searchQuery.isNotEmpty()) {
                val filteredGroups = groups.filter { it.contains(searchQuery, ignoreCase = true) }
                Column(
                    horizontalAlignment = Alignment.Start,
                    verticalArrangement = Arrangement.Top,
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
                ) {
                    filteredGroups.forEach { group ->
                        Text(
                            text = group,
                            style =
                                MaterialTheme.typography.bodyMedium.copy(
                                    color = MaterialTheme.colorScheme.onBackground,
                                ),
                            modifier = Modifier.padding(vertical = 4.dp),
                        )
                    }
                }
            }
        }
    }
}
