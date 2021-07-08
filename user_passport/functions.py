from db_model.db_utils import _query


def get_profile(user):
    q = f"""SELECT * FROM user_card WHERE user_id = {user.id}"""
    return _query(q)


def save_profile(address, phone, user):
    q = f"""UPDATE user_card SET address = '{address}', phone = '{phone}' WHERE user_id = {user.id};
            INSERT INTO user_card (user_id, address, phone) 
            SELECT {user.id}, '{address}', '{phone}'
            WHERE NOT EXISTS (SELECT 1 FROM user_card WHERE user_id = {user.id});"""
    _query(q)
