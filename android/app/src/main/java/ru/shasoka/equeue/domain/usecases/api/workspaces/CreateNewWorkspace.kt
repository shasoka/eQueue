/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.domain.usecases.api.workspaces

import kotlinx.coroutines.flow.first
import ru.shasoka.equeue.data.local.UserDao
import ru.shasoka.equeue.data.remote.dto.WorkspaceCreate
import ru.shasoka.equeue.data.remote.dto.WorkspaceRead
import ru.shasoka.equeue.domain.repository.ApiRepository

class CreateNewWorkspace(
    private val apiRepository: ApiRepository,
    private val userDao: UserDao,
) {
    suspend operator fun invoke(
        name: String,
        about: String? = null
    ): WorkspaceRead {
        try {
            val user = userDao
                .getUsers() // Get Flow<List<User>>
                .first() // Get List<User>
                .firstOrNull() // Get User
            if (user == null) {
                throw Exception("User not found")
            }

            if (user.assigned_group_id == null) {
                throw Exception("User not assigned to a group")
            }

            // TODO: get single group by id

            return apiRepository.createNewWorkspace(
                header = user.token_type + " " + user.access_token,
                body = WorkspaceCreate(
                    group_id = user.assigned_group_id,
                    name = name,
                    about = about,
                    semester = 1,
                )
            )
        } catch (e: Exception) {
            throw e
        }
    }
}
