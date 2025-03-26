/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.domain.usecases.api.workspaces

import kotlinx.coroutines.flow.first
import ru.shasoka.equeue.data.local.UserDao
import ru.shasoka.equeue.data.remote.dto.GroupRead
import ru.shasoka.equeue.data.remote.dto.WorkspaceCreate
import ru.shasoka.equeue.data.remote.dto.WorkspaceRead
import ru.shasoka.equeue.domain.repository.ApiRepository
import ru.shasoka.equeue.util.extractSemesterFromGroupName

class CreateNewWorkspace(private val apiRepository: ApiRepository, private val userDao: UserDao) {
    suspend operator fun invoke(name: String, about: String? = null): WorkspaceRead {
        try {
            val user = userDao
                .getUsers()
                .first()
                .firstOrNull()
            if (user == null) {
                throw Exception("User not found")
            }

            if (user.assigned_group_id == null) {
                throw Exception("User not assigned to a group")
            }

            val header: String = user.token_type + " " + user.access_token

            // Получение группы для вычисления текущего семестра
            val group: GroupRead = apiRepository.getSingleGroup(
                header = header,
                groupId = user.assigned_group_id.toString()
            )

            // Отправка запроса на создание воркспейса
            val newWs = apiRepository.createNewWorkspace(
                header = header,
                body = WorkspaceCreate(
                    group_id = user.assigned_group_id,
                    name = name,
                    about = if (about != "") about else null, // about == "", если не было введено
                    semester = extractSemesterFromGroupName(group.name)
                )
            )

            // Обновление пользователя в локальном хранилище
            userDao.upsert(
                user.copy(
                    id = user.id,
                    access_token = user.access_token,
                    token_type = user.token_type,
                    talon = user.talon,
                    assigned_group_id = user.assigned_group_id,
                    assigned_workspace_id = newWs.id,
                    workspace_chief = true,
                    first_name = user.first_name,
                    second_name = user.second_name,
                    ecourses_user_id = user.ecourses_user_id,
                    status = user.status,
                    user_picture_url = user.user_picture_url,
                    created_at = user.created_at
                )
            )

            return newWs
        } catch (e: Exception) {
            throw e
        }
    }
}
