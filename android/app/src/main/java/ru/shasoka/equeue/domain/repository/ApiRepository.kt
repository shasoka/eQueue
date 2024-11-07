/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.domain.repository

import ru.shasoka.equeue.data.remote.dto.ListOfGroupRead
import ru.shasoka.equeue.data.remote.dto.ListOfWorkspaceRead
import ru.shasoka.equeue.data.remote.dto.UserAuth
import ru.shasoka.equeue.data.remote.dto.UserRead
import ru.shasoka.equeue.data.remote.dto.UserUpdate

interface ApiRepository {
    suspend fun login(
        username: String,
        password: String,
    ): UserAuth

    suspend fun getGroups(header: String): ListOfGroupRead

    suspend fun patchUser(
        header: String,
        body: UserUpdate,
    ): UserRead

    suspend fun getExistingWorkspaces(header: String): ListOfWorkspaceRead
}
