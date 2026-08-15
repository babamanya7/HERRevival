
NDefines_Graphics.NGraphics.MAP_ICONS_GROUP_CAM_DISTANCE = 100				--group moving and still units
NDefines_Graphics.NGraphics.MAP_ICONS_STATE_GROUP_CAM_DISTANCE = 700.0		--group into states
NDefines_Graphics.NGraphics.MAP_ICONS_STRATEGIC_GROUP_CAM_DISTANCE = 900		--group units into air regions
NDefines_Graphics.NGraphics.AIRBASE_ICON_DISTANCE_CUTOFF = 800
NDefines_Graphics.NGraphics.NAVALBASE_ICON_DISTANCE_CUTOFF = 800
NDefines_Graphics.NGraphics.MAP_ICONS_STRATEGIC_AREA_HUGE = 220					--size limit for air region grouping
NDefines_Graphics.NGraphics.MAP_ICONS_STATE_HUGE = 100							--size limit for state grouping
NDefines_Graphics.NGraphics.MAPICON_GROUP_STRATEGIC_SIZE = 900
NDefines_Graphics.NGraphics.MAP_ICONS_GROUP_SPLIT_SELECTED_LIMIT = 10
NDefines_Graphics.NGraphics.MAP_ICONS_COARSE_COUNTRY_GROUPING_DISTANCE = 200
NDefines_Graphics.NGraphics.MAP_ICONS_COARSE_COUNTRY_GROUPING_DISTANCE_STRATEGIC = 0

NDefines_Graphics.NAirGfx.AIRPLANES_ANIMATION_GLOBAL_SPEED_PER_GAMESPEED = {0.3, 0.3, 0.3, 0.3, 0.3, 0.3}
NDefines_Graphics.NInterface.GRIDBOX_ELEMENTS_INTERPOLATION_SPEED = 0.2
NDefines_Graphics.NGraphics.GRADIENT_BORDERS_REFRESH_FREQ = 0.2 -- how frequent is gradient borders repainting (optimization for high-speed gameplay)

NDefines_Graphics.NGraphics.VICTORY_POINT_LEVELS = 3
NDefines_Graphics.NGraphics.VICTORY_POINT_MAP_ICON_AFTER = {0, 5, 20} -- After this amount of VP the map icon becomes bigger dot.
NDefines_Graphics.NGraphics.VICTORY_POINT_MAP_ICON_CAPITAL_CUTOFF_MAX = 1000.0	--Capitals are special snowflakes, they need their own number
NDefines_Graphics.NGraphics.VICTORY_POINT_MAP_ICON_TEXT_CUTOFF = {200, 500, 700}  -- At what camera distance the VP name text disappears.
NDefines_Graphics.NGraphics.VICTORY_POINT_MAP_ICON_TEXT_CUTOFF_MIN = 100.0 -- Min range for victory point text
NDefines_Graphics.NGraphics.VICTORY_POINT_MAP_ICON_TEXT_CUTOFF_MAX = 1000.0 -- Max range for victory point text
NDefines_Graphics.NGraphics.VICTORY_POINT_MAP_ICON_DOT_CUTOFF_MIN = 100.0 -- Min range for victory point dot
NDefines_Graphics.NGraphics.VICTORY_POINT_MAP_ICON_DOT_CUTOFF_MAX = 1000.0 -- Max range for victory point text
NDefines_Graphics.NGraphics.VICTORY_POINT_MAP_ICON_MAX_VICTORY_POINTS_FOR_PERCENT = 20 -- Default max value for point on the above range. It doesn't matter much if the VP value exceeds this, it'll be treated as max.

NDefines_Graphics.NGraphics.GRADIENT_BORDERS_COUNTRY_CENTER_THICKNESS = 1.5
NDefines_Graphics.NGraphics.GRADIENT_BORDERS_THICKNESS_DIPLOMACY = 1.5
NDefines_Graphics.NGraphics.BORDER_WIDTH = 1.0
NDefines_Graphics.NGraphics.GRADIENT_BORDERS_FIELD_COUNTRY_LOW = 0.0 -- country area in sum of pixels ...
NDefines_Graphics.NGraphics.GRADIENT_BORDERS_FIELD_COUNTRY_HIGH = 9000.0 -- ... the value is squared, so fe. country of size 100x100pix = 10000
NDefines_Graphics.NGraphics.GRADIENT_BORDERS_THICKNESS_COUNTRY_LOW = 15.0 -- thickness in pixels
NDefines_Graphics.NGraphics.GRADIENT_BORDERS_THICKNESS_COUNTRY_HIGH = 15.0
NDefines_Graphics.NGraphics.GRADIENT_BORDERS_THICKNESS_STATE = 3.0
NDefines_Graphics.NGraphics.GRADIENT_BORDERS_OUTLINE_CUTOFF_COUNTRY = 0.972
NDefines_Graphics.NGraphics.GRADIENT_BORDERS_OUTLINE_CUTOFF_DIPLOMACY = 0.972

NDefines.NGraphics.WEATHER_DISTANCE_CUTOFF = 1200 -- At what distance weather effects are hidden
NDefines.NGraphics.WEATHER_DISTANCE_FADE_LENGTH = 400 -- How far the fade out distance should be
NDefines.NGraphics.WEATHER_ZOOM_IN_CUTOFF = 1 -- At what distance weather effects are faded out the most when zooming in
NDefines.NGraphics.WEATHER_ZOOM_IN_FADE_LENGTH = 220 -- How far the zoom in fade out distance should be
NDefines.NGraphics.WEATHER_ZOOM_IN_FADE_FACTOR = 0.0 -- How much the weather effects should fade out when maximum zoomed in
NDefines.NGraphics.WEATHER_PLAYBACK_RATE = 0.25 -- Playback rate at maximum distance
NDefines.NGraphics.WEATHER_PLAYBACK_RATE_CUTOFF = 400 -- Playback rate maximum distance
NDefines.NGraphics.WEATHER_PLAYBACK_RATE_LENGTH = 200 -- For how long to fade between normal playback rate and maximum distance playback rate

NDefines_Graphics.NGraphics.DRAW_FOW_CUTOFF = 0 -- 400
NDefines_Graphics.NGraphics.DRAW_FOW_FADE_LENGTH = 0 -- 350

NDefines_Graphics.NAirGfx.AIRPLANES_ANIMATION_GLOBAL_SPEED_PER_GAMESPEED = { 0.3, 0.35, 0.4, 0.45, 0.5, 0.55 } -- Speed factor for each game speed (begin with paused). Larger value = faster animation.




