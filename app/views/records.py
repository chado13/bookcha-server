from fastapi import APIRouter

router = APIRouter()


@router.get("/{user_id}")
def fetch_records(user: int):
    data = service.fetch_all_records(user)
    return data


@router.post("/{user_id}")
def create_record(user_id: int):
    service.create_record(user_id)
    return {"message": "success"}


@router.put("/{record_id}")
def update_record(record_id: int):
    res = service.update_record(record_id)
    return res


@router.delete("/{record_id}")
def remove_record(record_id: int):
    service.remove_record(record_id)
    return {"message": "success"}
