/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.data.remote.dto

data class UserReadResponse(
    val assigned_group_id: Any,
    val assigned_workspace_id: Any,
    val created_at: String,
    val ecourses_user_id: Int,
    val first_name: String,
    val id: Int,
    val second_name: String,
    val status: String,
    val talon: String,
    val user_picture_url: String,
    val workspace_chief: Boolean,
)
