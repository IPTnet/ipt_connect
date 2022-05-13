# -*- encoding: utf-8 -*-
'''
Python >= 2.4
Django >= 1.0

Author: eu@rafaelsdm.com
'''
# https://djangosnippets.org/snippets/2524/
# https://stackoverflow.com/questions/20146741/django-per-user-view-caching
# https://stackoverflow.com/questions/62913281/django-1-11-disable-cache-for-authentificated-users

from django.core.cache import cache

def cache_per_user(ttl=None, prefix=None):
    '''Decorador que faz cache da view pra cada usuario
    * ttl - Tempo de vida do cache, não enviar esse parametro significa que o
      cache vai durar até que o servidor reinicie ou decida remove-lo 
    * prefix - Prefixo a ser usado para armazenar o response no cache. Caso nao
      seja informado sera usado 'view_cache_'+function.__name__
    * cache_post - Informa se eh pra fazer cache de requisicoes POST
    * O cache para usuarios anonimos é compartilhado com todos
    * A chave do cache será uma das possiveis opcoes:
        '%s_%s'%(prefix, user.id)
        '%s_anonymous'%(prefix)
        'view_cache_%s_%s'%(function.__name__, user.id)
        'view_cache_%s_anonymous'%(function.__name__)
    '''
    def decorator(function):
        def apply_cache(request, *args, **kwargs):

            # No caching for authorized users:
            # they have to see the results of their edits immideately!

            can_cache = request.user.is_anonymous() and request.method == 'GET'

            # Gera a chave do cache
            if prefix:
                CACHE_KEY = '%s_%s'%(prefix, 'anonymous')
            else:
                CACHE_KEY = 'view_cache_%s_%s_%s'%(function.__name__, request.get_full_path(), 'anonymous')

            if can_cache:
                response = cache.get(CACHE_KEY, None)
            else:
                response = None

            if not response:
                print('Not in cache: %s'%(CACHE_KEY))
                response = function(request, *args, **kwargs)
                if can_cache:
                    cache.set(CACHE_KEY, response, ttl)
            return response
        return apply_cache
    return decorator
