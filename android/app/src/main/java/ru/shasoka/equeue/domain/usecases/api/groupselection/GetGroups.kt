/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.domain.usecases.api.groupselection

import kotlinx.coroutines.flow.first
import ru.shasoka.equeue.data.local.UserDao
import ru.shasoka.equeue.data.remote.dto.GetGroupsResponse
import ru.shasoka.equeue.domain.repository.ApiRepository

class GetGroups(
    private val apiRepository: ApiRepository,
    private val userDao: UserDao,
) {
    suspend operator fun invoke(): GetGroupsResponse {
        try {
            val user =
                userDao
                    .getUsers() // Get Flow<List<User>>
                    .first() // Get List<User>
                    .first() // Get User
            return apiRepository.getGroups(user.token_type + " " + user.access_token)
        } catch (e: Exception) {
            throw e
        }
    }
}
