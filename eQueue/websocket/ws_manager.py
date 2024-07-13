#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
import json

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, subject_id: int):
        await websocket.accept()
        if subject_id not in self.active_connections:
            self.active_connections[subject_id] = []
        self.active_connections[subject_id].append(websocket)

    def disconnect(self, websocket: WebSocket, subject_id: int):
        self.active_connections[subject_id].remove(websocket)
        if not self.active_connections[subject_id]:
            del self.active_connections[subject_id]

    @staticmethod
    async def send_personal_message(message: str, websocket: WebSocket):
        await websocket.send_text(
            json.dumps(
                message,
                ensure_ascii=False,
                default=str,
            )
        )

    async def broadcast(self, message: str, subject_id: int):
        if subject_id in self.active_connections:
            for connection in self.active_connections[subject_id]:
                await connection.send_text(
                    json.dumps(
                        message,
                        ensure_ascii=False,
                        default=str,
                    )
                )


manager = ConnectionManager()
