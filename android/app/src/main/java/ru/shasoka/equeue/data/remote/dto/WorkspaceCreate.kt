/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.data.remote.dto

data class WorkspaceCreate(
    val group_id: Int,
    val name: String,
    val semester: Int,
    val about: String? = null
)
