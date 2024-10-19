/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.common

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import ru.shasoka.equeue.R
import ru.shasoka.equeue.presentation.Dimensions.MediumPadding
import ru.shasoka.equeue.presentation.Dimensions.SmallPadding

@Composable
fun SearchBar(
	placeholder: String,
	onTextChange: (String) -> Unit,
	onClick: () -> Unit,
	modifier: Modifier = Modifier,
	textState: String = "",
	keyboardOptions: KeyboardOptions = KeyboardOptions.Default,
	keyboardActions: KeyboardActions = KeyboardActions.Default,
) {

	Box(
		modifier =
		modifier
			.fillMaxWidth()
			.background(
				color = MaterialTheme.colorScheme.inverseOnSurface,
				shape = RoundedCornerShape(6.dp),
			).border(
				width = 1.dp,
				color = MaterialTheme.colorScheme.secondary,
				shape = RoundedCornerShape(6.dp),
			).padding(all = MediumPadding),
	) {
		Row(
			verticalAlignment = Alignment.CenterVertically,
			horizontalArrangement = Arrangement.Start,
			modifier = Modifier.fillMaxWidth(),
		) {
			Icon(
				imageVector = Icons.Default.Search,
				contentDescription = null,
				tint = MaterialTheme.colorScheme.secondary,
			)
			BasicTextField(
				value = textState,
				onValueChange = {
					onTextChange(it)
				},
				keyboardOptions = keyboardOptions,
				keyboardActions = keyboardActions,
				visualTransformation = VisualTransformation.None,
				maxLines = 1,
				textStyle = MaterialTheme.typography.bodyMedium.copy(
					color = MaterialTheme.colorScheme.secondary,
				),
				decorationBox = { innerTextField ->
					if (textState.isEmpty()) {
						Text(
							text = placeholder,
							color = MaterialTheme.colorScheme.secondary,
							style = MaterialTheme.typography.bodyMedium,
						)
					}
					innerTextField()
				},
				modifier = Modifier
					.padding(horizontal = SmallPadding)
					.weight(1f)
					.horizontalScroll(rememberScrollState()),
			)
			IconButton(
				modifier = Modifier.then(Modifier.size(24.dp)),
				onClick = { onClick() },
				) {
				Icon(
					painter = painterResource(R.drawable.nav_next),
					contentDescription = "Select this group and proceed",
					modifier = Modifier
						.size(24.dp)
						.padding(all = 0.dp),
					tint = MaterialTheme.colorScheme.secondary,
				)
			}
		}
	}
}
