import adsk.core, adsk.fusion, traceback, math

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create a new sketch on the xy plane.
        sketches = rootComp.sketches;
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        # Draw hiator

        # Set parameters (cm)
        ##################################################################
        vertices = 96

        width = 16
        height = 20

        thickness = 0.04  # 0 if not extrude

        outside_ellipse_height = 12
        outside_ellipse_width = 10
        inside_ellipse_height = 9
        inside_ellipse_width = 7.5
        ###################################################################

        lines = sketch.sketchCurves.sketchLines;
        for z in range(vertices):
            t = z * 2 * math.pi / vertices
            x1 = outside_ellipse_width * math.cos(t) / 2
            y1 = outside_ellipse_height * math.sin(t) / 2
            t += math.pi / vertices
            x2 = inside_ellipse_width * math.cos(t) / 2
            y2 = inside_ellipse_height * math.sin(t) / 2
            t -= 2*math.pi / vertices
            x3 = inside_ellipse_width * math.cos(t) / 2
            y3 = inside_ellipse_height * math.sin(t) / 2
            lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0), adsk.core.Point3D.create(x2, y2, 0))
            lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0), adsk.core.Point3D.create(x3, y3, 0))

        lines.addByTwoPoints(adsk.core.Point3D.create(-width/2, height/2, 0), adsk.core.Point3D.create(width/2, height/2, 0))
        lines.addByTwoPoints(adsk.core.Point3D.create(width/2, height/2, 0), adsk.core.Point3D.create(width/2, -height/2, 0))
        lines.addByTwoPoints(adsk.core.Point3D.create(width/2, -height/2, 0), adsk.core.Point3D.create(-width/2, -height/2, 0))
        lines.addByTwoPoints(adsk.core.Point3D.create(-width/2, -height/2, 0), adsk.core.Point3D.create(-width/2, height/2, 0))

        if thickness:
            # Get extrude features
            extrudes = rootComp.features.extrudeFeatures
            # Get the profile defined by the hiator
            prof = sketch.profiles.item(1)
            # Define a distance extent
            distance = adsk.core.ValueInput.createByReal(thickness)
            extrude1 = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            # Get the extrusion body
            body1 = extrude1.bodies.item(0)
            body1.name = "hiator"




    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))