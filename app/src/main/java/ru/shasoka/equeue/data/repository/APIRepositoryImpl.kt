/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.data.repository

import android.util.Log
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import ru.shasoka.equeue.data.remote.API
import ru.shasoka.equeue.data.remote.dto.ECoursesLoginResponse
import ru.shasoka.equeue.domain.repository.APIRepository

class APIRepositoryImpl(
    private val api: API,
) : APIRepository {
    override suspend fun login(
        username: String,
        password: String,
    ) {
        api.login(username, password).enqueue(
            object : Callback<ECoursesLoginResponse> {
                override fun onFailure(
                    call: Call<ECoursesLoginResponse>,
                    t: Throwable,
                ) = throw t

                override fun onResponse(
                    call: Call<ECoursesLoginResponse>,
                    response: Response<ECoursesLoginResponse>,
                ) {
                    if (response.body() == null) {
                        throw Exception("Server response is null")
                    } else {
                        val stringResponse = response.body().toString()
                        Log.d("HTTPResponse", stringResponse)
                    }
                }
            },
        )
    }
}
