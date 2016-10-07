from application.mongo.model import Profile
from application.utils import cisco
from application.logic import GameWorld

from bson.objectid import ObjectId

def get_all_profiles():
    return Profile().get_all()

def get_profile_by_mac_address(mac_address):
    profile = Profile().get_profile_by_mac_address(mac_address)
    if profile is None:
        success, message, data = create_profile(mac_address)
        if success:
            return success, message, data, True
        return  False, 'profile_not_found', None, False
    
    return  True, 'profile_fetch', {
            'id': str(profile['_id'])
        }, False

def create_profile(mac_address): 
    profile = Profile().get_profile_by_mac_address(mac_address)
    if profile is not None:
        return False, 'profile_already_exist', None
    
    res = Profile().create(mac_address, {})
    if res.inserted_id is None:
        return False, 'profile_not_created', None
    return True, 'profile_created', {'id': str(res.inserted_id)}

def fetch_all_clients():
    clients = cisco.get_all_clients()
    for c in clients:
        mac_address = c.get('macAddress')
        location = c.get('mapCoordinate')
        Profile().create(mac_address, location)

    GameWorld().update_world()
    
def get_profile_id(profile_id):
    try:
        return ObjectId(profile_id)
    except:
        return ''

def get_game_info(profile_id):
    data = Profile().get_all_active_players()
    
    active_player = {}
    neighbours = []

    profile = Profile().get_tmp_profile()
    if profile is not None:
        profile_id = str(profile['_id'])
    
    for d in data:
        if str(d['_id']) == profile_id:
            active_player = {
                'location': d['location'],
                'is_active': d['is_active'],
                'size': d['size']
            }
        else:
            neighbours.append({
                'id': str(d['_id']),
                'location': d['location'],
                'is_active': d['is_active'],
                'size': d['size']
            })
    
    return {
        'active_player': active_player,
        'neighbours': neighbours
    }    