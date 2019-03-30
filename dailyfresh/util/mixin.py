from django.contrib.auth.decorators import login_required

class MixInClass(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MixInClass, cls).as_view(**initkwargs)
        return login_required(view)