/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.data.repository

import ru.shasoka.equeue.data.remote.Api
import ru.shasoka.equeue.data.remote.dto.ListOfGroupRead
import ru.shasoka.equeue.data.remote.dto.ListOfWorkspaceRead
import ru.shasoka.equeue.data.remote.dto.UserAuth
import ru.shasoka.equeue.data.remote.dto.UserRead
import ru.shasoka.equeue.data.remote.dto.UserUpdate
import ru.shasoka.equeue.domain.repository.ApiRepository

class ApiRepositoryImpl(
    private val api: Api,
) : ApiRepository {
    override suspend fun login(
        username: String,
        password: String,
    ): UserAuth {
        try {
            return api.login(
                username,
                password,
            )
        } catch (e: Exception) {
            throw e
        }
    }

    override suspend fun getGroups(header: String): ListOfGroupRead {
        try {
            return api.getGroups(header)
        } catch (e: Exception) {
            throw e
        }
    }

    override suspend fun patchUser(
        header: String,
        body: UserUpdate,
    ): UserRead {
        try {
            return api.patchUser(
                header,
                body,
            )
        } catch (e: Exception) {
            throw e
        }
    }

    override suspend fun getExistingWorkspaces(header: String): ListOfWorkspaceRead {
        try {
            return api.getExistingWorkspaces(header)
        } catch (e: Exception) {
            throw e
        }
    }
}
