/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.groupselection

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
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
        private var groups = mutableListOf<GetGroupsResponseItem>()

        init {
            viewModelScope.launch {
                groups = getGroups()
            }
        }

        private suspend fun getGroups(): GetGroupsResponse = groupSelectionUseCases.getGroups()
    }
