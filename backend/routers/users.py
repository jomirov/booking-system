from fastapi import Body, Depends, HTTPException
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRouter

from ..repositories.userrepository import UserRepository
from ..models.user import UserCreate


router = APIRouter()

@router.post('/api/users')
async def add_user(user: UserCreate, repo: UserRepository = Depends(UserRepository)):
    await repo.create_user(user.email, user.password)

    return JSONResponse({"message": "User has been created"}, status_code=201)

@router.get('/api/users/{id}')
async def show_user(id: int, repo: UserRepository = Depends(UserRepository)):
    try:
        user = await repo.get_user(id)
    except ValueError:
        raise HTTPException(status_code=404)

    return JSONResponse(user)

@router.delete('/api/users/{id}')
async def remove_user(id: int, repo: UserRepository = Depends(UserRepository)):
    try:
        await repo.delete_user(id)
    except ValueError:
        raise HTTPException(status_code=404)

    return JSONResponse({"message": "User has been removed"})

@router.put('/api/users/{id}/email')
async def change_email(id: int, new_email: str = Body(), repo: UserRepository = Depends(UserRepository)):
    try:
        await repo.update_email(id, new_email)
    except ValueError:
        raise HTTPException(status_code=404)

    return JSONResponse({"message": "User email has been changed"})

@router.put('/api/users/{id}/password')
async def change_password(id: int, new_password: str = Body(), repo: UserRepository = Depends(UserRepository)):
    try:
        await repo.update_password(id, new_password)
    except ValueError:
        raise HTTPException(status_code=404)

    return JSONResponse({"message": "User password has been changed"})

@router.post('/api/users/xml')
async def show_users(repo: UserRepository = Depends(UserRepository)):
    users = await repo.get_users()

    xml_users = ""
    for user in users:
        xml_users += f"<tns:User><tns:id>{user["id"]}</tns:id><tns:email>{user["email"]}</tns:email></tns:User>"

    result_xml = f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope"
                xmlns:tns="http://localhost:8000/api/users/xml">
            <soap:Body>
                <tns:show_usersResponse>
                    <tns:usersResult>
                        {xml_users}
                    </tns:usersResult>
                </tns:show_usersResponse>
            </soap:Body>
        </soap:Envelope>
    """

    return Response(content=result_xml, media_type="application/xml" )