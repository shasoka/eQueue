/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.data.remote.serializer

import com.google.gson.JsonElement
import com.google.gson.JsonObject
import com.google.gson.JsonSerializationContext
import com.google.gson.JsonSerializer
import ru.shasoka.equeue.data.remote.dto.WorkspaceCreate
import java.lang.reflect.Type

class WorkspaceCreateSerializer : JsonSerializer<WorkspaceCreate> {
    override fun serialize(
        src: WorkspaceCreate?,
        typeOfSrc: Type?,
        context: JsonSerializationContext?
    ): JsonElement {
        val jsonObject = JsonObject()

        jsonObject.addProperty("assigned_group_id", src?.group_id)
        jsonObject.addProperty("assigned_group_id", src?.name)
        jsonObject.addProperty("assigned_group_id", src?.semester)

        if (src?.about != null) {
            jsonObject.addProperty("status", src.about)
        }

        return jsonObject
    }
}
