/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.data.remote

import retrofit2.http.Body
import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.PATCH
import retrofit2.http.POST
import retrofit2.http.Path
import ru.shasoka.equeue.data.remote.dto.GroupRead
import ru.shasoka.equeue.data.remote.dto.ListOfGroupRead
import ru.shasoka.equeue.data.remote.dto.ListOfWorkspaceRead
import ru.shasoka.equeue.data.remote.dto.UserAuth
import ru.shasoka.equeue.data.remote.dto.UserRead
import ru.shasoka.equeue.data.remote.dto.UserUpdate
import ru.shasoka.equeue.data.remote.dto.WorkspaceCreate
import ru.shasoka.equeue.data.remote.dto.WorkspaceRead

interface Api {
    @FormUrlEncoded
    @POST("users/moodle_auth")
    suspend fun login(
        @Field("username") username: String,
        @Field("password") password: String,
    ): UserAuth

    @GET("groups")
    suspend fun getGroups(
        @Header("Authorization") header: String,
    ): ListOfGroupRead

    @GET("groups/{group_id}")
    suspend fun getSingleGroup(
        @Header("Authorization") header: String,
        @Path("group_id") groupId: String,
    ): GroupRead

    @PATCH("users")
    suspend fun patchUser(
        @Header("Authorization") header: String,
        @Body userUpdate: UserUpdate,
    ): UserRead

    @GET("workspaces")
    suspend fun getExistingWorkspaces(
        @Header("Authorization") header: String,
    ): ListOfWorkspaceRead

    @POST("workspaces")
    suspend fun createNewWorkspace(
        @Header("Authorization") header: String,
        @Body workspaceCreate: WorkspaceCreate,
    ): WorkspaceRead
}
