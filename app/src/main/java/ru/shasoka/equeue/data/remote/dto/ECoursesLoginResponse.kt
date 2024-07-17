/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.data.remote.dto

@Suppress("PropertyName")
data class ECoursesLoginResponse(
    val access_token: String,
    val assigned_group_id: Int,
    val assigned_workspace_id: Int,
    val created_at: String,
    val ecourses_user_id: Int,
    val first_name: String,
    val id: Int,
    val second_name: String,
    val status: String,
    val talon: String,
    val token_type: String,
    val user_picture_url: String,
    val workspace_chief: Boolean,
)
