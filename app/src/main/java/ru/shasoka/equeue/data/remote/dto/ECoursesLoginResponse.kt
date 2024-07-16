/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.data.remote.dto

data class ECoursesLoginResponse(
    val accessToken: String,
    val assignedGroupId: Int,
    val assignedWorkspaceId: Int,
    val createdAt: String,
    val ecoursesUserId: Int,
    val firstName: String,
    val id: Int,
    val secondName: String,
    val status: String,
    val talon: String,
    val tokenType: String,
    val userPictureUrl: String,
    val workspaceChief: Boolean,
)
