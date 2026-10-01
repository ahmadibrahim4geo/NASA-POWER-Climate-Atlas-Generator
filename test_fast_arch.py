import time
import os
import arcpy
from arcpy.sa import *

arcpy.CheckOutExtension("Spatial")

gdb = r"C:\Users\ahmad\Desktop\Egypt Climate Data 1991-2025\Climate_Database_From_1991_To_2025.gdb"
pts = os.path.join(gdb, "Temperature")
mask = r"C:\Users\ahmad\Desktop\Egypt Climate Data 1991-2025\_scratch\maskp.shp"
if not arcpy.Exists(mask):
    # Find mask in sample data
    mask = r"D:\My Software\NASA POWER Climate Atlas Generator\Sample Data\Egypt Case Study\Egypt_Case_Study.gdb\Egypt_With_Islans"

out_tif = r"C:\Users\ahmad\Desktop\Egypt Climate Data 1991-2025\_scratch\fast_test.tif"
if arcpy.Exists(out_tif):
    arcpy.management.Delete(out_tif)

print("Setting environments...")
arcpy.env.outputCoordinateSystem = arcpy.Describe(pts).spatialReference
arcpy.env.extent = mask
arcpy.env.mask = mask
arcpy.env.cellSize = 250
arcpy.env.compression = "LZW"
arcpy.env.parallelProcessingFactor = "0"

print("Running pure IDW direct save...")
t0 = time.time()
surf = Idw(pts, "T_Winter_Mean", 250, 2.0)
surf.save(out_tif)
t1 = time.time()

print("Direct IDW + save completed in %.2f seconds!" % (t1 - t0))
d = arcpy.Describe(out_tif)
print("Output raster: %d x %d, format: %s, size: %d MB" % (d.width, d.height, d.format, os.path.getsize(out_tif) / (1024*1024)))

if arcpy.Exists(out_tif):
    arcpy.management.Delete(out_tif)
