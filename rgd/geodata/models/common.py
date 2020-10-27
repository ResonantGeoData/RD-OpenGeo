import os

# from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.utils import timezone
from model_utils.managers import InheritanceManager
from s3_file_field import S3FileField

from rgd.utility import compute_checksum

from .constants import DB_SRID


class ModifiableEntry(models.Model):
    """A base class for models that need to track modified datetimes and users."""

    modified = models.DateTimeField(editable=False, help_text='The last time this entry was saved.')
    created = models.DateTimeField(editable=False, help_text='When this was added to the database.')
    # creator = models.ForeignKey(
    #     get_user_model(), on_delete=models.DO_NOTHING, related_name='creator'
    # )
    # modifier = models.ForeignKey(
    #     get_user_model(), on_delete=models.DO_NOTHING, related_name='modifier'
    # )

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        if 'update_fields' in kwargs:
            kwargs = kwargs.copy()
            kwargs['update_fields'] = set(kwargs['update_fields']) | {'modified'}
        super(ModifiableEntry, self).save(*args, **kwargs)


class SpatialEntry(models.Model):
    """Common model to all geospatial data entries.

    This is intended to be used in a mixin manner.

    """

    spatial_id = models.AutoField(primary_key=True)

    # Datetime of creation for the dataset
    acquisition_date = models.DateTimeField(null=True, default=None, blank=True)

    # This can be used with GeoDjango's geographic database functions for spatial indexing
    footprint = models.PolygonField(srid=DB_SRID, null=True, blank=True)
    outline = models.PolygonField(srid=DB_SRID, null=True, blank=True)

    objects = InheritanceManager()

    def __str__(self):
        return 'Spatial ID: {} (type: {})'.format(self.spatial_id, type(self))


class ChecksumFile(ModifiableEntry):
    """A base class for tracking files.

    Child class must implement a file field called ``file``! This ensures the
    field is initialized with coorect options like uplaod location and
    validators.

    """

    name = models.CharField(max_length=100, blank=True, null=True)
    checksum = models.CharField(max_length=64, blank=True, null=True)
    validate_checksum = models.BooleanField(
        default=False
    )  # a flag to validate the checksum against the saved checksum
    last_validation = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def update_checksum(self):
        self.checksum = compute_checksum(self.file)
        # Simple update save - not full save
        super(ChecksumFile, self).save(
            update_fields=[
                'checksum',
            ]
        )

    def validate(self):
        previous = self.checksum
        self.update_checksum()
        self.last_validation = self.checksum == previous
        # Simple update save - not full save
        super(ChecksumFile, self).save(
            update_fields=[
                'last_validation',
            ]
        )
        return self.last_validation

    def save(self, *args, **kwargs):
        # TODO: is there a cleaner way to enforce child class has `file` field?
        if not hasattr(self, 'file'):
            raise AttributeError('Child class of `ChecksumFile` must have a `file` field.')
        if not self.name:
            self.name = os.path.basename(self.file.name)
        # Must save the model with the file before accessing it for the checksum
        super(ChecksumFile, self).save(*args, **kwargs)
        # Checksum is additional step after saving everything else - simply update these fields.
        if not self.checksum or self.validate_checksum:
            if self.validate_checksum:
                self.validate()
            else:
                self.update_checksum()
            # Reset the user flags
            self.validate_checksum = False
            # Simple update save - not full save
            super(ChecksumFile, self).save(
                update_fields=[
                    'checksum',
                    'last_validation',
                    'validate_checksum',
                ]
            )


class ArbitraryFile(ChecksumFile):
    """Container for arbitrary file uploads."""

    file = S3FileField()
