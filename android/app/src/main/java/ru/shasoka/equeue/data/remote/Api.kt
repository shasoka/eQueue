/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.data.remote

import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.POST
import ru.shasoka.equeue.data.remote.dto.ECoursesLoginResponse
import ru.shasoka.equeue.data.remote.dto.GetGroupsResponse

interface Api {
    @FormUrlEncoded
    @POST("users/moodle_auth")
    suspend fun login(
        @Field("username") username: String,
        @Field("password") password: String,
    ): ECoursesLoginResponse

    @GET("groups")
    suspend fun getGroups(
        @Header("Authorization") token: String,
    ): GetGroupsResponse
}