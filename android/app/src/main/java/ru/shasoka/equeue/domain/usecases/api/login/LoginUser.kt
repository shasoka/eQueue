/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.domain.usecases.api.login

import android.util.Log
import ru.shasoka.equeue.data.local.UserDao
import ru.shasoka.equeue.data.remote.dto.ECoursesLoginResponse
import ru.shasoka.equeue.data.remote.dto.toUser
import ru.shasoka.equeue.domain.repository.ApiRepository

class LoginUser(
    private val apiRepository: ApiRepository,
    private val userDao: UserDao,
) {
    suspend operator fun invoke(
        username: String,
        password: String,
    ): ECoursesLoginResponse =
        try {
            val response = apiRepository.login(username, password)
            userDao.upsert(response.toUser())
            response
        } catch (e: Exception) {
            throw e
        }
}
