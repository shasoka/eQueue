/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.domain.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Suppress("PropertyName")
@Entity
data class User(
    @PrimaryKey val id: Int,
    val access_token: String,
    val token_type: String,
    val talon: String?,
    val assigned_group_id: Int?,
    val assigned_workspace_id: Int?,
    val workspace_chief: Boolean,
    val first_name: String,
    val second_name: String,
    val ecourses_user_id: Int,
    val status: String,
    val user_picture_url: String,
    val created_at: String,
)
