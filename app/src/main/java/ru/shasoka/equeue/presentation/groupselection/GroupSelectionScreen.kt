/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
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
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import ru.shasoka.equeue.data.remote.dto.GetGroupsResponseItem
import ru.shasoka.equeue.presentation.groupselection.components.SearchBar
import ru.shasoka.equeue.presentation.groupselection.components.SearchResult
import ru.shasoka.equeue.presentation.groupselection.components.SelectionBackground
import ru.shasoka.equeue.util.Constants.SEARCH_RESULT_HEIGHT

@Composable
fun GroupSelectionScreen(
	groups: List<GetGroupsResponseItem>,
	isLoading: Boolean,
	showAlert: Boolean,
	event: (GroupSelectionEvent) -> Unit,
	navController: NavController,
	modifier: Modifier = Modifier,
) {
	var searchQuery by remember { mutableStateOf("") }
	val contentAlpha by animateFloatAsState(
		targetValue = if (searchQuery.isEmpty()) 0.5f else 0f,
		label = "",
	)
	val globalAlpha by animateFloatAsState(
		targetValue = if (isLoading) 0.1f else 1f,
		label = "",
	)
	
	val keyboardController = LocalSoftwareKeyboardController.current
	
	val context = LocalContext.current
	val activity = context as? Activity
	
	if (showAlert) {
		AlertDialog(
			onDismissRequest = { event(GroupSelectionEvent.DisposeAlert) },
			confirmButton = {
				Button(
					onClick = { event(GroupSelectionEvent.DisposeAlert) },
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
			modifier = Modifier
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
				if (searchQuery.isNotEmpty()) {
					val filteredGroups =
						groups.filter {
							it.name.contains(searchQuery, ignoreCase = true)
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
							)
							.border(
								width = 1.dp,
								color = MaterialTheme.colorScheme.inverseOnSurface,
								shape = RoundedCornerShape(6.dp),
							),
					) {
						if (filteredGroups.isEmpty()) {
							item {
								SearchResult(text = "Ничего не найдено")
							}
						} else {
							items(filteredGroups) { group ->
								SearchResult(text = group.name)
							}
						}
					}
				}
			}
			SearchBar(
				placeholder = "КИ21-16 ...",
				onTextChange = { searchQuery = it },
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
		}
	}
}
