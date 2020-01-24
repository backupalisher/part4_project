class part4router(object):
    def db_for_read(self, model, **hints):
        #print('label', model._meta.app_label)
        if model._meta.app_label == 'auth' or model._meta.app_label == 'sessions':
            return 'default'
        return 'part4'

    def db_for_write(self, model, **hints):
        #print('label', model._meta.app_label)
        if model._meta.app_label == 'auth' or model._meta.app_label == 'sessions':
            return 'default'
        return None

    def allow_syncdb(self, db, model):
        #print('label', model._meta.app_label)
        if db == 'default':
            return model._meta.app_label == 'auth'
        elif model._meta.app_label == 'auth':
            return False
        return None