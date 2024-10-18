/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.nvgraph

import androidx.compose.runtime.Composable
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navigation
import ru.shasoka.equeue.presentation.groupselection.GroupSelectionScreen
import ru.shasoka.equeue.presentation.groupselection.GroupSelectionViewModel
import ru.shasoka.equeue.presentation.login.LoginScreen
import ru.shasoka.equeue.presentation.login.LoginViewModel
import ru.shasoka.equeue.presentation.onboarding.OnBoardingScreen
import ru.shasoka.equeue.presentation.onboarding.OnBoardingViewModel

@Composable
fun NavGraph(startDestination: String) {
	val navController = rememberNavController()
	
	NavHost(navController = navController, startDestination = startDestination) {
		navigation(
			route = Route.AppStartNavigation.route,
			startDestination = Route.OnBoardingScreen.route,
		) {
			composable(route = Route.OnBoardingScreen.route) {
				val viewModel: OnBoardingViewModel = hiltViewModel()
				OnBoardingScreen(
					event = viewModel::onEvent,
				)
			}
		}
		
		navigation(
			route = Route.LogInNavigation.route,
			startDestination = Route.LogInScreen.route,
		) {
			composable(route = Route.LogInScreen.route) {
				val viewModel: LoginViewModel = hiltViewModel()
				LoginScreen(
					event = viewModel::onEvent,
					showAlert = viewModel.showAlert,
					isLoading = viewModel.isLoading,
					navController = navController,
				)
			}
		}
		
		navigation(
			route = Route.GroupSelectionNavigation.route,
			startDestination = Route.GroupSelectionScreen.route,
		) {
			composable(route = Route.GroupSelectionScreen.route) {
				val viewModel: GroupSelectionViewModel = hiltViewModel()
				GroupSelectionScreen(
					groups = viewModel.groups,
					isLoading = viewModel.isLoading,
					showAlert = viewModel.showAlert,
					showExitError = viewModel.showExitError,
					selectedGroup = viewModel.selectedGroup,
					event = viewModel::onEvent,
					navController = navController,
				)
			}
		}
	}
}
