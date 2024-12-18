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
import ru.shasoka.equeue.data.remote.dto.ListOfGroupRead
import ru.shasoka.equeue.data.remote.dto.ListOfWorkspaceRead
import ru.shasoka.equeue.data.remote.dto.UserAuth
import ru.shasoka.equeue.data.remote.dto.UserRead
import ru.shasoka.equeue.data.remote.dto.UserUpdate

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

    @PATCH("users")
    suspend fun patchUser(
        @Header("Authorization") header: String,
        @Body userUpdate: UserUpdate,
    ): UserRead

    @GET("workspaces")
    suspend fun getExistingWorkspaces(
        @Header("Authorization") header: String,
    ): ListOfWorkspaceRead
}
