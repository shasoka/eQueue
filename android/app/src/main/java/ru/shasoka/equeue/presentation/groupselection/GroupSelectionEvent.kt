/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.groupselection

import ru.shasoka.equeue.data.remote.dto.GetGroupsResponseItem

sealed class GroupSelectionEvent {
	data object DisposeAlert : GroupSelectionEvent()

	data class GroupSelected(
		val group: GetGroupsResponseItem
	) : GroupSelectionEvent()
}
