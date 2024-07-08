from fastapi import HTTPException


async def validate(
		response: dict,
		error_key: str = "exception",
		message_key: str = "message"
):
	if error_key in response:
		raise HTTPException(
			status_code=401,
			detail="Ответ от еКурсов: " + response[message_key]
		)
