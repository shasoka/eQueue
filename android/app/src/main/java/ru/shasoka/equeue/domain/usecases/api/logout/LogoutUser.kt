package ru.shasoka.equeue.domain.usecases.api.logout

import kotlinx.coroutines.flow.first
import ru.shasoka.equeue.data.local.UserDao

class LogoutUser(
    private val userDao: UserDao,
    ) {
    suspend operator fun invoke() {
        try{
            userDao.delete(userDao.getUsers().first().firstOrNull() ?: return)
        } catch (e: Exception) {
            throw e
        }
    }
}
