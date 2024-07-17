/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.domain.usecases.api

import ru.shasoka.equeue.data.remote.dto.ECoursesLoginResponse
import ru.shasoka.equeue.domain.repository.APIRepository

class LoginUser(
    private val apiRepository: APIRepository,
) {
    suspend operator fun invoke(
        username: String,
        password: String,
    ): ECoursesLoginResponse {
        try {
            return apiRepository.login(username, password)
        } catch (e: Exception) {
            throw e
        }
    }
}
