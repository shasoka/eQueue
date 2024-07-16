/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import ru.shasoka.equeue.R

val DINPro =
    FontFamily(
        fonts =
            listOf(
                Font(R.font.dinpro, FontWeight.Normal),
                Font(R.font.dinpro_bold, FontWeight.Bold),
                Font(R.font.dinpro_medium, FontWeight.SemiBold),
            ),
    )

val Typography =
    Typography(
        displaySmall =
            TextStyle(
                fontSize = 24.sp,
                fontFamily = DINPro,
                fontWeight = FontWeight.Normal,
                lineHeight = 36.sp,
            ),
        displayMedium =
            TextStyle(
                fontSize = 32.sp,
                fontFamily = DINPro,
                fontWeight = FontWeight.Normal,
                lineHeight = 48.sp,
            ),
        bodySmall =
            TextStyle(
                fontSize = 14.sp,
                fontFamily = DINPro,
                fontWeight = FontWeight.Normal,
                lineHeight = 21.sp,
            ),
        bodyMedium =
            TextStyle(
                fontSize = 16.sp,
                fontFamily = DINPro,
                fontWeight = FontWeight.Normal,
                lineHeight = 24.sp,
            ),
        labelSmall =
            TextStyle(
                fontSize = 13.sp,
                fontFamily = DINPro,
            fontWeight = FontWeight.Normal,
            lineHeight = 19.sp,
        ),
    )
