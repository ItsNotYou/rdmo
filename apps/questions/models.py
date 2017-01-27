from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.core.utils import get_uri_prefix
from apps.core.models import Model, TranslationMixin
from apps.domain.models import AttributeEntity

from .managers import QuestionEntityManager


@python_2_unicode_compatible
class Catalog(Model, TranslationMixin):

    uri = models.URLField(
        max_length=640, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this catalog (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256, blank=True, null=True,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this catalog.')
    )
    key = models.SlugField(
        max_length=128, blank=True, null=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this catalog. The URI will be generated from this key.')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional information about this catalog.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this catalog in lists.')
    )
    title_en = models.CharField(
        max_length=256,
        verbose_name=_('Title (en)'),
        help_text=_('The English title for this catalog.')
    )
    title_de = models.CharField(
        max_length=256,
        verbose_name=_('Title (de)'),
        help_text=_('The German title for this catalog.')
    )

    class Meta:
        ordering = ('order',)
        verbose_name = _('Catalog')
        verbose_name_plural = _('Catalogs')

    def __str__(self):
        return self.uri or self.key

    def save(self, *args, **kwargs):
        self.uri = self.build_uri()
        super(Catalog, self).save(*args, **kwargs)

        for section in self.sections.all():
            section.save()

    @property
    def title(self):
        return self.trans('title')

    @property
    def label(self):
        return self.trans('title')

    def build_uri(self):
        return get_uri_prefix(self) + '/questions/%s' % self.key


@python_2_unicode_compatible
class Section(Model, TranslationMixin):

    uri = models.URLField(
        max_length=640, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this section (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256, blank=True, null=True,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this section.')
    )
    key = models.SlugField(
        max_length=128, blank=True, null=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this section. The URI will be generated from this key.')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional information about this section.')
    )
    catalog = models.ForeignKey(
        Catalog, related_name='sections',
        verbose_name=_('Catalog'),
        help_text=_('The catalog this section belongs to.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this section in lists.')
    )
    title_en = models.CharField(
        max_length=256,
        verbose_name=_('Title (en)'),
        help_text=_('The English title for this section.')
    )
    title_de = models.CharField(
        max_length=256,
        verbose_name=_('Title (de)'),
        help_text=_('The German title for this section.')
    )
    label_en = models.TextField(
        verbose_name=_('Label (en)'),
        help_text=_('The English label for this section (auto-generated).')
    )
    label_de = models.TextField(
        verbose_name=_('Label (de)'),
        help_text=_('The German label for this section (auto-generated).')
    )

    class Meta:
        ordering = ('catalog__order', 'order')
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __str__(self):
        return self.uri or self.key

    def save(self, *args, **kwargs):
        self.uri = self.build_uri()
        self.label_en = self.build_label('en')
        self.label_de = self.build_label('de')

        super(Section, self).save(*args, **kwargs)

        for subsection in self.subsections.all():
            subsection.save()

    @property
    def title(self):
        return self.trans('title')

    @property
    def label(self):
        return self.trans('label')

    def build_uri(self):
        return get_uri_prefix(self) + '/questions/%s/%s' % (self.catalog.key, self.key)

    def build_label(self, lang):
        return getattr(self.catalog, 'title_' + lang) + ' / ' + getattr(self, 'title_' + lang)


@python_2_unicode_compatible
class Subsection(Model, TranslationMixin):

    uri = models.URLField(
        max_length=640, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this subsection (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256, blank=True, null=True,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this subsection.')
    )
    key = models.SlugField(
        max_length=128, blank=True, null=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this subsection. The URI will be generated from this key.')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional information about this subsection.')
    )
    section = models.ForeignKey(
        Section, related_name='subsections',
        verbose_name=_('Section'),
        help_text=_('The section this subsection belongs to.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this subsection in lists.')
    )
    title_en = models.CharField(
        max_length=256,
        verbose_name=_('Title (en)'),
        help_text=_('The English title for this subsection.')
    )
    title_de = models.CharField(
        max_length=256,
        verbose_name=_('Title (de)'),
        help_text=_('The German title for this subsection.')
    )
    label_en = models.TextField(
        verbose_name=_('Label (en)'),
        help_text=_('The English label for this subsection (auto-generated).')
    )
    label_de = models.TextField(
        verbose_name=_('Label (de)'),
        help_text=_('The German label for this subsection (auto-generated).')
    )

    class Meta:
        ordering = ('section__catalog__order', 'section__order', 'order')
        verbose_name = _('Subsection')
        verbose_name_plural = _('Subsections')

    def __str__(self):
        return self.uri or self.key

    def save(self, *args, **kwargs):
        self.uri = self.build_uri()
        self.label_en = self.build_label('en')
        self.label_de = self.build_label('de')

        super(Subsection, self).save(*args, **kwargs)

        for entity in self.entities.all():
            entity.save()

    @property
    def title(self):
        return self.trans('title')

    @property
    def label(self):
        return self.trans('label')

    def build_uri(self):
        return get_uri_prefix(self) + '/questions/%s/%s/%s' % (self.section.catalog.key, self.section.key, self.key)

    def build_label(self, lang):
        return getattr(self.section, 'label_' + lang) + ' / ' + getattr(self, 'title_' + lang)


