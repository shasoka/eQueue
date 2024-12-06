/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.data.remote.serializer

import com.google.gson.JsonElement
import com.google.gson.JsonObject
import com.google.gson.JsonSerializationContext
import com.google.gson.JsonSerializer
import ru.shasoka.equeue.data.remote.dto.UserUpdate
import java.lang.reflect.Type

class UserUpdateSerializer : JsonSerializer<UserUpdate> {
    override fun serialize(
        src: UserUpdate?,
        typeOfSrc: Type?,
        context: JsonSerializationContext?
    ): JsonElement {
        val jsonObject = JsonObject()

        if (src?.access_token != null) {
            jsonObject.addProperty("access_token", src.access_token)
        }

        jsonObject.addProperty("assigned_group_id", src?.assigned_group_id)

        if (src?.status != null) {
            jsonObject.addProperty("status", src.status)
        }

        if (src?.user_picture_url != null) {
            jsonObject.addProperty("user_picture_url", src.user_picture_url)
        }

        return jsonObject
    }
}
