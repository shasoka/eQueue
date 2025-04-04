package ru.shasoka.equeue.presentation.workspaceselection

import android.app.Activity
import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
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
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.platform.LocalContext
import androidx.navigation.NavController
import ru.shasoka.equeue.data.remote.dto.WorkspaceRead
import ru.shasoka.equeue.presentation.common.ExceptionAlert
import ru.shasoka.equeue.presentation.common.HyperlinkNAV
import ru.shasoka.equeue.presentation.common.SelectionBackground
import ru.shasoka.equeue.presentation.common.SubmitButon
import ru.shasoka.equeue.presentation.workspaceselection.components.WorkspaceCreationDialog
import ru.shasoka.equeue.util.Alerts
import ru.shasoka.equeue.util.DataAlerts
import ru.shasoka.equeue.util.Dimensions.SmallPadding

fun spawnDisposeAlertDataConflict(event: (WorkspaceSelectionEvent) -> Unit) {
    event(WorkspaceSelectionEvent.DisposeAlert(Alerts.Data(DataAlerts.DATA_CONFLICT)))
}

@Composable
fun WorkspaceSelectionScreen(
    workspaces: List<WorkspaceRead>,
    isLoading: Boolean,
    showWorkspacesLoadingAlert: Boolean,
    showGroupLeaveAlert: Boolean,
    showConnectionAlert: Boolean,
    showDbErrorAlert: Boolean,
    onNameChange: (String) -> Unit,
    onAboutChange: (String) -> Unit,
    showWorkspaceCreationModal: Boolean,
    event: (WorkspaceSelectionEvent) -> Unit,
    navController: NavController,
    modifier: Modifier = Modifier
) {
    val globalAlpha by animateFloatAsState(
        targetValue = if (isLoading || showWorkspaceCreationModal) 0.1f else 1f,
        label = ""
    )

    val context = LocalContext.current
    val activity = context as? Activity

    if (showGroupLeaveAlert) {
        ExceptionAlert(
            onDismiss = { spawnDisposeAlertDataConflict(event) },
            onConfirm = { spawnDisposeAlertDataConflict(event) },
            alertContent =
            "Вы не можете покинуть группу, пока являетесь администратором " +
                "связанного с этой группой рабочего пространства"
        )
    }

    Box(
        modifier =
        modifier
            .fillMaxSize()
            .padding(WindowInsets.ime.asPaddingValues()),
        contentAlignment = Alignment.Center
    ) {
        BackHandler {
            activity?.finish()
        }

        if (showWorkspaceCreationModal) {
            WorkspaceCreationDialog(
                onDismissRequest = { event(WorkspaceSelectionEvent.DisposeModal) },
                onConfirm = { event(WorkspaceSelectionEvent.CreateWorkspace) },
                onNameChange = onNameChange,
                onAboutChange = onAboutChange
            )
        }

        AnimatedVisibility(
            visible = isLoading,
            enter = fadeIn(),
            exit = fadeOut()
        ) {
            CircularProgressIndicator()
        }

        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
            modifier =
            Modifier
                .fillMaxWidth()
                .fillMaxHeight()
                .alpha(globalAlpha)
        ) {
            if (workspaces.isEmpty()) { // Если не найдено ни одного рабочего пространства
                SelectionBackground(
                    contentAlpha = 0.5f,
                    text =
                    "Похоже никто еще не создал рабочее пространство для вашей группы." +
                        "\nВы можете стать первым!\n\uD83D\uDC51",
                    modifier = Modifier.fillMaxWidth(0.7f)
                )
                SubmitButon(
                    text = "Настало моё время...",
                    onClick = { event(WorkspaceSelectionEvent.InitModal) }
                )
            } else { // Если рабочее пространство для группы пользователя найдено
            }
            HyperlinkNAV(
                text = "Сменить группу \uD83D\uDEAA",
                modifier = Modifier.padding(vertical = SmallPadding),
                onClick = { event(WorkspaceSelectionEvent.ChangeGroup(navController)) }
            )
        }
    }
}
