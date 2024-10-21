/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.domain.usecases.appentry

import ru.shasoka.equeue.domain.manager.LocalUserManager

class SaveAppEntry(
    // Using abstract repository
    private val localUserManager: LocalUserManager,
) {
    // Operator allows to call this function by class name
    suspend operator fun invoke() {
        localUserManager.saveAppEntry()
    }
}
