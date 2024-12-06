/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import ru.shasoka.equeue.data.local.UserDao
import ru.shasoka.equeue.domain.usecases.appentry.AppEntryUseCases
import ru.shasoka.equeue.presentation.nvgraph.Route
import javax.inject.Inject

@HiltViewModel
class MainViewModel
@Inject
constructor(
    private val appEntryUseCases: AppEntryUseCases,
    private val userDao: UserDao,
) : ViewModel() {
    var splashCondition by mutableStateOf(true)
        private set

    var startDestination by mutableStateOf(Route.AppStartNavigation.route)
        private set

    init {
        viewModelScope.launch {
            // Получаем список пользователей из базы данных
            val users = userDao.getUsers().first()
            val user = users.firstOrNull() // Получаем первого пользователя или null

            if (user != null) {
                // Проверяем наличие группы у пользователя
                startDestination = if (user.assigned_group_id != null) {
                    Route.WorkspaceSelectionNavigation.route
                } else {
                    Route.GroupSelectionNavigation.route
                }
                delay(300)
                splashCondition = false
                return@launch
            }

            // Читаем состояние приложения для определения начального маршрута
            appEntryUseCases
                .readAppEntry()
                .collectLatest { shouldStartFromLoginScreen ->
                    startDestination = if (shouldStartFromLoginScreen) {
                        Route.LogInNavigation.route
                    } else {
                        Route.AppStartNavigation.route
                    }
                    delay(300)
                    splashCondition = false
                }
        }
    }
}
