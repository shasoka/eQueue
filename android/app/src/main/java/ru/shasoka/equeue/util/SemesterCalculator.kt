/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.util

import java.util.Calendar

fun extractSemesterFromGroupName(input: String): Int {
    val regex = Regex("[^0-9]*(\\d+)")
    val yearOfAssignment = regex.find(input)?.groupValues?.get(1)?.toIntOrNull() ?: return 0

    val admissionYear = 2000 + yearOfAssignment
    val calendar = Calendar.getInstance()
    val currentYear = calendar.get(Calendar.YEAR)
    val currentMonth = calendar.get(Calendar.MONTH)

    // 1st september of admission year
    val admissionDate = Calendar.getInstance().apply {
        set(admissionYear, Calendar.SEPTEMBER, 1)
    }

    // Number of full years
    val fullYears = if (calendar.after(admissionDate)) {
        currentYear - admissionYear - if (currentMonth < Calendar.SEPTEMBER) 1 else 0
    } else {
        -1
    }

    val firstSemesterMonths =
        listOf(
            Calendar.SEPTEMBER,
            Calendar.OCTOBER,
            Calendar.NOVEMBER,
            Calendar.DECEMBER,
            Calendar.JANUARY,
            Calendar.FEBRUARY
        )

    return if (fullYears < 0) {
        fullYears
    } else {
        if (currentMonth in firstSemesterMonths) {
            fullYears * 2 + 1
        } else {
            fullYears * 2 + 2
        }
    }
}
