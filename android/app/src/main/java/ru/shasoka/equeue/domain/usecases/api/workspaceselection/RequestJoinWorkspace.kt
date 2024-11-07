package ru.shasoka.equeue.domain.usecases.api.workspaceselection

import ru.shasoka.equeue.data.local.UserDao
import ru.shasoka.equeue.domain.repository.ApiRepository

class RequestJoinWorkspace(
    private val apiRepository: ApiRepository,
    private val userDao: UserDao,
)
