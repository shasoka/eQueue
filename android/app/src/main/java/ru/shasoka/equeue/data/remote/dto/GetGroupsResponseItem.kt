/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.data.remote.dto

data class GetGroupsResponseItem(
    val id: Int,
    val name: String,
    val users: List<UserReadResponse>,
)
