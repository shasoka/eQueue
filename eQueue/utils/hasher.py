import hashlib


def hash_from_str(string_in: str) -> str:
	return hashlib.sha256(string_in.encode('utf-8')).hexdigest()
