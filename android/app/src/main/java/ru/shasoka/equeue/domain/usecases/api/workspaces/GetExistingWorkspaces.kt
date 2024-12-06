package ru.shasoka.equeue.domain.usecases.api.workspaces

import kotlinx.coroutines.flow.first
import ru.shasoka.equeue.data.local.UserDao
import ru.shasoka.equeue.data.remote.dto.ListOfWorkspaceRead
import ru.shasoka.equeue.domain.repository.ApiRepository

class GetExistingWorkspaces(
    private val apiRepository: ApiRepository,
    private val userDao: UserDao,
) {
    suspend operator fun invoke(): ListOfWorkspaceRead {
        try {
            val user =
                userDao
                    .getUsers() // Get Flow<List<User>>
                    .first() // Get List<User>
                    .firstOrNull() // Get User
            if (user == null) {
                throw Exception("User not found")
            }
            return apiRepository.getExistingWorkspaces(
                user.token_type + " " + user.access_token,
            )
        } catch (e: Exception) {
            throw e
        }
    }
}
