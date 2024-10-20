/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.data.remote.dto

import ru.shasoka.equeue.domain.model.User

// TODO на бэке поправить кодирование полей
data class UserAuth(
    val access_token: String,
    val assigned_group_id: Int?,
    val assigned_workspace_id: Int?,
    val created_at: String,
    val ecourses_user_id: Int,
    val first_name: String,
    val id: Int,
    val second_name: String,
    val status: String,
    val talon: String?,
    val token_type: String,
    val user_picture_url: String,
    val workspace_chief: Boolean,
)

fun UserAuth.toUser(): User =
    User(
        id = this.id,
        access_token = this.access_token,
        token_type = this.token_type,
        talon = this.talon,
        assigned_group_id = this.assigned_group_id,
        assigned_workspace_id = this.assigned_workspace_id,
        workspace_chief = this.workspace_chief,
        first_name = this.first_name,
        second_name = this.second_name,
        ecourses_user_id = this.ecourses_user_id,
        status = this.status,
        user_picture_url = this.user_picture_url,
        created_at = this.created_at,
    )
