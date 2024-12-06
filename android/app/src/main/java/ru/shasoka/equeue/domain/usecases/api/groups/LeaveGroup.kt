/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.domain.usecases.api.groups

import kotlinx.coroutines.flow.first
import ru.shasoka.equeue.data.local.UserDao
import ru.shasoka.equeue.data.remote.GroupLeaveException
import ru.shasoka.equeue.data.remote.dto.UserRead
import ru.shasoka.equeue.data.remote.dto.UserUpdate
import ru.shasoka.equeue.domain.repository.ApiRepository

class LeaveGroup(
    private val apiRepository: ApiRepository,
    private val userDao: UserDao,
) {
    suspend operator fun invoke(): UserRead =
        try {
            val user = userDao
                .getUsers()
                .first()
                .firstOrNull()
            if (user == null) {
                throw Exception("User not found")
            }

            if (user.workspace_chief) {
                throw GroupLeaveException("User can't leave group while is worskpace chief")
            }

            val response = apiRepository.patchUser(
                header = user.token_type + " " + user.access_token,
                body = UserUpdate(assigned_group_id = null),
            )

            userDao.upsert(user.copy(assigned_group_id = response.assigned_group_id))
            response
        } catch (e: Exception) {
            throw e
        }
}
