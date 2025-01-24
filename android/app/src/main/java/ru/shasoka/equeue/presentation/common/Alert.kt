/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.presentation.common

import androidx.compose.foundation.layout.Box
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.text.font.FontWeight

@Composable
fun ExceptionAlert(
    onDismiss: () -> Unit,
    onConfirm: () -> Unit,
    alertContent: String,
    confirmBtnText: String = "Так точно \uD83E\uDEE1",
) {
    AlertDialog(
        onDismissRequest = onDismiss,
        confirmButton = {
            Button(onClick = onConfirm) {
                Text(text = confirmBtnText)
            }
        },
        text = {
            Box {
                Text(
                    text = alertContent,
                    style = MaterialTheme.typography.bodyMedium.copy(
                        color = MaterialTheme.colorScheme.secondary,
                        fontWeight = FontWeight.Bold,
                    ),
                )
            }
        },
        shape = MaterialTheme.shapes.medium,
    )
}
