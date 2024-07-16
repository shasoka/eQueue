/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.domain.repository

import ru.shasoka.equeue.data.remote.dto.ECoursesLoginResponse

interface APIRepository {
    suspend fun login(
        username: String,
        password: String,
    ): ECoursesLoginResponse
}
