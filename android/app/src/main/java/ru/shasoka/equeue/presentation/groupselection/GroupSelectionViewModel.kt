/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
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
import ru.shasoka.equeue.data.remote.dto.GroupRead
import ru.shasoka.equeue.data.remote.dto.ListOfGroupRead
import ru.shasoka.equeue.data.remote.dto.UserRead
import ru.shasoka.equeue.domain.usecases.api.groupselection.GroupSelectionUseCases
import ru.shasoka.equeue.domain.usecases.api.logout.LogoutUseCases
import ru.shasoka.equeue.presentation.nvgraph.Route
import ru.shasoka.equeue.util.Alerts
import ru.shasoka.equeue.util.ConnAlerts
import ru.shasoka.equeue.util.DataAlerts
import ru.shasoka.equeue.util.DbAlerts
import javax.inject.Inject

@HiltViewModel
class GroupSelectionViewModel
    @Inject
    constructor(
        private val groupSelectionUseCases: GroupSelectionUseCases,
        private val logoutUseCases: LogoutUseCases,
    ) : ViewModel() {
        var isLoading: Boolean by mutableStateOf(false)
            private set
	
        var showConnectionAlert: Boolean by mutableStateOf(false)
            private set

        var showGroupsLoadingAlert: Boolean by mutableStateOf(false)
            private set

        var showDbErrorAlert: Boolean by mutableStateOf(false)
            private set
	
        var groups by mutableStateOf<List<GroupRead>>(emptyList())
            private set

        init {
            viewModelScope.launch {
                try {
                    isLoading = true
                    delay(500)
                    groups = getGroups()
                    isLoading = false
                } catch (e: Exception) {
                    showGroupsLoadingAlert = true
                    isLoading = false
                }
            }
        }

        fun onEvent(event: GroupSelectionEvent) {
            when (event) {
                is GroupSelectionEvent.DisposeAlert -> {
                    when (val type = event.alertType) {
                        is Alerts.Connection -> {
                            if (type.alert == ConnAlerts.BASE_CONNECTION) {
                                showConnectionAlert = false
                            }
                        }
                        is Alerts.Data -> {
                            if (type.alert == DataAlerts.DATA_LOADING) {
                                showGroupsLoadingAlert = false
                            }
                        }
                        is Alerts.Db -> {
                            if (type.alert == DbAlerts.DB_ERROR) {
                                showDbErrorAlert = false
                            }
                        }
                    }
                }

                is GroupSelectionEvent.JoinGroup -> {
                    viewModelScope.launch {
                        try {
                            isLoading = true
                            delay(300)
                            joinGroup(event.group.id)
                            isLoading = false
                            event.navController.navigate(Route.WorkspaceSelectionNavigation.route)
                        } catch (e: Exception) {
                            showConnectionAlert = true
                            isLoading = false
                        }
                    }
                }

                is GroupSelectionEvent.ChangeAccount -> {
                    viewModelScope.launch {
                        try {
                            isLoading = true
                            delay(300)
                            logoutUser()
                            isLoading = false
                            event.navController.navigate(Route.LogInNavigation.route)
                        } catch (e: Exception) {
                            showGroupsLoadingAlert = true
                            isLoading = false
                        }
                    }
                }
            }
        }

        private suspend fun getGroups(): ListOfGroupRead = groupSelectionUseCases.getGroups()

        private suspend fun logoutUser() {
            try {
                return logoutUseCases.logoutUser()
            } catch (e: Exception) {
                throw e
            }
        }

        private suspend fun joinGroup(groupId: Int): UserRead {
            try {
                return groupSelectionUseCases.joinGroup(groupId)
            } catch (e: Exception) {
                throw e
            }
        }
    }
