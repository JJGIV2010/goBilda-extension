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
    def __init__(self):
        self.extensionID = None

    def on_startup(self, ext_id):
        print("[goBilda] GoBilda startup")

        # Register a menu item under the "Extensions" menu
        self.extensionID = ext_id
        # self.aboutWindow()
        self.init_menu(ext_id)
        self.stage = omni.usd.get_context().get_stage()

    _menu_list = None
    _sub_menu_list = None

    # Menu name.
    _menu_name = "goBilda"

    def comingSoon(self):
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
                Coming soon!
                """, textwrap=True)

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
                Welcome to the unofficial extension for goBilda parts! If you're unfamiliar, goBilda is an open-source robotics prototyping platform perfect for designing robots, machines, and much more.
        
                With our extension, you can seamlessly integrate goBilda parts into your Omniverse scene. This tool provides valuable insight into your assembly, aids in simulating your design, and even ensures part compatibility via simulation. The result? A smoother design process that saves you both time and money.
                
                Check out the official goBilda website for more information: https://www.gobilda.com/
                
                Ready to start building? Follow these simple steps:
                
                Congratulations, you've already enabled the extension! If necessary, resetting the extension is as easy as disabling and enabling it again.
                
                To select a part, navigate through the file menu bar: goBilda > parts > select a part.
                
                Your chosen part will be incorporated into the scene.
                
                For additional details about the scene, feel free to explore the goBilda menu.
                
                Customize each part to fit your project needs by adding physics, materials, and attributes as needed.
                
                To update or import a new step file for a fresh part, simply head over to the goBilda menu and choose the import step file option.
                
                Thanks for checking out the extension. Now, let the fun begin. Happy building!
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

        path = f"{ext_path}/data/models/{component}/_"
        primSourceLocation = path + component + "_allVariants.usda"
        omni.kit.commands.execute("CreatePayload",
                                  path_to=Sdf.Path(f"/World/Components/_{component}"),
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
            MenuItemDescription(name="UChannel", onclick_fn=lambda: self.addToStage("1120")),
            MenuItemDescription(name="LowUChannel", onclick_fn=lambda: self.addToStage("1121")),
        ]

        self.goRailSubMenu = [
            MenuItemDescription(name="GoRailClosed", onclick_fn=lambda: self.addToStage("1109")),
            MenuItemDescription(name="GoRailOpen", onclick_fn=lambda: self.addToStage("1118")),
        ]

        self.beamsSubMenu = [
            MenuItemDescription(name="U Beams", onclick_fn=lambda: self.addToStage("1101")),
            MenuItemDescription(name="L Beams", onclick_fn=lambda: self.addToStage("1103")),
            MenuItemDescription(name="Flat Beams", onclick_fn=lambda: self.addToStage("1102")),
            MenuItemDescription(name="Square Beams", onclick_fn=lambda: self.addToStage("1106")),
            MenuItemDescription(name="Shaft Beams", onclick_fn=lambda: self.addToStage("1119")),
        ]


        self.shaftsAndTubingSubMenu = [
            MenuItemDescription(name="Steel Round", onclick_fn=lambda: self.addToStage("2100")),
            MenuItemDescription(name="Steel D", onclick_fn=lambda: self.addToStage("2101")),
            MenuItemDescription(name="Steel Rex", onclick_fn=lambda: self.addToStage("2102")),
            MenuItemDescription(name="Aluminum Rex", onclick_fn=lambda: self.addToStage("2104")),
            MenuItemDescription(name="Hub Shafts", onclick_fn=lambda: self.addToStage("2110")),
            MenuItemDescription(name="Aluminum Tubing", onclick_fn=lambda: self.addToStage("4100")),
            MenuItemDescription(name="goTube", onclick_fn=lambda: self.addToStage("4103")),
            MenuItemDescription(name="goRail", sub_menu=self.goRailSubMenu)
        ]

        self.mountsSubMenu = [
            MenuItemDescription(name="Block Mounts", onclick_fn=lambda: self.addToStage("1203")),
            MenuItemDescription(name="Dual Block Mounts", onclick_fn=lambda: self.addToStage("1205")),
            MenuItemDescription(name="One Side Two Post Pattern", onclick_fn=lambda: self.addToStage("1400")),
            MenuItemDescription(name="Two Side Two Post Pattern", onclick_fn=lambda: self.addToStage("1401")),
            MenuItemDescription(name="Gusseted Angle Pattern", onclick_fn=lambda: self.addToStage("1204"))
            ]


        self.structureSubMenu = [
            MenuItemDescription(name="Channel", sub_menu=self.channelSubMenu),
            MenuItemDescription(name="goRail", sub_menu=self.goRailSubMenu),
            MenuItemDescription(name="Beams", sub_menu=self.beamsSubMenu),
            MenuItemDescription(name="Shafting & Tubing", sub_menu=self.shaftsAndTubingSubMenu),
            MenuItemDescription(name="Mounts", sub_menu=self.mountsSubMenu)
        ]
        self.motionSubMenu = [
            MenuItemDescription(name="Servos", onclick_fn=lambda: self.addToStage("2000"))
        ]
        self.electronicsSubMenu = [
            # MenuItemDescription(name="Motor Controllers", onclick_fn=lambda: self.addToStage("motorControllers")),
            # MenuItemDescription(name="Servo Electronics", onclick_fn=lambda: self.addToStage("servoElectronics")),
            # MenuItemDescription(name="Signal Mixers", onclick_fn=lambda: self.addToStage("signalMixers")),
            # MenuItemDescription(name="Batteries", onclick_fn=lambda: self.addToStage("batteries")),
            # MenuItemDescription(name="Voltage Regulators", onclick_fn=lambda: self.addToStage("voltageRegulators")),
            # MenuItemDescription(name="Power Distribution Boards", onclick_fn=lambda: self.addToStage("powerDistributionBoards")),
            # MenuItemDescription(name="Wiring", onclick_fn=lambda: self.addToStage("wiring")),
            # MenuItemDescription(name="Switches", onclick_fn=lambda: self.addToStage("switches")),
            # MenuItemDescription(name="Lights", onclick_fn=lambda: self.addToStage("lights")),
        ]
        self.hardwareSubMenu = [
            # MenuItemDescription(name="Screws", onclick_fn=lambda: self.addToStage("screws")),
            # MenuItemDescription(name="M4 Threaded Rods", onclick_fn=lambda: self.addToStage("threadedRods")),
            # MenuItemDescription(name="Washers", onclick_fn=lambda: self.addToStage("washers")),
            # MenuItemDescription(name="Shaft Spacers & Shims", onclick_fn=lambda: self.addToStage("sahftSpacersAndShims")),
            # MenuItemDescription(name="Hole Reducers", onclick_fn=lambda: self.addToStage("holeReducers")),
            # MenuItemDescription(name="Nuts", onclick_fn=lambda: self.addToStage("nuts")),
            # MenuItemDescription(name="Springs", onclick_fn=lambda: self.addToStage("springs")),
            # MenuItemDescription(name="Threaded Plates", onclick_fn=lambda: self.addToStage("threadedPlates")),
            # MenuItemDescription(name="Standoffs & Spacers", onclick_fn=lambda: self.addToStage("standoffsAndSpacers")),
            # MenuItemDescription(name="Collars", onclick_fn=lambda: self.addToStage("collars")),
            # MenuItemDescription(name="Hinges", onclick_fn=lambda: self.addToStage("hinges")),
            # MenuItemDescription(name="Tools", onclick_fn=lambda: self.addToStage("tools")),
            # MenuItemDescription(name="Flexible Tubing", onclick_fn=lambda: self.addToStage("flexibleTubing")),
            # MenuItemDescription(name="Cable", onclick_fn=lambda: self.addToStage("cable")),
            # MenuItemDescription(name="Wire Management", onclick_fn=lambda: self.addToStage("wireManagement")),
            # MenuItemDescription(name="Grommets", onclick_fn=lambda: self.addToStage("grommets")),
            # MenuItemDescription(name="Rubber Feet", onclick_fn=lambda: self.addToStage("rubberFeet")),
            # MenuItemDescription(name="Magnets", onclick_fn=lambda: self.addToStage("magnets"))
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
