/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.domain.usecases.api.groups

class GroupsUseCases(
    val getGroups: GetGroups,
    val joinGroup: JoinGroup,
    val leaveGroup: LeaveGroup,
)
