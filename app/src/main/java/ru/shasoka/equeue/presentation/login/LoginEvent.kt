/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.login

sealed class LoginEvent {
    data class LoginUser(
        val username: String,
        val password: String,
    ) : LoginEvent()

    data object DisposeAlert : LoginEvent()
}
