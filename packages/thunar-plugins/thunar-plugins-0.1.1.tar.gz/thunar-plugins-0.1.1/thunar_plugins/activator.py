import pkg_resources
import warnings

thunar_plugin_entry_point_name = "thunar_plugin"
for entry_point in pkg_resources.iter_entry_points(
    thunar_plugin_entry_point_name
):
    try:
        entry_point_obj = entry_point.load()
    except BaseException as e:
        warnings.warn(
            _("Couldn't load {} entry-point {} from {}: {}").format(
                repr(thunar_plugin_entry_point_name),
                repr(entry_point.name),
                repr(entry_point.dist or _("unknown distribution")),
                e,
            )
        )
        continue
    print(
        _("Found {} entry-point {} ({}) from {}").format(
            repr(thunar_plugin_entry_point_name),
            repr(entry_point.name),
            repr(entry_point_obj),
            repr(entry_point.dist or _("unknown distribution")),
        )
    )
    locals()[entry_point_obj.__name__] = entry_point_obj
    del entry_point_obj
