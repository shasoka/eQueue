#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from core.models import db_helper
from crud.queues import get_subject_queue, enter_subject_queue, leave_subject_queue
from moodle.auth import MoodleOAuth2
from websocket import manager

router = APIRouter(tags=["Websocket"])


@router.websocket("/{subject_id}", name="Endpoint for queue websocket")
async def websocket_endpoint(
    *,  # All next params must be keyword-only
    websocket: WebSocket,
    subject_id: int,
    token: Annotated[str, Query(...)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    current_user = await MoodleOAuth2.validate_token(token, session)

    await manager.connect(websocket, subject_id)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                match data:
                    case "get":
                        queue = await get_subject_queue(
                            session=session,
                            user=current_user,
                            subject_id=subject_id,
                        )
                        await manager.send_personal_message(queue, websocket)
                    case "enter":
                        updated_queue = await enter_subject_queue(
                            session=session,
                            user=current_user,
                            subject_id=subject_id,
                        )
                        await manager.broadcast(updated_queue, subject_id)
                    case "leave":
                        updated_queue = await leave_subject_queue(
                            session=session,
                            user=current_user,
                            subject_id=subject_id,
                        )
                        await manager.broadcast(updated_queue, subject_id)
                    case "leave_and_mark":
                        updated_queue = await leave_subject_queue(
                            session=session,
                            user=current_user,
                            subject_id=subject_id,
                            mark_done=True,
                        )
                        await manager.broadcast(updated_queue, subject_id)
                    case _:
                        raise HTTPException(
                            status_code=400,
                            detail="Bad request",
                        )
            except HTTPException as e:
                await manager.send_personal_message({"error": e.detail}, websocket)
            except Exception as e:
                await manager.send_personal_message({"error": str(e)}, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, subject_id)
    except Exception as e:  # Broad exception for unexpected errors
        manager.disconnect(websocket, subject_id)
        raise e
