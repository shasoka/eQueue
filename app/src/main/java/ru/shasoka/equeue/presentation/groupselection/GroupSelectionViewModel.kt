/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.groupselection

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import ru.shasoka.equeue.data.remote.dto.GetGroupsResponse
import ru.shasoka.equeue.data.remote.dto.GetGroupsResponseItem
import ru.shasoka.equeue.domain.usecases.api.groupselection.GroupSelectionUseCases
import javax.inject.Inject

@HiltViewModel
class GroupSelectionViewModel
@Inject
constructor(
	private val groupSelectionUseCases: GroupSelectionUseCases,
) : ViewModel() {
	var isLoading: Boolean by mutableStateOf(false)
		private set
	
	var showAlert: Boolean by mutableStateOf(false)
		private set
	
	var groups by mutableStateOf<List<GetGroupsResponseItem>>(emptyList())
		private set
	
	init {
		viewModelScope.launch {
			try {
				isLoading = true
				delay(500)
				groups = getGroups()
				isLoading = false
			} catch (e: Exception) {
				showAlert = true
				isLoading = false
			}
		}
	}
	
	fun onEvent(event: GroupSelectionEvent) {
		when (event) {
			is GroupSelectionEvent.DisposeAlert -> {
				showAlert = false
			}
		}
	}
	
	private suspend fun getGroups(): GetGroupsResponse = groupSelectionUseCases.getGroups()
}
