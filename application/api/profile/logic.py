from application.api.mongo.model import Profile

def get_all_profiles():
    return Profile().get_all()

def get_profile_by_mac_address(mac_address):
    profile = Profile().get_profile_by_mac_address(mac_address)
    if profile is None:
        return  False, 'profile_not_found', None
    
    return  True, 'profile_fetch', {
            'id': str(profile['_id'])
        }

def create_profile(mac_address): 
    profile = Profile().get_profile_by_mac_address(mac_address)
    if profile is not None:
        return False, 'profile_already_exist', None
    
    res = Profile().create(mac_address, {})
    if res.inserted_id is None:
        return False, 'profile_not_created', None
    return True, 'profile_created', {'id': str(res.inserted_id)}
