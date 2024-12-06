/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.util

import java.util.Calendar

fun extractYearOfAssignmentFromGroupName(input: String): Int {
    val regex = Regex("[^0-9]*(\\d+)")
    val yearOfAssignment = regex.find(input)?.groupValues?.get(1)?.toIntOrNull() ?: return 0

    val currentYear = Calendar.getInstance().get(Calendar.YEAR)

    val yearsPassed = currentYear - (2000 + yearOfAssignment)

    return if (yearsPassed < 0) 0 else {
        yearsPassed * 2 + if (Calendar.getInstance().get(Calendar.MONTH) >= 7) 1 else 2
    }
}
