/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.groupselection

import androidx.navigation.NavController
import ru.shasoka.equeue.data.remote.dto.GetGroupsResponseItem

sealed class GroupSelectionEvent {
	data object DisposeAlert : GroupSelectionEvent()

	data object DisposeError : GroupSelectionEvent()

	data class GroupSelected(
		val group: GetGroupsResponseItem
	) : GroupSelectionEvent()

	data class ChangeAccount(
		val navController: NavController
	) : GroupSelectionEvent()
}