class QuestionEntity(Model, TranslationMixin):

    objects = QuestionEntityManager()

    uri = models.URLField(
        max_length=640, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this question/questionset (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256, blank=True, null=True,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this question/questionset.')
    )
    key = models.SlugField(
        max_length=128, blank=True, null=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this question/questionset. The URI will be generated from this key.')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional information about this question/questionset.')
    )
    attribute_entity = models.ForeignKey(
        AttributeEntity, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
        verbose_name=_('Attribute entity'),
        help_text=_('The attribute/entity this question/questionset belongs to.')
    )
    subsection = models.ForeignKey(
        Subsection, related_name='entities',
        verbose_name=_('Subsection'),
        help_text=_('The section this question/questionset belongs to.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this question/questionset in lists.')
    )
    label_en = models.TextField(
        verbose_name=_('Label (en)'),
        help_text=_('The English label for this question/questionset (auto-generated).')
    )
    label_de = models.TextField(
        verbose_name=_('Label (de)'),
        help_text=_('The German label for this question/questionset (auto-generated).')
    )
    help_en = models.TextField(
        null=True, blank=True,
        verbose_name=_('Help (en)'),
        help_text=_('The English help text for this question/questionset.')
    )
    help_de = models.TextField(
        null=True, blank=True,
        verbose_name=_('Help (de)'),
        help_text=_('The German help text for this question/questionset.')
    )

    class Meta:
        ordering = ('subsection__section__catalog__order', 'subsection__section__order', 'subsection__order', 'order')
        verbose_name = _('Question entity')
        verbose_name_plural = _('Question entities')

    def __str__(self):
        return self.uri or self.key

    def save(self, *args, **kwargs):
        self.uri = self.build_uri()
        self.label_en = self.build_label('en')
        self.label_de = self.build_label('de')

        super(QuestionEntity, self).save(*args, **kwargs)

        for question in self.questions.all():
            question.save()

    @property
    def help(self):
        return self.trans('help')

    @property
    def label(self):
        return self.trans('label')

    @property
    def is_collection(self):
        if self.attribute_entity:
            return self.attribute_entity.is_collection
        else:
            return False

    @property
    def is_set(self):
        return not hasattr(self, 'question')

    def build_uri(self):
        try:
            question = Question.objects.get(pk=self.pk)
            return get_uri_prefix(self) + '/questions/%s/%s/%s/%s/%s' % (
                self.subsection.section.catalog.key,
                self.subsection.section.key,
                self.subsection.key,
                question.parent.key,
                self.key
            )
        except (Question.DoesNotExist, AttributeError):
            # Question.DoesNotExist is raised if self is a questionset
            # AttributeError is raised if question.parent is None
            return get_uri_prefix(self) + '/questions/%s/%s/%s/%s' % (
                self.subsection.section.catalog.key,
                self.subsection.section.key,
                self.subsection.key,
                self.key
            )

    def build_label(self, lang):
        if self.attribute_entity:
            return getattr(self.subsection, 'label_' + lang) + ' / ' + self.attribute_entity.key
        else:
            return getattr(self.subsection, 'label_' + lang) + ' / --'


class Question(QuestionEntity):

    WIDGET_TYPE_CHOICES = (
        ('text', 'Text'),
        ('textarea', 'Textarea'),
        ('yesno', 'Yes/No'),
        ('checkbox', 'Checkboxes'),
        ('radio', 'Radio buttons'),
        ('select', 'Select drop-down'),
        ('range', 'Range slider'),
        ('date', 'Date picker'),
    )

    parent = models.ForeignKey(
        QuestionEntity, blank=True, null=True, related_name='questions',
        verbose_name=_('Parent'),
        help_text=_('The question set this question belongs to.')
    )
    text_en = models.TextField(
        verbose_name=_('Text (en)'),
        help_text=_('The English text for this question.')
    )
    text_de = models.TextField(
        verbose_name=_('Text (de)'),
        help_text=_('The German text for this question.')
    )
    widget_type = models.CharField(
        max_length=12, choices=WIDGET_TYPE_CHOICES,
        verbose_name=_('Widget type'),
        help_text=_('Type of widget for this question.')
    )

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    @property
    def text(self):
        return self.trans('text')
