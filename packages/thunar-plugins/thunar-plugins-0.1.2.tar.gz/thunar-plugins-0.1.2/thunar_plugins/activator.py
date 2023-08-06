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
            "Couldn't load {} entry-point {} from {}: {}".format(
                repr(thunar_plugin_entry_point_name),
                repr(entry_point.name),
                repr(entry_point.dist or "unknown distribution"),
                e,
            )
        )
        continue
    print(
        "Found {} entry-point {} ({}) from {}".format(
            repr(thunar_plugin_entry_point_name),
            repr(entry_point.name),
            repr(entry_point_obj),
            repr(entry_point.dist or "unknown distribution"),
        )
    )
    locals()[entry_point_obj.__name__] = entry_point_obj
    del entry_point_obj
