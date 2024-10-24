/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.domain.usecases.appentry

import kotlinx.coroutines.flow.Flow
import ru.shasoka.equeue.domain.manager.LocalUserManager

class ReadAppEntry(
    // Using abstract repository
    private val localUserManager: LocalUserManager,
) {
    // Operator allows to call this function by class name
    operator fun invoke(): Flow<Boolean> = localUserManager.readAppEntry()
}
