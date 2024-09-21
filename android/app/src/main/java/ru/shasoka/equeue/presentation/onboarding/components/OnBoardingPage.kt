/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.onboarding.components

import android.content.res.Configuration.UI_MODE_NIGHT_YES
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import ru.shasoka.equeue.presentation.Dimensions.LargePadding
import ru.shasoka.equeue.presentation.Dimensions.LargestPadding
import ru.shasoka.equeue.presentation.onboarding.Page
import ru.shasoka.equeue.presentation.onboarding.pages
import ru.shasoka.equeue.ui.theme.EQueueTheme

@Composable
fun OnBoardingPage(
    page: Page,
    modifier: Modifier = Modifier,
) {
    val configuration = LocalConfiguration.current
    val screenHeight = configuration.screenHeightDp.dp
	
    Column(
        verticalArrangement = Arrangement.Top,
    ) {
        Image(
            painter = painterResource(id = page.image),
            contentDescription = null,
            contentScale = ContentScale.FillWidth,
            modifier = Modifier
                .height(screenHeight / 2 - 5.dp)
                .fillMaxWidth(),
        )
        Spacer(
            modifier =
                Modifier.height(
                    LargePadding,
                ),
        )
        Text(
            text = page.title,
            modifier = Modifier.padding(horizontal = LargestPadding),
            style = MaterialTheme.typography.displaySmall.copy(fontWeight = FontWeight.Bold),
            color = MaterialTheme.colorScheme.inverseSurface,
        )
		
        val scrollState = rememberScrollState()
        val lineHeightDp: Dp =
            with(LocalDensity.current) {
                MaterialTheme.typography.bodyMedium.lineHeight
                    .toDp()
            }
		
        Box(
            modifier =
            Modifier
                    .padding(horizontal = LargestPadding, vertical = LargePadding)
                    .height(lineHeightDp * 5) // Set the maximum height for the text box
                .verticalScroll(scrollState),
            contentAlignment = Alignment.Center,
        ) {
            Text(
                text = page.description,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                minLines = 5,
            )
        }
    }
}

@Preview(showBackground = true)
@Preview(uiMode = UI_MODE_NIGHT_YES)
@Composable
private fun OnBoardingPagePreview() {
    EQueueTheme {
        OnBoardingPage(
            page = pages[0],
        )
    }
}
