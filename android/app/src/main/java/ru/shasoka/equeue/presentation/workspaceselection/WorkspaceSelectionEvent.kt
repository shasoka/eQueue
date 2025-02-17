package ru.shasoka.equeue.presentation.workspaceselection

import androidx.navigation.NavController
import ru.shasoka.equeue.util.Alerts

sealed class WorkspaceSelectionEvent {
    data class DisposeAlert(
        val alertType: Alerts,
    ) : WorkspaceSelectionEvent()

    data class ChangeGroup(
        val navController: NavController,
    ) : WorkspaceSelectionEvent()

    data object DisposeModal : WorkspaceSelectionEvent()

    data object InitModal : WorkspaceSelectionEvent()

    data object CreateWorkspace : WorkspaceSelectionEvent()
}
