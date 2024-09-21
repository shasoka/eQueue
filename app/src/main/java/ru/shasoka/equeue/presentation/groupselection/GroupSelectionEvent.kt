/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.groupselection

sealed class GroupSelectionEvent {
	data object DisposeAlert : GroupSelectionEvent()
}
