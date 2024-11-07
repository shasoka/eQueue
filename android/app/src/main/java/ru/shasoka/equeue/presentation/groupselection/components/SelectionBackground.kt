/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.groupselection.components

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.style.TextAlign
import ru.shasoka.equeue.R
import ru.shasoka.equeue.util.Dimensions.MediumPadding
import ru.shasoka.equeue.util.Dimensions.SmallPadding

@Composable
fun SelectionBackground(
    text: String,
    contentAlpha: Float,
    modifier: Modifier = Modifier,
) {
    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Image(
            painter = painterResource(id = R.drawable.sfu_u),
            contentDescription = null,
            contentScale = ContentScale.Fit,
            modifier =
                Modifier
                    .padding(SmallPadding),
            alpha = contentAlpha,
        )
        Text(
            text = text,
            style =
                MaterialTheme.typography.bodyLarge.copy(
                    color =
                        MaterialTheme
                            .colorScheme.onBackground
                            .copy(alpha = contentAlpha),
                ),
            textAlign = TextAlign.Center,
            modifier =
                Modifier
                    .fillMaxWidth()
                    .padding(all = MediumPadding),
        )
    }
}
