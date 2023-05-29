import omni.ext
import omni.ui as ui
import asyncio
import carb.input
import omni.kit.menu.utils
import omni.kit.undo
import omni.kit.commands
import omni.usd
from omni.kit.menu.utils import MenuItemDescription
from pxr import Sdf
# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class GoBildaExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[goBilda] GoBilda startup")

        # Register a menu item under the "Extensions" menu
        self.extensionID = ext_id
        self.aboutWindow()
        self.init_menu(ext_id)
        self.stage = omni.usd.get_context().get_stage()

    _menu_list = None
    _sub_menu_list = None

    # Menu name.
    _menu_name = "goBilda"

    def aboutWindow(self):
        self._window = ui.Window("goBilda Extension", width=500, textwrap=True)
        with self._window.frame:
            with ui.VStack():
                #######  Image : Omniverse logo ########
                with ui.HStack():
                    ext_manager = omni.kit.app.get_app().get_extension_manager()
                    ext_path = ext_manager.get_extension_path(self.extensionID)
                    img = ui.Image(alignment=ui.Alignment.CENTER)
                    img.source_url = ext_path + "/data/goBildaLogo.png"
                ui.Label("""
                This is an unofficial extension for goBilda parts. goBilda is 
                goBilda is an open source robotics prototyping platform that 
                can be used to build robots, machines, and more.

                This extension allows you to import goBilda parts into your
                Omniverse scene and get some useful information about the assembly,
                as well as help you simulate the assembly, and make sure that
                the parts you are using are compatible with each other through
                simulation. This can save you time and $$$.

                Here is the official goBilda website:
                https://www.gobilda.com/

                Steps to get you started building:

                1. If you are reading this you already enabled the extension.
                You can always reset this extension by disabling and enabling
                the extension if you need to. 

                2. Using the file menu bar go to:
                goBilda > parts > select a part

                3. The part will be added to the scene.

                4. You can also use the goBilda menu to get more useful information
                about the scene. 

                5. Feel free to add physics, materials and attributes that might
                be useful to your project to each individual part. 

                6. If you need to update or import a new step file for a new part
                you can do so by going to the goBilda menu and selecting the import
                step file option.

                Thanks and happy building!

                """, textwrap=True)

    def stageInfoWindow(self):
        self.stageInfoWindow = ui.Window("Stage Info", width=500, textwrap=True)
        with self.stageInfoWindow.frame:
            ui.Label("Stage Info")

    def viewportOverlay(self):
        print("viewport overlay place holder")


    def addToStage(self, component):
        """
        This function adds a component to the stage
        :param component:
        :return:
        """
        ext_manager = omni.kit.app.get_app().get_extension_manager()
        ext_path = ext_manager.get_extension_path(self.extensionID)
        primSourceLocation = ext_path + "/data/" + component + ".usd"
        omni.kit.commands.execute("CreateReference",
                                  path_to=Sdf.Path(f"/World/Components/{component}"),
                                  # Prim path for where to create the reference
                                  asset_path=primSourceLocation,
                                  # The file path to reference. Relative paths are accepted too.
                                  usd_context=omni.usd.get_context()
                                  )

    def getCost(self):
        """
        This function gets the cost of the parts in the scene
        :return:
        """
        totalCost = 0
        print("analyzing components in scene for cost")
        # get all the components in the scene
        components = self.stage.GetPrimAtPath("/World/Components").GetChildren()
        # get the cost of each component
        for component in components:
            cost = component.GetAttribute("cost").Get()
            totalCost = totalCost + cost
        print("total cost of components in scene: " + str(totalCost))
        return totalCost

    def getWeight(self):
        """
        This function gets the total weight of the parts in the scene
        :return:
        """
        totalWeight = 0
        print("analyzing components in scene for weight")
        # get all the components in the scene
        components = self.stage.GetPrimAtPath("/World/Components").GetChildren()
        # get the weight of each component
        for component in components:
            weight = component.GetAttribute("weight").Get()
            totalWeight = totalWeight + weight
        print("total weight of components in scene: " + str(totalWeight))
        return totalWeight


    def init_menu(self, ext_id):
        async def _rebuild_menus():
            await omni.kit.app.get_app().next_update_async()
            omni.kit.menu.utils.rebuild_menus()

        self.channelSubMenu = [
            MenuItemDescription(name="UChannel", onclick_fn=lambda: self.addToStage("UChannel")),
            MenuItemDescription(name="LowUChannel", onclick_fn=lambda: self.addToStage("LowUChannel")),
        ]

        self.goRailSubMenu = [
            MenuItemDescription(name="GoRailClosed", onclick_fn=lambda: self.addToStage("GoRailClosed")),
            MenuItemDescription(name="GoRailOpen", onclick_fn=lambda: self.addToStage("GoRailOpen")),
        ]

        self.beamsSubMenu = [
            MenuItemDescription(name="U Beams", onclick_fn=lambda: self.addToStage("uBeam")),
            MenuItemDescription(name="L Beams", onclick_fn=lambda: self.addToStage("lBeam")),
            MenuItemDescription(name="Flat Beams", onclick_fn=lambda: self.addToStage("flatBeam")),
            MenuItemDescription(name="Square Beams", onclick_fn=lambda: self.addToStage("squareBeam")),
            MenuItemDescription(name="Shaft Beams", onclick_fn=lambda: self.addToStage("shaftBeam")),
        ]

        self.shaftsAndTubingSubMenu = [
            MenuItemDescription(name="Steel Round", onclick_fn=lambda: self.addToStage("uBeam")),
            MenuItemDescription(name="Steel D", onclick_fn=lambda: self.addToStage("lBeam")),
            MenuItemDescription(name="Steel Rex", onclick_fn=lambda: self.addToStage("flatBeam")),
            MenuItemDescription(name="Aluminum Rex", onclick_fn=lambda: self.addToStage("squareBeam")),
            MenuItemDescription(name="Hub Shafts", onclick_fn=lambda: self.addToStage("shaftBeam")),
            MenuItemDescription(name="Aluminum Tubing", onclick_fn=lambda: self.addToStage("uBeam")),
            MenuItemDescription(name="goTube", onclick_fn=lambda: self.addToStage("lBeam")),
            MenuItemDescription(name="goRail", onclick_fn=lambda: self.addToStage("flatBeam")),
            MenuItemDescription(name="Flanged Aluminum", onclick_fn=lambda: self.addToStage("squareBeam")),
            MenuItemDescription(name="Aluminum Lead Screw Tubing", onclick_fn=lambda: self.addToStage("shaftBeam")),
            MenuItemDescription(name="Servo Tube Shaft", onclick_fn=lambda: self.addToStage("shaftBeam")),
            MenuItemDescription(name="Standoffs & Spacers", onclick_fn=lambda: self.addToStage("shaftBeam")),
            MenuItemDescription(name="Rex Standoffs", onclick_fn=lambda: self.addToStage("shaftBeam")),
        ]

        self.mountsSubMenu = [
            MenuItemDescription(name="Block Mounts", onclick_fn=lambda: self.addToStage("blockMounts")),
            MenuItemDescription(name="Dual Block Mounts", onclick_fn=lambda: self.addToStage("dualBlockMounts")),
            MenuItemDescription(name="Quad Block Pattern Mounts", onclick_fn=lambda: self.addToStage("quadBlockMounts")),
            MenuItemDescription(name="One Side Two Post Pattern", onclick_fn=lambda: self.addToStage("oneSideTwoPostPatternMounts")),
            MenuItemDescription(name="Two Side Two Post Pattern", onclick_fn=lambda: self.addToStage("twoSideTwoPostPatternMounts")),
            MenuItemDescription(name="Angle Pattern", onclick_fn=lambda: self.addToStage("anglePatternMounts")),
            MenuItemDescription(name="Gusseted Angle Pattern", onclick_fn=lambda: self.addToStage("gussetedAnglePatternMounts")),
            MenuItemDescription(name="Flat Mounts", onclick_fn=lambda: self.addToStage("flatMounts")),
            MenuItemDescription(name="Surface Mounts", onclick_fn=lambda: self.addToStage("surfaceMounts")),
            MenuItemDescription(name="Clamping Mounts", onclick_fn=lambda: self.addToStage("clampingMounts")),
            MenuItemDescription(name="Motor Mounts", onclick_fn=lambda: self.addToStage("motorMounts")),
            MenuItemDescription(name="Servo Mounts", onclick_fn=lambda: self.addToStage("servoMounts")),
            ]


        self.structureSubMenu = [
            MenuItemDescription(name="Channel", sub_menu=self.channelSubMenu),
            MenuItemDescription(name="goRail", sub_menu=self.goRailSubMenu),
            MenuItemDescription(name="Beams", sub_menu=self.beamsSubMenu),
            MenuItemDescription(name="Shafting & Tubing", sub_menu=self.shaftsAndTubingSubMenu),
            MenuItemDescription(name="Mounts", sub_menu=self.mountsSubMenu),
            MenuItemDescription(name="Clamping Mounts", onclick_fn=lambda: self.addToStage("clampingMounts")),
            MenuItemDescription(name="Grid Plates", onclick_fn=lambda: self.addToStage("gridPlates")),
            MenuItemDescription(name="Pattern Plates", onclick_fn=lambda: self.addToStage("patternPlates")),
            MenuItemDescription(name="Brackets", onclick_fn=lambda: self.addToStage("brackets")),
            MenuItemDescription(name="Base Plates", onclick_fn=lambda: self.addToStage("basePlates")),
            MenuItemDescription(name="Pattern Adaptors", onclick_fn=lambda: self.addToStage("patternAdaptors")),
            MenuItemDescription(name="Pattern Spacers", onclick_fn=lambda: self.addToStage("patternSpacers")),
            MenuItemDescription(name="Standoffs & Spacers", onclick_fn=lambda: self.addToStage("standoffsAndSpacers")),
            MenuItemDescription(name="Threaded Plates", onclick_fn=lambda: self.addToStage("threadedPlates")),
            MenuItemDescription(name="Hinges", onclick_fn=lambda: self.addToStage("hinges")),
        ]
        self.motionSubMenu = [
            MenuItemDescription(name="Motors", onclick_fn=lambda: self.addToStage("motors")),
            MenuItemDescription(name="Servos", onclick_fn=lambda: self.addToStage("servos")),
            MenuItemDescription(name="Linear Servos", onclick_fn=lambda: self.addToStage("linearServos")),
            MenuItemDescription(name="Wheels & Tires", onclick_fn=lambda: self.addToStage("wheelsAndTires")),
            MenuItemDescription(name="Tracks", onclick_fn=lambda: self.addToStage("tracks")),
            MenuItemDescription(name="Gears", onclick_fn=lambda: self.addToStage("gears")),
            MenuItemDescription(name="Sprockets & Chain", onclick_fn=lambda: self.addToStage("sprocketsAndChain")),
            MenuItemDescription(name="Timing Belts & Pulleys", onclick_fn=lambda: self.addToStage("timingBeltsAndPulleys")),
            MenuItemDescription(name="Round Belts & Pulleys", onclick_fn=lambda: self.addToStage("roundBeltsAndPulleys")),
            MenuItemDescription(name="Cable & Pulleys", onclick_fn=lambda: self.addToStage("cableAndPulleys")),
            MenuItemDescription(name="Lead Screws", onclick_fn=lambda: self.addToStage("leadScrews")),
            MenuItemDescription(name="Linear Slides", onclick_fn=lambda: self.addToStage("linearSlides")),
            MenuItemDescription(name="Linear Motion Guides", onclick_fn=lambda: self.addToStage("linearMotionGuides")),
            MenuItemDescription(name="Hubs", onclick_fn=lambda: self.addToStage("hubs")),
            MenuItemDescription(name="Bearings", onclick_fn=lambda: self.addToStage("bearings")),
            MenuItemDescription(name="Shafting & Tubing", onclick_fn=lambda: self.addToStage("shaftingAndTubing")),
            MenuItemDescription(name="Standoffs & Spacers", onclick_fn=lambda: self.addToStage("standoffsAndSpacers")),
            MenuItemDescription(name="Shaft Spacers & Shims", onclick_fn=lambda: self.addToStage("shaftsSpacersAndShims")),
            MenuItemDescription(name="Collars", onclick_fn=lambda: self.addToStage("collars")),
            MenuItemDescription(name="Couplers", onclick_fn=lambda: self.addToStage("couplers")),
            MenuItemDescription(name="Universal Joints", onclick_fn=lambda: self.addToStage("universalJoints")),
            MenuItemDescription(name="Shocks", onclick_fn=lambda: self.addToStage("shocks")),
            MenuItemDescription(name="Push Arms", onclick_fn=lambda: self.addToStage("pushArms")),
            MenuItemDescription(name="Linkages & Threaded Rods", onclick_fn=lambda: self.addToStage("linkagesAndThreadedRods")),
            MenuItemDescription(name="Hinges", onclick_fn=lambda: self.addToStage("hinges"))
        ]
        self.electronicsSubMenu = [
            MenuItemDescription(name="Motor Controllers", onclick_fn=lambda: self.addToStage("motorControllers")),
            MenuItemDescription(name="Servo Electronics", onclick_fn=lambda: self.addToStage("servoElectronics")),
            MenuItemDescription(name="Signal Mixers", onclick_fn=lambda: self.addToStage("signalMixers")),
            MenuItemDescription(name="Batteries", onclick_fn=lambda: self.addToStage("batteries")),
            MenuItemDescription(name="Voltage Regulators", onclick_fn=lambda: self.addToStage("voltageRegulators")),
            MenuItemDescription(name="Power Distribution Boards", onclick_fn=lambda: self.addToStage("powerDistributionBoards")),
            MenuItemDescription(name="Wiring", onclick_fn=lambda: self.addToStage("wiring")),
            MenuItemDescription(name="Switches", onclick_fn=lambda: self.addToStage("switches")),
            MenuItemDescription(name="Lights", onclick_fn=lambda: self.addToStage("lights")),
        ]
        self.hardwareSubMenu = [
            MenuItemDescription(name="Screws", onclick_fn=lambda: self.addToStage("screws")),
            MenuItemDescription(name="M4 Threaded Rods", onclick_fn=lambda: self.addToStage("threadedRods")),
            MenuItemDescription(name="Washers", onclick_fn=lambda: self.addToStage("washers")),
            MenuItemDescription(name="Shaft Spacers & Shims", onclick_fn=lambda: self.addToStage("sahftSpacersAndShims")),
            MenuItemDescription(name="Hole Reducers", onclick_fn=lambda: self.addToStage("holeReducers")),
            MenuItemDescription(name="Nuts", onclick_fn=lambda: self.addToStage("nuts")),
            MenuItemDescription(name="Springs", onclick_fn=lambda: self.addToStage("springs")),
            MenuItemDescription(name="Threaded Plates", onclick_fn=lambda: self.addToStage("threadedPlates")),
            MenuItemDescription(name="Standoffs & Spacers", onclick_fn=lambda: self.addToStage("standoffsAndSpacers")),
            MenuItemDescription(name="Collars", onclick_fn=lambda: self.addToStage("collars")),
            MenuItemDescription(name="Hinges", onclick_fn=lambda: self.addToStage("hinges")),
            MenuItemDescription(name="Tools", onclick_fn=lambda: self.addToStage("tools")),
            MenuItemDescription(name="Flexible Tubing", onclick_fn=lambda: self.addToStage("flexibleTubing")),
            MenuItemDescription(name="Cable", onclick_fn=lambda: self.addToStage("cable")),
            MenuItemDescription(name="Wire Management", onclick_fn=lambda: self.addToStage("wireManagement")),
            MenuItemDescription(name="Grommets", onclick_fn=lambda: self.addToStage("grommets")),
            MenuItemDescription(name="Rubber Feet", onclick_fn=lambda: self.addToStage("rubberFeet")),
            MenuItemDescription(name="Magnets", onclick_fn=lambda: self.addToStage("magnets"))
        ]
        self.stageToolsSubMenu = [
            MenuItemDescription(name="Stage Info Window", onclick_fn=lambda: self.stageInfoWindow()),
            MenuItemDescription(name="Viewport Overlay", onclick_fn=lambda: self.viewportOverlay())
        ]

        self._menu_list = [
            MenuItemDescription(name="Tools", sub_menu=self.stageToolsSubMenu),
            MenuItemDescription(),
            MenuItemDescription(name="Structure", sub_menu=self.structureSubMenu),
            MenuItemDescription(name="Motion", sub_menu=self.motionSubMenu),
            MenuItemDescription(name="Electronics", sub_menu=self.electronicsSubMenu),
            MenuItemDescription(name="Hardware", sub_menu=self.hardwareSubMenu),
            MenuItemDescription(),
            MenuItemDescription(name="About",
                                onclick_fn=lambda: self.aboutWindow()),
        ]

        # Rebuild with additional menu items.
        omni.kit.menu.utils.add_menu_items(self._menu_list, self._menu_name)
        asyncio.ensure_future(_rebuild_menus())

    def on_standards_option_select(self):
        enabled = True

    def on_standards_option_checked(self):
        enabled = False
        return enabled

    def on_standards_normally_open_option_select(self):
        enabled = False

    def on_standards_normally_closed_option_checked(self):
        enabled = True
        return enabled

    def term_menu(self):
        async def _rebuild_menus():
            await omni.kit.app.get_app().next_update_async()
            omni.kit.menu.utils.rebuild_menus()

        # Remove and rebuild the added menu items.
        omni.kit.menu.utils.remove_menu_items(self._menu_list, self._menu_name)
        asyncio.ensure_future(_rebuild_menus())

    def on_shutdown(self):
        print("[goBilda] GoBilda shutdown")
