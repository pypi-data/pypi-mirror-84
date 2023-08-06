import log_pb2


class BaseEntity:
    def __init__(self, item):
        self.__item = item

    def get(self):
        return self.__item


class Actor(BaseEntity):
    def __init__(self, id, admin_id, login_token):
        BaseEntity.__init__(self, log_pb2.Actor(login_token=login_token, admin_id=admin_id, id=id))


class Device(BaseEntity):
    def __init__(self, user_agent, fingerprint):
        BaseEntity.__init__(self, log_pb2.Device(user_agent=user_agent, fingerprint=fingerprint))


class Location(BaseEntity):
    def __init__(self, lat=0, long=0, city=None, country=None, region=None, ip=None):
        BaseEntity.__init__(self,
                            log_pb2.Location(lat=lat, long=long, city=city, country=country, region=region, ip=ip))


class Page(BaseEntity):
    def __init__(self, path, referrer, utm_source, metadata=None):
        BaseEntity.__init__(self, log_pb2.Page(path=path, referrer=referrer, utm_source=utm_source, metadata=metadata))


class Affected(BaseEntity):
    def __init__(self, id, metadata=None):
        BaseEntity.__init__(self, log_pb2.Affected(id=id, metadata=metadata))


class EventEnum(BaseEntity):
    def __init__(self, key, metadata=None):
        BaseEntity.__init__(self, log_pb2.EventEnum(key=key, metadata=metadata))


class Event(BaseEntity):
    def __init__(self, owner_id, date, action_type, duration_ms, actor=None,
                 device=None, location=None,
                 pages=[], affected=[], event_enums=[]):
        def get_pb_item(entity):
            return entity.get()

        BaseEntity.__init__(self, log_pb2.Event(owner_id=owner_id, date=date, action_type=action_type,
                                                duration_ms=duration_ms, actor=actor.get(), device=device.get(),
                                                location=location.get(), pages=map(get_pb_item, pages),
                                                affected=map(get_pb_item, affected),
                                                event_enums=map(get_pb_item, event_enums)))
