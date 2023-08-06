
from django.db import migrations, models
import warnings
import json
from djangocms_charts.migration_utils import migrate_cms_plugin


models_to_migrate = [
    'ChartJsBarModel',
    'ChartJsDoughnutModel',
    'ChartJsLineModel',
    'ChartJsPieModel',
    'ChartJsPolarModel',
    'ChartJsRadarModel',
]


# Mapping Fields
fields_to_migrate = [
    ('cmsplugin_ptr_id', 'type'),
    ('name', 'label'),
    ('table_data', 'table_data'),
    ('labels_top', 'labels_top'),
    ('labels_left', 'labels_left'),
    ('data_series_format', 'data_series_format'),

    ('title_display', 'display_title'),
    ('legend_display', 'display_legend'),
    ('legend_position', 'legend_position'),
    ('chart_width', 'chart_width'),
    ('chart_height', 'chart_height'),

    ('chart_container_classes', 'chart_container_classes'),
    ('chart_classes', 'chart_classes'),
]

chart_type_mapping = {
    'ChartJsBarPlugin': 'bar',
    'ChartJsDoughnutPlugin': 'doughnut',
    'ChartJsLinePlugin': 'line',
    'ChartJsPiePlugin': 'pie',
    'ChartJsPolarPlugin': 'polarArea',
    'ChartJsRadarPlugin': 'radar',
}


def get_chart_type(cmsplugin_ptr_id, apps):
    cmsplugin_model = apps.get_model('cms', 'cmsplugin')
    cmsplugin_inst = cmsplugin_model.objects.get(id=cmsplugin_ptr_id)
    chart_type = cmsplugin_inst.plugin_type
    return chart_type_mapping[chart_type]


# Custom functions to transform each options field
def from_legend_pos(from_val):
    return str(from_val).replace('legend-', '')


field_mappings = {
    'cmsplugin_ptr_id': {
        None: get_chart_type,
    },
    'legend_position': {
        None: from_legend_pos,
    }
}

def migrate_chart_plugins(apps, schema_editor):
    warnings.warn(
        "CAUTION - this is a full refactor of DjangoCMS Charts to ChartJS ver 2.x "
        "Not all charts and chart settings will be migrated to this new format "
        "BACKUP YOUR DATA - CHECK THE RESULTS")

    for old_app in models_to_migrate:
        old_table = f'djangocms_charts_{old_app.lower()}'

        migrate_cms_plugin(apps,
                           old_table=old_table,
                           new_app='djangocms_charts',
                           new_model='chartmodel',
                           new_plugin_type='ChartJsPlugin',
                           fields_to_migrate = fields_to_migrate,
                           value_mapping = field_mappings)

class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_charts', '0005_complete_refactor'),
    ]

    operations = [
        migrations.RunPython(migrate_chart_plugins, reverse_code=migrations.RunPython.noop)


    ]
