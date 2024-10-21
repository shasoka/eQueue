/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.login

import androidx.navigation.NavController

sealed class LoginEvent {
    data class LoginUser(
        val username: String,
        val password: String,
        val navController: NavController,
    ) : LoginEvent()

    data object DisposeAlert : LoginEvent()
}
