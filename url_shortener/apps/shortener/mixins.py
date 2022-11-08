from dataclasses import asdict
from typing import Tuple, List

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from openpyxl import load_workbook

from .forms import UploadFileForm


def handle_uploaded_file(f):
    fp = settings.BASE_DIR / 'media' / f.name
    with open(fp, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return fp


class BaseImportMixin(object):
    change_list_template = 'admin/shortener/change_list_import.html'
    import_template_name = None
    upload_form = UploadFileForm
    row_model = None
    sheet_name = 'Sheet1'

    def get_row_model(self):
        if self.row_model is None:
            raise ValueError(
                '`row_model` parameter is required.'
            )
        return self.row_model

    def get_fields_and_count(self) -> Tuple[List[str], int]:
        fields = list(filter(
            lambda f: f != 'message',
            self.get_row_model().__dataclass_fields__.keys()
        ))
        return fields, len(fields)

    def get_model_info(self):
        return self.model._meta.app_label, self.model._meta.model_name

    def get_urls(self):
        urls = super().get_urls()
        info = self.get_model_info()
        my_urls = [
            path('process-import/',
                 self.admin_site.admin_view(self.process_import),
                 name='%s_%s_process_import' % info),
            path('import/',
                 self.admin_site.admin_view(self.import_action),
                 name='%s_%s_import' % info),
        ]
        return my_urls + urls

    def import_action(self, request, *args, **kwargs):
        if self.import_template_name is None:
            raise ValueError(
                '`import_template_name` parameter is required.'
            )
        context = dict(
            self.admin_site.each_context(request),
            opts=self.model._meta,
            ff=self.upload_form()
        )
        if 'errors' in request.session:
            context.update(request.session.pop('errors'))
        if 'error_message' in request.session:
            self.message_user(
                request, request.session.pop('error_message'),
                messages.ERROR
            )
        request.current_app = self.admin_site.name
        return TemplateResponse(
            request, self.import_template_name, context
        )

    @method_decorator(require_POST)
    def process_import(self, request, *args, **kwargs):
        form = self.upload_form(request.POST, request.FILES)
        info = self.get_model_info()
        invalid_format = None
        invalid_rows = list()
        if form.is_valid():
            fields, fields_count = self.get_fields_and_count()
            row_model = self.get_row_model()
            file_path = handle_uploaded_file(request.FILES['file'])
            rows = list()
            wb = load_workbook(file_path, read_only=True, data_only=True)
            sheet = wb[self.sheet_name]
            idx = 0
            for row in sheet.rows:
                if idx == 0:
                    idx += 1
                    fields = tuple(f.value for f in row[:fields_count])
                    continue
                if not row:
                    request.session['error_message'] = (
                        'ფაილში ან ფაილის ბოლოში მოცემულია ცარიელი '
                        'სვეტები, გაასწორეთ ფაილი და ცადეთ თავიდან '
                        'ატვირთვა.'
                    )
                    url = reverse(
                        'admin:%s_%s_import' % info,
                        current_app=self.admin_site.name
                    )
                    return HttpResponseRedirect(url)

                row = row_model(*self.validate_row(row, fields_count))
                if row.is_valid():
                    rows.append(row)
                else:
                    invalid_rows.append(asdict(row))
            if not invalid_rows:
                self.message_user(
                    request, 'ფაილი წარმატებით დაიმპორტდა.',
                    messages.SUCCESS
                )
                self.process_result(rows)
                url = reverse('admin:%s_%s_changelist' % info,
                              current_app=self.admin_site.name)
                return HttpResponseRedirect(url)
        else:
            invalid_format = form.errors['file'][0]
        request.session['errors'] = {
            'invalid_format': invalid_format, 'invalid_rows': invalid_rows,
            'fields': fields
        }
        url = reverse('admin:%s_%s_import' % info,
                      current_app=self.admin_site.name)
        return HttpResponseRedirect(url)

    @staticmethod
    def process_result(rows):
        raise NotImplementedError(
            '`process_result` function is required, needs implement.'
        )

    @staticmethod
    def validate_row(row, fields_count):
        _row = list()
        for r in row[:fields_count]:
            if (r.value == 'NULL'
                    or (isinstance(r.value, str)
                        and r.value.strip().lower() == 'null')):
                _row.append(None)
            elif isinstance(r.value, str):
                _row.append(r.value.strip())
            else:
                _row.append(r.value)
        return _row
