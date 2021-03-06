from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ProcessFormView, ModelFormMixin


class MultiFormMixin(ContextMixin):
    form_classes = {}
    prefixes = {}
    success_urls = {}

    initial = {}
    prefix = None
    success_url = None

    def get_form_classes(self):
        return self.form_classes

    def get_forms(self, form_classes):
        return dict([(key, self._create_form(key, class_name)) \
                     for key, class_name in form_classes.items()])

    def get_instance(self, form_name):
        instance_method = 'get_%s_instance' % form_name
        if hasattr(self, instance_method):
            return getattr(self, instance_method)()
        else:
            return None

    def get_form_kwargs(self, form_name):
        kwargs = {}
        kwargs.update({'instance': self.get_instance(form_name)})  # helps when updating records
        kwargs.update({'initial': self.get_initial(form_name)})
        kwargs.update({'prefix': self.get_prefix(form_name)})

        if (self.request.method in ('POST', 'PUT')) and (form_name in self.request.POST.get('action')):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs

    def forms_valid(self, forms, form_name):
        form_valid_method = '%s_form_valid' % form_name
        if hasattr(self, form_valid_method):
            return getattr(self, form_valid_method)(forms[form_name])
        else:
            return HttpResponseRedirect(self.get_success_url(form_name))

    def forms_invalid(self, forms):
        return self.render_to_response(self.get_context_data(forms=forms))

    def get_initial(self, form_name):
        initial_method = 'get_%s_initial' % form_name
        if hasattr(self, initial_method):
            attrs = getattr(self, initial_method)()
            attrs['action'] = form_name
            return attrs
        else:
            return {'action': form_name}

    def get_prefix(self, form_name):
        return self.prefixes.get(form_name, self.prefix)

    def get_success_url(self, form_name=None):
        return self.success_urls.get(form_name, self.success_url)

    def _create_form(self, form_name, form_class):
        form_kwargs = self.get_form_kwargs(form_name)
        form = form_class(**form_kwargs)
        return form


class ProcessMultipleFormsView(ProcessFormView):

    def get(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)
        return self.render_to_response(self.get_context_data(forms=forms))

    def post(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        form_name = request.POST.get('action')

        return self._process_individual_form(form_name, form_classes)

    def _process_individual_form(self, form_name, form_classes):
        forms = self.get_forms(form_classes)
        form = forms.get(form_name)

        if not form:
            return HttpResponseForbidden()
        elif form.is_valid():
            return self.forms_valid(forms, form_name)
        else:
            return self.forms_invalid(forms)


class BaseMultipleFormsView(MultiFormMixin, ProcessMultipleFormsView):
    """
    A base view for displaying several forms.
    """


class MultiFormsView(TemplateResponseMixin, BaseMultipleFormsView):
    """
    A view for displaying several forms, and rendering a template response.
    """


class ModelMultiFormMixin(ModelFormMixin, MultiFormMixin):
    def get_form_kwargs(self, form_name):
        kwargs = {}
        kwargs.update({'initial': self.get_initial(form_name)})
        kwargs.update({'prefix': self.get_prefix(form_name)})
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs

    def get_initial(self, form_name):
        initial_method = 'get_%s_initial' % form_name
        if hasattr(self, initial_method):
            return getattr(self, initial_method)()
        else:
            return {'action': form_name}

    def get_prefix(self, form_name):
        return self.prefixes.get(form_name, self.prefix)

    def get_context_data(self, **kwargs):
        kwargs.setdefault('view', self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        return kwargs

    def get_success_url(self, form_name=None):
        return self.success_urls.get(form_name, self.success_url)

    def forms_valid(self, forms, form_name):
        """If the forms are valid, save the associated model."""
        obj = forms.get(form_name)
        obj.save()
        return HttpResponseRedirect(self.get_success_url(form_name))


class BaseMultipleFormsUpdateView(ModelMultiFormMixin, ProcessMultipleFormsView):
    """
    Base view for updating an existing object.

    Using this base class requires subclassing to provide a response mixin.
    """

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class MultiFormsUpdateView(SingleObjectTemplateResponseMixin, BaseMultipleFormsUpdateView):
    pass
