/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.login

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import ru.shasoka.equeue.data.remote.dto.ECoursesLoginResponse
import ru.shasoka.equeue.domain.usecases.api.APIUseCases
import javax.inject.Inject

@HiltViewModel
class LoginViewModel
    @Inject
    constructor(
        private val apiUseCases: APIUseCases,
    ) : ViewModel() {
        var userProfileData: ECoursesLoginResponse? = null
            private set

        var showAlert: Boolean by mutableStateOf(false)
            private set

        var isLoading: Boolean by mutableStateOf(false)
            private set

        fun onEvent(event: LoginEvent) {
            when (event) {
                is LoginEvent.LoginUser -> {
                    viewModelScope.launch {
                        try {
                            isLoading = true
                            delay(500)
                            userProfileData = loginUser(event.username, event.password)
                            isLoading = false
                        } catch (e: Exception) {
                            showAlert = true
                            isLoading = false
                        }
                    }
                }

                is LoginEvent.DisposeAlert -> {
                    showAlert = false
                }
            }
        }

        private suspend fun loginUser(
            username: String,
            password: String,
        ): ECoursesLoginResponse {
            try {
                return apiUseCases.loginUser(username, password)
            } catch (e: Exception) {
                throw e
            }
        }
    }
