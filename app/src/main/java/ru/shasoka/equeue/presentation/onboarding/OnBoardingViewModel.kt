/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.onboarding

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import ru.shasoka.equeue.domain.usecases.AppEntryUseCases
import javax.inject.Inject

@HiltViewModel
class OnBoardingViewModel
    @Inject
    constructor(
        private val appEntryUseCases: AppEntryUseCases,
    ) : ViewModel() {
        fun onEvent(event: OnBoardingEvent) {
            when (event) {
                is OnBoardingEvent.SaveAppEntry -> {
                    saveAppEntry()
                }
            }
        }

        private fun saveAppEntry() {
            viewModelScope.launch {
                appEntryUseCases.saveAppEntry()
            }
        }
    }
