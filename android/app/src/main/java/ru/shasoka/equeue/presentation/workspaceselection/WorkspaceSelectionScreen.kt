package ru.shasoka.equeue.presentation.workspaceselection

import android.app.Activity
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.asPaddingValues
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.ime
import androidx.compose.foundation.layout.padding
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.navigation.NavController
import ru.shasoka.equeue.data.remote.dto.GroupRead
import ru.shasoka.equeue.data.remote.dto.WorkspaceRead
import ru.shasoka.equeue.presentation.common.SelectionBackground
import ru.shasoka.equeue.presentation.common.SubmitButon
import ru.shasoka.equeue.presentation.workspaceselection.components.WorkspaceCreationDialog
import ru.shasoka.equeue.util.keyboardAsState

@Composable
fun WorkspaceSelectionScreen(
    workspaces: List<WorkspaceRead>,
    isLoading: Boolean,
    showWorkspacesLoadingAlert: Boolean,
    showConnectionAlert: Boolean,
    showDbErrorAlert: Boolean,
    showWorkspaceCreationModal: Boolean,
    event: (WorkspaceSelectionEvent) -> Unit,
    navController: NavController,
    modifier: Modifier = Modifier,
) {
    // TODO move to viewModel
    var searchQuery by remember { mutableStateOf("") }
    var filteredGroups by remember { mutableStateOf<List<GroupRead>>(emptyList()) }
    var proceedDialog by remember { mutableStateOf(false) }
    var correctGroupSelected by remember { mutableStateOf(false) }

    val keyboardController = LocalSoftwareKeyboardController.current
    val keyboardOpen by keyboardAsState()
    val focusManager = LocalFocusManager.current

    val contentAlpha by animateFloatAsState(
        targetValue = if (searchQuery.isNotEmpty() && keyboardOpen) 0f else 0.5f,
        label = "",
    )
    val globalAlpha by animateFloatAsState(
        targetValue = if (isLoading || showWorkspaceCreationModal) 0.1f else 1f,
        label = "",
    )

    val context = LocalContext.current
    val activity = context as? Activity



    Box(
        modifier =
        modifier
            .fillMaxSize()
            .padding(WindowInsets.ime.asPaddingValues()),
        contentAlignment = Alignment.Center,
    ) {
        if (showWorkspaceCreationModal) {
            WorkspaceCreationDialog(onDismissRequest = {}, onConfirm = {})
        }

        if (workspaces.isEmpty()) {  // Если не найдено ни одного рабочего пространства
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center,
                modifier =
                Modifier
                    .fillMaxWidth()
                    .fillMaxHeight()
                    .alpha(globalAlpha),
            ) {
                SelectionBackground(
                    contentAlpha = contentAlpha,
                    text =
                    "Похоже никто еще не создал рабочее пространство для вашей группы." +
                            "\nВы можете стать первым!\n\uD83D\uDC51",
                    modifier = Modifier.fillMaxWidth(0.7f),
                )

                SubmitButon(
                    text = "Настало моё время...",
                    onClick = { event(WorkspaceSelectionEvent.InitModal) },
                )
            }
        } else {
        }
    }

}
