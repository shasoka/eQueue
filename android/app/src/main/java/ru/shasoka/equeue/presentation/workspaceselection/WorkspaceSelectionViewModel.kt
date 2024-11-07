package ru.shasoka.equeue.presentation.workspaceselection

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import ru.shasoka.equeue.data.remote.dto.ListOfWorkspaceRead
import ru.shasoka.equeue.data.remote.dto.WorkspaceRead
import ru.shasoka.equeue.domain.usecases.api.logout.LogoutUseCases
import ru.shasoka.equeue.domain.usecases.api.workspaceselection.WorkspaceSelectionUseCases
import ru.shasoka.equeue.presentation.nvgraph.Route
import ru.shasoka.equeue.util.Alerts
import ru.shasoka.equeue.util.ConnAlerts
import ru.shasoka.equeue.util.DataAlerts
import ru.shasoka.equeue.util.DbAlerts
import javax.inject.Inject

@HiltViewModel
class WorkspaceSelectionViewModel
    @Inject
    constructor(
        private val workspaceSelectionUseCases: WorkspaceSelectionUseCases,
        private val logoutUseCases: LogoutUseCases,
    ) : ViewModel() {
        var isLoading: Boolean by mutableStateOf(false)
            private set

        var showConnectionAlert: Boolean by mutableStateOf(false)
            private set

        var showWorkspacesLoadingAlert: Boolean by mutableStateOf(false)
            private set

        var showDbErrorAlert: Boolean by mutableStateOf(false)
            private set

        var workspaces by mutableStateOf<List<WorkspaceRead>>(emptyList())
            private set

        init {
            viewModelScope.launch {
                try {
                    isLoading = true
                    delay(500)
                    workspaces = getExistingWorkspaces()
                    isLoading = false
                } catch (e: Exception) {
                    showWorkspacesLoadingAlert = true
                    isLoading = false
                }
            }
        }

        fun onEvent(event: WorkspaceSelectionEvent) {
            when (event) {
                is WorkspaceSelectionEvent.DisposeAlert -> {
                    when (val type = event.alertType) {
                        is Alerts.Connection -> {
                            if (type.alert == ConnAlerts.BASE_CONNECTION) {
                                showConnectionAlert = false
                            }
                        }
                        is Alerts.Data -> {
                            if (type.alert == DataAlerts.DATA_LOADING) {
                                showWorkspacesLoadingAlert = false
                            }
                        }
                        is Alerts.Db -> {
                            if (type.alert == DbAlerts.DB_ERROR) {
                                showDbErrorAlert = false
                            }
                        }
                    }
                }

                is WorkspaceSelectionEvent.ChangeAccount -> {
                    viewModelScope.launch {
                        try {
                            isLoading = true
                            delay(300)
                            logoutUser()
                            isLoading = false
                            event.navController.navigate(Route.LogInNavigation.route)
                        } catch (e: Exception) {
                            showDbErrorAlert = true
                            isLoading = false
                        }
                    }
                }
            }
        }

        private suspend fun getExistingWorkspaces(): ListOfWorkspaceRead = workspaceSelectionUseCases.getExistingWorkspaces()

        private suspend fun logoutUser() {
            try {
                return logoutUseCases.logoutUser()
            } catch (e: Exception) {
                throw e
            }
        }
    }
