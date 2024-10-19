package ru.shasoka.equeue.domain.usecases.api.groupselection

import kotlinx.coroutines.flow.first
import ru.shasoka.equeue.data.local.UserDao
import ru.shasoka.equeue.data.remote.dto.UserReadResponse
import ru.shasoka.equeue.domain.repository.ApiRepository

class JoinGroup(
    private val apiRepository: ApiRepository,
    private val userDao: UserDao,
) {
    suspend operator fun invoke(
        groupId: Int,
    ): UserReadResponse {
        try {
            val user = userDao
                .getUsers()
                .first()
                .firstOrNull()
            if (user == null) {
                throw Exception("User not found")
            }
            return apiRepository.patchUser(
                user.token_type + " " + user.access_token,
                null,
                groupId,
                null,
                null
            )
        } catch (e: Exception) {
            throw e
        }
    }
}
