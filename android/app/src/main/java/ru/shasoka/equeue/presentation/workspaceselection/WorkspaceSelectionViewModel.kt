package ru.shasoka.equeue.presentation.workspaceselection

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import ru.shasoka.equeue.data.remote.GroupLeaveException
import ru.shasoka.equeue.data.remote.dto.ListOfWorkspaceRead
import ru.shasoka.equeue.data.remote.dto.UserRead
import ru.shasoka.equeue.data.remote.dto.WorkspaceRead
import ru.shasoka.equeue.domain.usecases.api.groups.GroupsUseCases
import ru.shasoka.equeue.domain.usecases.api.workspaces.WorkspacesUseCases
import ru.shasoka.equeue.presentation.nvgraph.Route
import ru.shasoka.equeue.util.Alerts
import ru.shasoka.equeue.util.ConnAlerts
import ru.shasoka.equeue.util.DataAlerts
import ru.shasoka.equeue.util.DbAlerts

@HiltViewModel
class WorkspaceSelectionViewModel
@Inject
constructor(
    private val workspacesUseCases: WorkspacesUseCases,
    private val groupsUseCases: GroupsUseCases
) : ViewModel() {
    var isLoading: Boolean by mutableStateOf(false)
        private set

    var showConnectionAlert: Boolean by mutableStateOf(false)
        private set

    var showWorkspacesLoadingAlert: Boolean by mutableStateOf(false)
        private set

    var showGroupLeaveAlert: Boolean by mutableStateOf(false)
        private set

    var showDbErrorAlert: Boolean by mutableStateOf(false)
        private set

    var showWorkspaceCreationModal: Boolean by mutableStateOf(false)
        private set

    var workspaces by mutableStateOf<List<WorkspaceRead>>(emptyList())
        private set

    private var newWsName by mutableStateOf("")

    private var newWsAbout by mutableStateOf("")

    fun setWsName(name: String) {
        newWsName = name
    }

    fun setWsAbout(about: String) {
        newWsAbout = about
    }

    init {
        viewModelScope.launch {
            try {
                isLoading = true
                delay(500)
                workspaces = getExistingWorkspaces()
                if (workspaces.isEmpty()) showWorkspaceCreationModal = true
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
                        } else if (type.alert == DataAlerts.DATA_CONFLICT) {
                            showGroupLeaveAlert = false
                        }
                    }

                    is Alerts.Db -> {
                        if (type.alert == DbAlerts.DB_ERROR) {
                            showDbErrorAlert = false
                        }
                    }
                }
            }

            is WorkspaceSelectionEvent.ChangeGroup -> {
                viewModelScope.launch {
                    try {
                        isLoading = true
                        delay(300)
                        leaveGroup()
                        isLoading = false
                        event.navController.navigate(Route.GroupSelectionNavigation.route)
                    } catch (e: GroupLeaveException) {
                        showGroupLeaveAlert = true
                        isLoading = false
                    } catch (e: Exception) {
                        showDbErrorAlert = true
                        isLoading = false
                    }
                }
            }

            is WorkspaceSelectionEvent.DisposeModal -> showWorkspaceCreationModal = false

            is WorkspaceSelectionEvent.InitModal -> showWorkspaceCreationModal = true

            is WorkspaceSelectionEvent.CreateWorkspace -> {
                viewModelScope.launch {
                    try {
                        isLoading = true
                        delay(300)
                        createWorkspace()
                        isLoading = false
                        // TODO: nav next
                    } catch (e: Exception) {
                        // TODO custom error
                        showConnectionAlert = true
                        isLoading = false
                    }
                }
            }
        }
    }

    private suspend fun getExistingWorkspaces(): ListOfWorkspaceRead =
        workspacesUseCases.getExistingWorkspaces()

    private suspend fun leaveGroup(): UserRead {
        try {
            return groupsUseCases.leaveGroup()
        } catch (e: Exception) {
            throw e
        }
    }

    private suspend fun createWorkspace(): WorkspaceRead {
        try {
            return workspacesUseCases.createNewWorkspace(
                name = newWsName,
                about = newWsAbout
            )
        } catch (e: Exception) {
            throw e
        }
    }
}
