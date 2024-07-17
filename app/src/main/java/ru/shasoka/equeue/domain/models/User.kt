/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.domain.models

@Suppress("PropertyName")
data class User(
    val id: Int,
    val access_token: String,
    val token_type: String,
    val talon: String,
    val assigned_group_id: Any,
    val assigned_workspace_id: Any,
    val workspace_chief: Boolean,
    val first_name: String,
    val second_name: String,
    val ecourses_user_id: Int,
    val status: String,
    val user_picture_url: String,
    val created_at: String,
)
