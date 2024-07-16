/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.login.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import ru.shasoka.equeue.R
import ru.shasoka.equeue.presentation.Dimensions.MediumPadding
import ru.shasoka.equeue.ui.theme.EQueueTheme

@Composable
fun FormField(
    placeholder: String,
    icon: ImageVector,
    modifier: Modifier = Modifier,
    isSecret: Boolean = false,
) {
    var text by remember { mutableStateOf("") }
    var passwordVisible by remember { mutableStateOf(false) }
	
    val visualTransformation =
        if (isSecret && !passwordVisible) {
            PasswordVisualTransformation()
        } else {
            VisualTransformation.None
        }
	
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
                imageVector = icon,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.secondary,
            )
            BasicTextField(
                value = text,
                onValueChange = { text = it },
                visualTransformation = visualTransformation,
                maxLines = 1,
                textStyle =
                    MaterialTheme.typography.bodyMedium.copy(
                        color = MaterialTheme.colorScheme.secondary,
                        fontWeight = FontWeight.Bold,
                    ),
                decorationBox = { innerTextField ->
                    if (text.isEmpty()) {
                        Text(
                            text = placeholder,
                            color = MaterialTheme.colorScheme.secondary,
                            style = MaterialTheme.typography.bodyMedium,
                        )
                    }
                    innerTextField()
                },
                modifier =
                    Modifier
                        .padding(start = 8.dp)
                        .weight(1f)
                        .horizontalScroll(rememberScrollState()),
            )
            if (isSecret) {
                IconButton(
                    modifier = Modifier.then(Modifier.size(24.dp)),
                    onClick = { passwordVisible = !passwordVisible },
                ) {
                    Icon(
                        painter =
                            if (passwordVisible) {
                                painterResource(R.drawable.visibility_on)
                            } else {
                                painterResource(R.drawable.visibility_off)
                            },
                        contentDescription = if (passwordVisible) "Hide password" else "Show password",
                        modifier = Modifier.size(24.dp).padding(all = 0.dp),
                        tint = MaterialTheme.colorScheme.secondary,
                    )
                }
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
private fun FormFieldPreview() {
    EQueueTheme(dynamicColor = false) {
        Column {
            FormField(
                placeholder = "Введите логин ... ",
                icon = Icons.Default.Person,
            )
            FormField(
                placeholder = "Введите пароль ...",
                icon = Icons.Default.Lock,
                isSecret = true,
            )
        }
    }
}
