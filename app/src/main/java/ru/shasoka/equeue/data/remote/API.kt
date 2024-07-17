/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.data.remote

import retrofit2.Call
import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.POST
import ru.shasoka.equeue.data.remote.dto.ECoursesLoginResponse

interface API {
    @FormUrlEncoded
    @POST("users/moodle_auth")
    fun login(
        @Field("username") username: String,
        @Field("password") password: String,
    ): Call<ECoursesLoginResponse>
}
