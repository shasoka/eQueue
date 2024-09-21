/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.groupselection.components

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import ru.shasoka.equeue.presentation.Dimensions.MediumPadding

@Composable
fun SearchResult(
	text: String,
	modifier: Modifier = Modifier,
) {
	// Height is about 33.dp
	Box(
		modifier =
		modifier
			.fillMaxWidth()
			.padding(all = MediumPadding)
			.horizontalScroll(rememberScrollState()),
		contentAlignment = Alignment.CenterStart,
	) {
		Text(
			text = text,
			style =
			MaterialTheme.typography.bodyMedium.copy(
				color = MaterialTheme.colorScheme.secondary,
				fontWeight = FontWeight.SemiBold,
			),
			textAlign = TextAlign.Start,
			overflow = TextOverflow.Ellipsis,
			maxLines = 1,
		)
	}
}