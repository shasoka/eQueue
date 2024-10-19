/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.data.remote

import androidx.annotation.Nullable
import retrofit2.http.Body
import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.PATCH
import retrofit2.http.POST
import ru.shasoka.equeue.data.remote.dto.ECoursesLoginResponse
import ru.shasoka.equeue.data.remote.dto.GetGroupsResponse
import ru.shasoka.equeue.data.remote.dto.UserReadResponse

interface Api {
    @FormUrlEncoded
    @POST("users/moodle_auth")
    suspend fun login(
        @Field("username") username: String,
        @Field("password") password: String,
    ): ECoursesLoginResponse

    @GET("groups")
    suspend fun getGroups(
        @Header("Authorization") header: String,
    ): GetGroupsResponse

    @PATCH("users")
    suspend fun patchUser(
        @Header("Authorization") header: String,
        @Nullable @Body access_token: String?,
        @Nullable @Body assigned_group_id: Int?,
        @Nullable @Body status: String?,
        @Nullable @Body user_picture_url: String?,
    ): UserReadResponse
}
