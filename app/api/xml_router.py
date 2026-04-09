from fastapi import APIRouter
from dicttoxml import dicttoxml
from models.user import User 
from fastapi import APIRouter, Response
from models.messages import Message as M



router = APIRouter(
    prefix='/xml',
    tags=['xml']
)

@router.get('/users')
async def users_list():
    
    u = User.load_all_users()
    
    xml_data = dicttoxml(u, custom_root='User', attr_type=False)
    
    return Response(content=xml_data, media_type="application/xml")


@router.get('/messages')
async def messages_list():

    m = M.load_all_messages()

    xml_data = dicttoxml(m, custom_root='Message', attr_type=False)
    
    return Response(content=xml_data, media_type="application/xml")