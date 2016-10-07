from application.mongo.model import Profile


def try_subscribe(email):
    print 'try_subscribe'
    profile = Profile().get_profile_by_email(email)
    if profile is not None:
        return False, 'profile_already_exist'
    
    profile = Profile().create(email)
    if profile.inserted_id is not None:
        return True, 'profile_created'
    return False, 'profile_not_created'