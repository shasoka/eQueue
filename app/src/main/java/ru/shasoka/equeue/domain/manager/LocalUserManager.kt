/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.domain.manager

import kotlinx.coroutines.flow.Flow

// Repository
interface LocalUserManager {
    suspend fun saveAppEntry()

    suspend fun readAppEntry(): Flow<Boolean>
}
