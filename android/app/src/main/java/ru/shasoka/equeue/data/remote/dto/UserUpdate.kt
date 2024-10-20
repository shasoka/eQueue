/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.data.remote.dto

data class UserUpdate(
    val access_token: String? = null,
    val assigned_group_id: Int? = null,
    val status: String? = null,
    val user_picture_url: String? = null,
)
