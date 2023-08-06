from gfaaccesslib.api_helpers import GFAExposureStack, GFAStandardExposureBuilder, GFACCDGeom, GFAExposeMode, GFARoisSet
from gfaaccesslib.api_helpers import GFARoi

roi = GFARoi.new(10, 15, 20, 25)


def header(title):
    print()
    print('*'*80)
    print(" - {0}".format(title))
    print('*'*80)


header("Custom defined exposure")
g = GFAExposureStack()
g.add_new_image_cmd(100015050)
g.add_set_modes_cmd(True, False, True, False)
g.add_set_modes_cmd(False, True, False, True)
g.add_dump_rows_cmd(2048)
g.add_wait_cmd(20*60*1000)
g.add_accumulate_rows_cmd(200)
g.add_set_roi_conf_cmd(roi)
g.add_read_rows_cmd(2000)
g.add_none_cmd()
print(g)

header("Clear Exposure stack")
g.clear()
print(g)


header("Geometry used for automatically generated exposures")
geom = GFACCDGeom()
geom.set_default_values()
print(geom)

header("Automatic Full exposure")
g = GFAStandardExposureBuilder(geom, 1502)
g.integration_time = 30020
g.mode = GFAExposeMode.full_frame
print(g)

print(g.build())

header("Store and read storage")
g.mode = GFAExposeMode.store_and_read
print(g)

print(g.build())

header("Store Image section into storage")
g.mode = GFAExposeMode.store_only
print(g)
print(g.build())

header("Read storage section without moving image section")
g.mode = GFAExposeMode.read_storage
print(g)
print(g.build())

header("Roi image with collisions on rois")
g = GFAStandardExposureBuilder(geom, 1503)
g.integration_time = 66666666
g.mode = GFAExposeMode.roi
roi = GFARoi.new_width(row_init=10, col_init=100, width=50, height=50)
g.rois.add_roi(roi)
g.rois.add_roi_geom(row_init=70, col_init=120, width=50, height=50)
for i in range(10):
    g.rois.add_roi_geom(row_init=i*45+100, col_init=120+i*10, width=50+2*i, height=40+i)
print(g)
print(g.build())

print("There are merged rois: {0}".format(g.rois.clash))
print(g.rois.merged_rois)
print(g.rois.rois)

header("Roi image without collisions on rois")
g = GFAStandardExposureBuilder(geom, 1503)
g.integration_time = 66666666
g.mode = GFAExposeMode.roi
for i in range(10):
    g.rois.add_roi_geom(row_init=i*100, col_init=120+i*10, width=50, height=50)
print(g)
print(g.build())

print("There are merged rois: {0}".format(g.rois.clash))
print(g.rois.merged_rois)
print(g.rois.rois)
