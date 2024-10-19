/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.groupselection

import androidx.navigation.NavController
import ru.shasoka.equeue.data.remote.dto.GetGroupsResponseItem
import ru.shasoka.equeue.util.Alerts

sealed class GroupSelectionEvent {
	data class DisposeAlert(
		val alertType: Alerts
	) : GroupSelectionEvent()

	data class JoinGroup(
		val group: GetGroupsResponseItem
	) : GroupSelectionEvent()

	data class ChangeAccount(
		val navController: NavController
	) : GroupSelectionEvent()
}
