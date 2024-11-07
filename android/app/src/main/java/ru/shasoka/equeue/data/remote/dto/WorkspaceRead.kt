package ru.shasoka.equeue.data.remote.dto

data class WorkspaceRead(
    val id: Int,
    val users: ListOfUserRead,
    val group_id: Int,
    val name: String?,
    val semester: Int?,
    val about: String?,
    val pending_users: ArrayList<Int>?,
)
