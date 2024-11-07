package ru.shasoka.equeue.presentation.workspaceselection

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.NavController
import ru.shasoka.equeue.data.remote.dto.WorkspaceRead

@Composable
fun WorkspaceSelectionScreen(
    workspaces: List<WorkspaceRead>,
    isLoading: Boolean,
    showWorkspacesLoadingAlert: Boolean,
    showConnectionAlert: Boolean,
    showDbErrorAlert: Boolean,
    event: (WorkspaceSelectionEvent) -> Unit,
    navController: NavController,
    modifier: Modifier = Modifier,
) {
    workspaces
    workspaces
}
