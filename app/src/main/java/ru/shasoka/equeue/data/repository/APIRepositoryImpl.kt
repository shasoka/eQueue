/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.data.repository

import ru.shasoka.equeue.data.remote.API
import ru.shasoka.equeue.data.remote.dto.ECoursesLoginResponse
import ru.shasoka.equeue.domain.repository.APIRepository

class APIRepositoryImpl(
    private val api: API,
) : APIRepository {
    override suspend fun login(
        username: String,
        password: String,
    ): ECoursesLoginResponse {
        try {
            return api.login(username, password)
        } catch (e: Exception) {
            throw e
        }
    }
}
