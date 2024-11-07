/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.nvgraph

sealed class Route(
    val route: String,
) {
    data object OnBoardingScreen : Route(route = "onBoardingScreen")

    data object LogInScreen : Route(route = "logInScreen")

    data object GroupSelectionScreen : Route(route = "groupSelectionScreen")

    data object WorkspaceSelectionScreen : Route(route = "workspaceSelectionScreen")

    // Subgraphs
    data object AppStartNavigation : Route(route = "appStartNavigation")

    data object LogInNavigation : Route(route = "logInNavigation")

    data object GroupSelectionNavigation : Route(route = "groupSelectionNavigation")

    data object WorkspaceSelectionNavigation : Route(route = "workspaceSelectionNavigation")
}
