/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.util

enum class ConnAlerts {
    BASE_CONNECTION,
}

enum class DbAlerts {
    DB_ERROR,
}

enum class DataAlerts {
    DATA_LOADING,
}

sealed class Alerts {
    data class Connection(
        val alert: ConnAlerts,
    ) : Alerts()

    data class Data(
        val alert: DataAlerts,
    ) : Alerts()

    data class Db(
        val alert: DbAlerts,
    ) : Alerts()
}
