/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import ru.shasoka.equeue.domain.model.User

@Database(entities = [User::class], version = 1)
abstract class EQueueDatabase : RoomDatabase() {
    abstract val userDao: UserDao
}
