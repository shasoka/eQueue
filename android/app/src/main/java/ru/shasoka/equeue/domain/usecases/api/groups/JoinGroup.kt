/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.domain.usecases.api.groups

import kotlinx.coroutines.flow.first
import ru.shasoka.equeue.data.local.UserDao
import ru.shasoka.equeue.data.remote.dto.UserRead
import ru.shasoka.equeue.data.remote.dto.UserUpdate
import ru.shasoka.equeue.domain.repository.ApiRepository

class JoinGroup(
    private val apiRepository: ApiRepository,
    private val userDao: UserDao,
) {
    suspend operator fun invoke(groupId: Int): UserRead = try {
        val user = userDao
            .getUsers()
            .first()
            .firstOrNull()
        if (user == null) {
            throw Exception("User not found")
        }
        val response = apiRepository.patchUser(
            user.token_type + " " + user.access_token,
            UserUpdate(
                assigned_group_id = groupId,
            ),
        )

        // Getting assigned group id from response after successful request
        userDao.upsert(user.copy(assigned_group_id = response.assigned_group_id))
        response
    } catch (e: Exception) {
        throw e
    }
}
