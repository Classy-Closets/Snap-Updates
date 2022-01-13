import bpy
from bpy.props import (BoolProperty, EnumProperty, StringProperty, PointerProperty)


class WM_PROPERTIES_2d_views(bpy.types.PropertyGroup):

    expand_options: BoolProperty(name="Expand Dimension Options",
                                 description="Expands Dimension Options Box",
                                 default=True)

    page_layout_setting: EnumProperty(name="Page Layout Settings",
                                      items=[('PLAN+1ELVS', "Plan and elevations",
                                              'Plan on top plus three elevations (U-Shaped)'),
                                             ('3ELVS', 'Three elevations per page',
                                              'Three elevations per page'),
                                             ('2ELVS', "Two elevations per page",
                                              'Two elevations per page'),
                                             ('SINGLE', "One elevation per page",
                                              'One elevation per page')],
                                      default='SINGLE')

    accordions_layout_setting: EnumProperty(name="Page Layout Settings",
                                             items=[
                                                 ('1_ACCORD', "One Accordion per page",
                                                  'One accordion per page'),
                                                 ('PLAN+1ACCORDS', "Plan and Accordions",
                                                  'Plan on top plus accordions (U-Shaped)'),
                                                   ],default='PLAN+1ACCORDS')

    paper_size: EnumProperty(name="Paper Size",
                             items=[('ELEVENSEVENTEEN', '11x17',
                                     'US Ledger Paper - 11 x 17 inches - ANSI B'),
                                    ('LEGAL', 'Legal',
                                     'US Legal Paper - 8.5 x 14 inches')],
                             default='LEGAL')
    
    views_option: EnumProperty(name="2D Views Options",
                             items=[('ACCORDIONS', 'PV + Accordions + Islands',
                                     'Generates the Plan View, Accordions and existing islands'),
                                    ('ELEVATIONS', 'PV + Elevations + Islands',
                                     'Generates the Plan View, Elevations and existing islands')],
                             default='ACCORDIONS')

    single_views_option: EnumProperty(name="2D Views Options",
                                     items=[('ELEVATIONS', 'PV + Elevations + Islands',
                                            'Generates the Plan View, Elevations and existing islands')],
                                     default='ELEVATIONS')

    @classmethod
    def register(cls):
        bpy.types.WindowManager.views_2d = PointerProperty(
            name="views_2d",
            description="2d Views Object Properties",
            type=cls
        )

    @classmethod
    def unregister(cls):
        del bpy.types.WindowManager.views_2d


class single_scene_objs(bpy.types.PropertyGroup):
    obj_name: StringProperty(name="Object Name")


classes = (
    WM_PROPERTIES_2d_views,
    single_scene_objs
)

register, unregister = bpy.utils.register_classes_factory(classes)
