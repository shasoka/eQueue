/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.onboarding

import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import ru.shasoka.equeue.presentation.Dimensions.MediumPadding2
import ru.shasoka.equeue.presentation.Dimensions.PageIndicatorWidth
import ru.shasoka.equeue.presentation.common.BackTextButton
import ru.shasoka.equeue.presentation.common.StartButton
import ru.shasoka.equeue.presentation.onboarding.components.OnBoardingPage
import ru.shasoka.equeue.presentation.onboarding.components.PageIndicator
import ru.shasoka.equeue.ui.theme.EQueueTheme

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun OnBoardingScreen() {
    Column(
        modifier = Modifier.fillMaxHeight(),
        verticalArrangement = Arrangement.SpaceBetween,
    ) {
        val pagerState =
            rememberPagerState(initialPage = 0) {
                pages.size
            }
		
        val buttonState =
            remember {
                derivedStateOf {
                    when (pagerState.currentPage) {
                        0 -> listOf("", "Далее")
                        1 -> listOf("Назад", "Войти")
                        else -> listOf("", "")
                    }
                }
            }
		
        HorizontalPager(
            contentPadding = PaddingValues(all = 0.dp),
            state = pagerState,
        ) { index ->
            OnBoardingPage(page = pages[index])
        }
		
        Row(
            modifier =
                Modifier
                    .fillMaxWidth()
                    .padding(all = MediumPadding2)
                    .navigationBarsPadding(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            PageIndicator(
                modifier = Modifier.width(PageIndicatorWidth),
                pageSize = pages.size,
                selectedPage = pagerState.currentPage,
            )
            Row(
                verticalAlignment = Alignment.CenterVertically,
            ) {
                val scope = rememberCoroutineScope()
				
                if (buttonState.value[0].isNotEmpty()) {
                    BackTextButton(
                        text = buttonState.value[0],
                        onClick = {
                            scope.launch {
                                pagerState.animateScrollToPage(page = pagerState.currentPage - 1)
                            }
                        },
                    )
                }
				
                StartButton(
                    text = buttonState.value[1],
                    onClick = {
                        scope.launch {
                            if (pagerState.currentPage == 3) {
                                // nav to login screen
                            } else {
                                pagerState.animateScrollToPage(page = pagerState.currentPage + 1)
                            }
                        }
                    },
                )
            }
        }
    }
}

@Preview(showBackground = true, widthDp = 480, heightDp = 800)
@Preview(showBackground = true, widthDp = 720, heightDp = 1280)
@Preview(showBackground = true, widthDp = 720, heightDp = 1600)
@Composable
private fun OnBoardingScreenPreview() {
    EQueueTheme {
        OnBoardingScreen()
    }
}
