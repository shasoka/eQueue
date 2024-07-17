/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.nvgraph

sealed class Route(
    val route: String,
) {
    object OnBoardingScreen : Route(route = "onBoardingScreen")

    object LogInScreen : Route(route = "logInScreen")

    object GroupSelectionScreen : Route(route = "groupSelectionScreen")

    object HomeScreen : Route(route = "homeScreen")

    // Subgraphs
    object AppStartNavigation : Route(route = "appStartNavigation")

    object LogInNavigation : Route(route = "logInNavigation")

    object GroupSelectionNavigation : Route(route = "groupSelectionNavigation")
}
