/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.login

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import ru.shasoka.equeue.domain.usecases.api.APIUseCases
import javax.inject.Inject

@HiltViewModel
class LoginViewModel
    @Inject
    constructor(
        private val apiUseCases: APIUseCases,
    ) : ViewModel() {
        fun onEvent(event: LoginEvent) {
            when (event) {
                is LoginEvent.LoginUser -> {
                    viewModelScope.launch {
                        loginUser(event.username, event.password)
                    }
                }
            }
        }

        private suspend fun loginUser(
            username: String,
            password: String,
        ) {
            apiUseCases.loginUser(username, password)
        }
    }
