/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.domain.repository

import ru.shasoka.equeue.data.remote.dto.ECoursesLoginResponse
import ru.shasoka.equeue.data.remote.dto.GetGroupsResponse

interface ApiRepository {
    suspend fun login(
        username: String,
        password: String,
    ): ECoursesLoginResponse

    suspend fun getGroups(token: String): GetGroupsResponse
}
