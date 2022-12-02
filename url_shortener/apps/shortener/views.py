import json
import logging
from datetime import datetime

from django.conf import settings
from asgiref.sync import sync_to_async
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseGone, JsonResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from apps.tokens.backends import AccessToken, jwt_settings
from apps.tokens.exceptions import TokenError
from apps.utils import agenerate_key
from .forms import UrlForm
from .models import Url

logger = logging.getLogger(__name__)


class UrlRedirectView(generic.View):

    async def get_redirect_url(self, *args, **kwargs):
        url = await Url.objects.aget(url_key=kwargs['url_key'])
        url.usage_count += 1
        await sync_to_async(url.save)()
        return url.redirect_url

    async def get(self, request, *args, **kwargs):
        url = await self.get_redirect_url(*args, **kwargs)
        if url:
            return HttpResponseRedirect(url)
        else:
            logger.warning(
                "Gone: %s", request.path,
                extra={"status_code": 410, "request": request}
            )
            return HttpResponseGone()


class ShortenUrlMixin(object):

    @csrf_exempt
    async def dispatch(self, request, *args, **kwargs):
        try:
            header_type, token = request.headers.get(
                'Authorization', ''
            ).split()
            if header_type not in jwt_settings.AUTH_HEADER_TYPES:
                return JsonResponse(
                    {'message': 'Unable to access with provided credentials'},
                    status=401
                )
        except (ValueError, IndexError):
            return JsonResponse(
                {'message': 'Unable to access with provided credentials'},
                status=401
            )
        try:
            AccessToken(token=token)
        except TokenError as e:
            msg = f'Unable to access with provided credentials. {e.args[0]}'
            return JsonResponse({'message': msg}, status=401)
        return await super().dispatch(request, *args, **kwargs)

    @staticmethod
    async def loads_request_data(request):
        try:
            return json.loads(request.body)
        except Exception:
            return {}


class ShortenUrlView(ShortenUrlMixin, generic.View):

    async def post(self, request, *args, **kwargs):
        form = UrlForm(data=await self.loads_request_data(request))
        if await sync_to_async(form.is_valid)():
            tag = await Url.objects.filter(tag=form.cleaned_data['tag']).afirst()
            if tag:
                return JsonResponse({'errors': f'{tag} tag already exists'})
            url_key = await agenerate_key(form.cleaned_data['redirect_url'])
            url = await Url.objects.filter(url_key=url_key).afirst()
            if url:
                url_key = await agenerate_key(
                    form.cleaned_data['redirect_url'], shuffle=True
                )
            if not form.cleaned_data['expired']:
                form.cleaned_data.pop('expired')
            if not form.cleaned_data['key']:
                form.cleaned_data.pop('key')
            url = Url(url_key=url_key, **form.cleaned_data)
            await sync_to_async(url.save)()
            short_url = f'{settings.DOMAIN}/{url.url_key}/'
            return JsonResponse({
                'data': {
                    'redirect_url': url.redirect_url,
                    'short_url': short_url,
                    'scheme_short_url': f'{request.scheme}://{short_url}',
                    'tag': url.tag,
                    'key': url.key,
                    'expired': url.expired,
                    'created_at': str(url.created_at)
                }
            })
        return JsonResponse({'errors': form.errors})


class ListShortenUrlView(ShortenUrlMixin, generic.View):

    async def post(self, request, *args, **kwargs):
        data = await self.loads_request_data(request)
        try:
            page_number = int(data.get('page', 1))
        except ValueError:
            return JsonResponse({'error': '`page` invalid value.'})
        try:
            per_page = int(data.get('per_page', 25))
        except ValueError:
            return JsonResponse({'error': '`per_page` invalid value.'})
        status, q_obj = await self.get_query_object(data)
        if status is False:
            return JsonResponse({'error': q_obj})
        urls = list()
        paginator = Paginator(Url.objects.filter(q_obj).all(), per_page)
        page_obj = await sync_to_async(paginator.get_page)(page_number)
        async for url in page_obj.object_list:
            short_url = f'{settings.DOMAIN}/{url.url_key}/'
            urls.append({
                'redirect_url': url.redirect_url,
                'short_url': short_url,
                'scheme_short_url': f'{request.scheme}://{short_url}',
                'tag': url.tag,
                'key': url.key,
                'expired': url.expired,
                'created_at': str(url.created_at)
            })
        total = page_obj.paginator.count
        return JsonResponse({
            'total': total,
            'pages': page_obj.paginator.num_pages if total else 0,
            'urls': urls,
        })

    @staticmethod
    async def get_query_object(data):
        q_obj = Q()
        tag = data.get('tag')
        if isinstance(tag, (list, dict, tuple)):
            return False, f'`tag` Invalid value, must be string.'
        elif tag:
            q_obj &= Q(tag=tag)
        created_at = data.get('date')
        if created_at and isinstance(created_at, dict):
            if 'gte' in created_at:
                gte = created_at['gte']
                try:
                    q_obj &= Q(created_at__gte=datetime.strptime(gte, '%Y-%m-%d'))
                except ValueError as e:
                    return False, f'`date.gte` - {e}'
            elif 'gt' in created_at:
                gt = created_at['gt']
                try:
                    q_obj &= Q(created_at__gt=datetime.strptime(gt, '%Y-%m-%d'))
                except ValueError as e:
                    return False, f'`date.gt` - {e}'

            if 'lte' in created_at:
                lte = created_at['lte']
                try:
                    q_obj &= Q(created_at__lte=datetime.strptime(lte, '%Y-%m-%d'))
                except ValueError as e:
                    return False, f'`date.lte` - {e}'
            elif 'lt' in created_at:
                lt = created_at['lt']
                try:
                    q_obj &= Q(created_at__lt=datetime.strptime(lt, '%Y-%m-%d'))
                except ValueError as e:
                    return False, f'`date.lt` - {e}'
        return True, q_obj
