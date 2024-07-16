/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.onboarding.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import ru.shasoka.equeue.presentation.Dimensions.IndicatorSize
import ru.shasoka.equeue.ui.theme.Gray

@Composable
fun PageIndicator(
    pageSize: Int,
    selectedPage: Int,
    modifier: Modifier = Modifier,
    selectedColor: Color = MaterialTheme.colorScheme.primary,
    unselectedColor: Color = Gray,
) {
    Row(
        modifier = modifier,
        horizontalArrangement = Arrangement.SpaceBetween,
    ) {
        repeat(pageSize) { page ->
            Box(
                modifier =
                    Modifier
                        .size(
                            IndicatorSize,
                        ).clip(CircleShape)
                        .background(color = if (page == selectedPage) selectedColor else unselectedColor),
            )
        }
    }
}
