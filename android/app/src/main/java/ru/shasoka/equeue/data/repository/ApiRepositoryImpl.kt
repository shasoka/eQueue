/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.data.repository

import ru.shasoka.equeue.data.remote.Api
import ru.shasoka.equeue.data.remote.dto.ECoursesLoginResponse
import ru.shasoka.equeue.data.remote.dto.GetGroupsResponse
import ru.shasoka.equeue.domain.repository.ApiRepository
import java.net.URLEncoder

class ApiRepositoryImpl(
    private val api: Api,
) : ApiRepository {
    @Suppress("BlockingMethodInNonBlockingContext")
    override suspend fun login(
        username: String,
        password: String,
    ): ECoursesLoginResponse {
        try {
            return api.login(
                URLEncoder.encode(username, "utf-8"),
                URLEncoder.encode(password, "utf-8")
            )
        } catch (e: Exception) {
            throw e
        }
    }

    override suspend fun getGroups(token: String): GetGroupsResponse {
        try {
            return api.getGroups(token)
        } catch (e: Exception) {
            throw e
        }
    }
}
