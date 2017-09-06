#!/usr/bin/env python3

import os
import subprocess
import numpy as np
import xml.etree.ElementTree as et

level=4  # hald4
#level=5  # hald5
cube_size=level*level
image_size=level*level*level

# list of styles plus a human frindly name
styles={'60\'s': '60\'s',
        '60\'s_faded': '60\'s faded',
        '60\'s_faded_alt': '60\'s faded alt',
        'agfa_apx_100': 'Agfa APX 100',
        'agfa_apx_25': 'Agfa APX 25',
        'agfa_precisa_100': 'Agfa Precisa 100',
        'agfa_ultra_color_100': 'Agfa Ultra color 100',
        'agfa_vista_200': 'Agfa Vista 200',
        'alien_green': 'alien green',
        'analogfx_anno_1870_color': 'AnalogFX anno 1870 color',
        'analogfx_old_style_i': 'AnalogFX old style I',
        'analogfx_old_style_ii': 'AnalogFX old style II',
        'analogfx_old_style_iii': 'AnalogFX old style III',
        'analogfx_sepia_color': 'AnalogFX sepia color',
        'analogfx_soft_sepia_i': 'AnalogFX soft sepia I',
        'analogfx_soft_sepia_ii': 'AnalogFX soft sepia II',
        'black_and_white': 'black and white',
        'bleach_bypass': 'bleach bypass',
        'blue_mono': 'blue mono',
        'color_rich': 'color rich',
        'expired_fade': 'expired fade',
        'expired_polaroid': 'expired Polaroid',
        'extreme': 'extreme',
        'fade': 'fade',
        'faded': 'faded',
        'faded_alt': 'faded alt',
        'faded_analog': 'faded analog',
        'faded_extreme': 'faded extreme',
        'faded_vivid': 'faded vivid',
        'faux_infrared': 'faux infrared',
        'fuji3510_constlclip': 'Fuji 3510 constlclip',
        'fuji3510_constlmap': 'Fuji 3510 constlmap',
        'fuji3510_cuspclip': 'Fuji 3510 cuspclip',
        'fuji3513_constlclip': 'Fuji 3513 constlclip',
        'fuji3513_constlmap': 'Fuji 3513 constlmap',
        'fuji3513_cuspclip': 'Fuji 3513 cuspclip',
        'fuji_160c': 'Fuji 160c',
        'fuji_160c_+': 'Fuji 160c +',
        'fuji_160c_++': 'Fuji 160c ++',
        'fuji_160c_-': 'Fuji 160c -',
        'fuji_400h': 'Fuji 400h',
        'fuji_400h_+': 'Fuji 400h +',
        'fuji_400h_++': 'Fuji 400h ++',
        'fuji_400h_-': 'Fuji 400h -',
        'fuji_800z': 'Fuji 800z',
        'fuji_800z_+': 'Fuji 800z +',
        'fuji_800z_++': 'Fuji 800z ++',
        'fuji_800z_-': 'Fuji 800z -',
        'fuji_astia_100f': 'Fuji Astia 100f',
        'fuji_fp-100c': 'Fuji FP-100c',
        'fuji_fp-100c_+': 'Fuji FP-100c +',
        'fuji_fp-100c_++': 'Fuji FP-100c ++',
        'fuji_fp-100c_+++': 'Fuji FP-100c +++',
        'fuji_fp-100c_++_alt': 'Fuji FP-100c ++ alt',
        'fuji_fp-100c_-': 'Fuji FP-100c -',
        'fuji_fp-100c_--': 'Fuji FP-100c --',
        'fuji_fp-100c_cool': 'Fuji FP-100c cool',
        'fuji_fp-100c_cool_+': 'Fuji FP-100c cool +',
        'fuji_fp-100c_cool_++': 'Fuji FP-100c cool ++',
        'fuji_fp-100c_cool_-': 'Fuji FP-100c cool -',
        'fuji_fp-100c_cool_--': 'Fuji FP-100c cool --',
        'fuji_fp-100c_negative': 'Fuji FP-100c negative',
        'fuji_fp-100c_negative_+': 'Fuji FP-100c negative +',
        'fuji_fp-100c_negative_++': 'Fuji FP-100c negative ++',
        'fuji_fp-100c_negative_+++': 'Fuji FP-100c negative +++',
        'fuji_fp-100c_negative_++_alt': 'Fuji FP-100c negative ++ alt',
        'fuji_fp-100c_negative_-': 'Fuji FP-100c negative -',
        'fuji_fp-100c_negative_--': 'Fuji FP-100c negative --',
        'fuji_fp-3000b': 'Fuji FP-3000b',
        'fuji_fp-3000b_+': 'Fuji FP-3000b +',
        'fuji_fp-3000b_++': 'Fuji FP-3000b ++',
        'fuji_fp-3000b_+++': 'Fuji FP-3000b +++',
        'fuji_fp-3000b_-': 'Fuji FP-3000b -',
        'fuji_fp-3000b_--': 'Fuji FP-3000b --',
        'fuji_fp-3000b_hc': 'Fuji FP-3000b hc',
        'fuji_fp-3000b_negative': 'Fuji FP-3000b negative',
        'fuji_fp-3000b_negative_+': 'Fuji FP-3000b negative +',
        'fuji_fp-3000b_negative_++': 'Fuji FP-3000b negative ++',
        'fuji_fp-3000b_negative_+++': 'Fuji FP-3000b negative +++',
        'fuji_fp-3000b_negative_-': 'Fuji FP-3000b negative -',
        'fuji_fp-3000b_negative_--': 'Fuji FP-3000b negative --',
        'fuji_fp-3000b_negative_early': 'Fuji FP-3000b negative early',
        'fuji_fp_100c': 'Fuji FP-100c',
        'fuji_ilford_delta_3200': 'Fuji Ilford Delta 3200',
        'fuji_ilford_delta_3200_+': 'Fuji Ilford Delta 3200 +',
        'fuji_ilford_delta_3200_++': 'Fuji Ilford Delta 3200 ++',
        'fuji_ilford_delta_3200_-': 'Fuji Ilford Delta 3200 -',
        'fuji_ilford_hp5': 'Fuji Ilford HP5',
        'fuji_ilford_hp5_+': 'Fuji Ilford HP5 +',
        'fuji_ilford_hp5_++': 'Fuji Ilford HP5 ++',
        'fuji_ilford_hp5_-': 'Fuji Ilford HP5 -',
        'fuji_neopan_1600': 'Fuji Neopan 1600',
        'fuji_neopan_1600_+': 'Fuji Neopan 1600 +',
        'fuji_neopan_1600_++': 'Fuji Neopan 1600 ++',
        'fuji_neopan_1600_-': 'Fuji Neopan 1600 -',
        'fuji_neopan_acros_100': 'Fuji Neopan Acros 100',
        'fuji_provia_100f': 'Fuji provia 100f',
        'fuji_provia_400f': 'Fuji provia 400f',
        'fuji_provia_400x': 'Fuji provia 400x',
        'fuji_sensia_100': 'Fuji sensia 100',
        'fuji_superia_100': 'Fuji superia 100',
        'fuji_superia_100_+': 'Fuji superia 100 +',
        'fuji_superia_100_++': 'Fuji superia 100 ++',
        'fuji_superia_100_-': 'Fuji superia 100 -',
        'fuji_superia_1600': 'Fuji superia 1600',
        'fuji_superia_1600_+': 'Fuji superia 1600 +',
        'fuji_superia_1600_++': 'Fuji superia 1600 ++',
        'fuji_superia_1600_-': 'Fuji superia 1600 -',
        'fuji_superia_200': 'Fuji superia 200',
        'fuji_superia_200_xpro': 'Fuji superia 200 xpro',
        'fuji_superia_400': 'Fuji superia 400',
        'fuji_superia_400_+': 'Fuji superia 400 +',
        'fuji_superia_400_++': 'Fuji superia 400 ++',
        'fuji_superia_400_-': 'Fuji superia 400 -',
        'fuji_superia_800': 'Fuji superia 800',
        'fuji_superia_800_+': 'Fuji superia 800 +',
        'fuji_superia_800_++': 'Fuji superia 800 ++',
        'fuji_superia_800_-': 'Fuji superia 800 -',
        'fuji_superia_hg_1600': 'Fuji superia hg 1600',
        'fuji_superia_reala_100': 'Fuji superia reala 100',
        'fuji_superia_x-tra_800': 'Fuji superia x-tra 800',
        'fuji_velvia_50': 'Fuji velvia 50',
        'fuji_xtrans_ii_astia_v2': 'Fuji xtrans ii astia v2',
        'fuji_xtrans_ii_classic_chrome_v1': 'Fuji xtrans ii classic chrome v1',
        'fuji_xtrans_ii_pro_neg_hi_v2': 'Fuji xtrans ii pro neg hi v2',
        'fuji_xtrans_ii_pro_neg_std_v2': 'Fuji xtrans ii pro neg std v2',
        'fuji_xtrans_ii_provia_v2': 'Fuji xtrans ii provia v2',
        'fuji_xtrans_ii_velvia_v2': 'Fuji xtrans ii velvia v2',
        'generic_fuji_astia_100': 'generic Fuji astia 100',
        'generic_fuji_provia_100': 'generic Fuji provia 100',
        'generic_fuji_velvia_100': 'generic Fuji velvia 100',
        'generic_kodachrome_64': 'generic Kodachrome 64',
        'generic_kodak_ektachrome_100_vs': 'generic Kodak Ektachrome 100 vs',
        'golden': 'golden',
        'golden_bright': 'golden bright',
        'golden_fade': 'golden fade',
        'golden_mono': 'golden mono',
        'golden_vibrant': 'golden vibrant',
        'goldfx_bright_spring_breeze': 'GoldFX bright spring breeze',
        'goldfx_bright_summer_heat': 'GoldFX bright summer heat',
        'goldfx_hot_summer_heat': 'GoldFX hot summer heat',
        'goldfx_perfect_sunset_01min': 'GoldFX perfect sunset 01min',
        'goldfx_perfect_sunset_05min': 'GoldFX perfect sunset 05min',
        'goldfx_perfect_sunset_10min': 'GoldFX perfect sunset 10min',
        'goldfx_spring_breeze': 'GoldFX spring breeze',
        'goldfx_summer_heat': 'GoldFX summer heat',
        'green_mono': 'green mono',
        'hong_kong': 'hong kong',
        'ilford_delta_100': 'Ilford Delta 100',
        'ilford_delta_3200': 'Ilford Delta 3200',
        'ilford_delta_400': 'Ilford Delta 400',
        'ilford_fp4_plus_125': 'Ilford FP4 plus 125',
        'ilford_hp5_plus_400': 'Ilford HP5 plus 400',
        'ilford_hps_800': 'Ilford HPS 800',
        'ilford_pan_f_plus_50': 'Ilford Pan F plus 50',
        'ilford_xp2': 'Ilford XP2',
        'kodak2383_constlclip': 'Kodak 2383 constlclip',
        'kodak2383_constlmap': 'Kodak 2383 constlmap',
        'kodak2383_cuspclip': 'Kodak 2383 cuspclip',
        'kodak2393_constlclip': 'Kodak 2393 constlclip',
        'kodak2393_constlmap': 'Kodak 2393 constlmap',
        'kodak2393_cuspclip': 'Kodak 2393 cuspclip',
        'kodak_bw_400_cn': 'Kodak bw 400 CN',
        'kodak_e-100_gx_ektachrome_100': 'Kodak E-100 GX Ektachrome 100',
        'kodak_ektachrome_100_vs': 'Kodak Ektachrome 100 vs',
        'kodak_elite_100_xpro': 'Kodak Elite 100 xpro',
        'kodak_elite_chrome_200': 'Kodak Elite chrome 200',
        'kodak_elite_chrome_400': 'Kodak Elite chrome 400',
        'kodak_elite_color_200': 'Kodak Elite color 200',
        'kodak_elite_color_400': 'Kodak Elite color 400',
        'kodak_elite_extracolor_100': 'Kodak Elite extracolor 100',
        'kodak_hie_(hs_infra)': 'Kodak hie (hs infra)',
        'kodak_kodachrome_200': 'Kodak Kodachrome 200',
        'kodak_kodachrome_25': 'Kodak Kodachrome 25',
        'kodak_kodachrome_64': 'Kodak Kodachrome 64',
        'kodak_portra_160': 'Kodak Portra 160',
        'kodak_portra_160_+': 'Kodak Portra 160 +',
        'kodak_portra_160_++': 'Kodak Portra 160 ++',
        'kodak_portra_160_-': 'Kodak Portra 160 -',
        'kodak_portra_160_nc': 'Kodak Portra 160 nc',
        'kodak_portra_160_nc_+': 'Kodak Portra 160 nc +',
        'kodak_portra_160_nc_++': 'Kodak Portra 160 nc ++',
        'kodak_portra_160_nc_-': 'Kodak Portra 160 nc -',
        'kodak_portra_160_vc': 'Kodak Portra 160 vc',
        'kodak_portra_160_vc_+': 'Kodak Portra 160 vc +',
        'kodak_portra_160_vc_++': 'Kodak Portra 160 vc ++',
        'kodak_portra_160_vc_-': 'Kodak Portra 160 vc -',
        'kodak_portra_400': 'Kodak Portra 400',
        'kodak_portra_400_+': 'Kodak Portra 400 +',
        'kodak_portra_400_++': 'Kodak Portra 400 ++',
        'kodak_portra_400_-': 'Kodak Portra 400 -',
        'kodak_portra_400_nc': 'Kodak Portra 400 nc',
        'kodak_portra_400_nc_+': 'Kodak Portra 400 nc +',
        'kodak_portra_400_nc_++': 'Kodak Portra 400 nc ++',
        'kodak_portra_400_nc_-': 'Kodak Portra 400 nc -',
        'kodak_portra_400_uc': 'Kodak Portra 400 uc',
        'kodak_portra_400_uc_+': 'Kodak Portra 400 uc +',
        'kodak_portra_400_uc_++': 'Kodak Portra 400 uc ++',
        'kodak_portra_400_uc_-': 'Kodak Portra 400 uc -',
        'kodak_portra_400_vc': 'Kodak Portra 400 vc',
        'kodak_portra_400_vc_+': 'Kodak Portra 400 vc +',
        'kodak_portra_400_vc_++': 'Kodak Portra 400 vc ++',
        'kodak_portra_400_vc_-': 'Kodak Portra 400 vc -',
        'kodak_portra_800': 'Kodak Portra 800',
        'kodak_portra_800_+': 'Kodak Portra 800 +',
        'kodak_portra_800_++': 'Kodak Portra 800 ++',
        'kodak_portra_800_-': 'Kodak Portra 800 -',
        'kodak_t-max_100': 'Kodak T-Max 100',
        'kodak_t-max_3200': 'Kodak T-Max 3200',
        'kodak_t-max_400': 'Kodak T-Max 400',
        'kodak_tmax_3200': 'Kodak T-Max 3200',
        'kodak_tmax_3200_+': 'Kodak T-Max 3200 +',
        'kodak_tmax_3200_++': 'Kodak T-Max 3200 ++',
        'kodak_tmax_3200_-': 'Kodak T-Max 3200 -',
        'kodak_tri-x_400': 'Kodak Tri-X 400',
        'kodak_tri-x_400_+': 'Kodak Tri-X 400 +',
        'kodak_tri-x_400_++': 'Kodak Tri-X 400 ++',
        'kodak_tri-x_400_-': 'Kodak Tri-X 400 -',
        'light_blown': 'light blown',
        'lomo': 'lomo',
        'lomography_redscale_100': 'Lomography redscale 100',
        'lomography_x-pro_slide_200': 'Lomography x-pro slide 200',
        'mono_tinted': 'mono tinted',
        'mute_shift': 'mute shift',
        'muted_fade': 'muted fade',
        'natural_vivid': 'natural vivid',
        'nostalgic': 'nostalgic',
        'orange_tone': 'orange tone',
        'pink_fade': 'pink fade',
        'polaroid_664': 'Polaroid 664',
        'polaroid_665': 'Polaroid 665',
        'polaroid_665_+': 'Polaroid 665 +',
        'polaroid_665_++': 'Polaroid 665 ++',
        'polaroid_665_-': 'Polaroid 665 -',
        'polaroid_665_--': 'Polaroid 665 --',
        'polaroid_665_negative': 'Polaroid 665 negative',
        'polaroid_665_negative_+': 'Polaroid 665 negative +',
        'polaroid_665_negative_-': 'Polaroid 665 negative -',
        'polaroid_665_negative_hc': 'Polaroid 665 negative hc',
        'polaroid_667': 'Polaroid 667',
        'polaroid_669': 'Polaroid 669',
        'polaroid_669_+': 'Polaroid 669 +',
        'polaroid_669_++': 'Polaroid 669 ++',
        'polaroid_669_+++': 'Polaroid 669 +++',
        'polaroid_669_-': 'Polaroid 669 -',
        'polaroid_669_--': 'Polaroid 669 --',
        'polaroid_669_cold': 'Polaroid 669 cold',
        'polaroid_669_cold_+': 'Polaroid 669 cold +',
        'polaroid_669_cold_-': 'Polaroid 669 cold -',
        'polaroid_669_cold_--': 'Polaroid 669 cold --',
        'polaroid_672': 'Polaroid 672',
        'polaroid_690': 'Polaroid 690',
        'polaroid_690_+': 'Polaroid 690 +',
        'polaroid_690_++': 'Polaroid 690 ++',
        'polaroid_690_-': 'Polaroid 690 -',
        'polaroid_690_--': 'Polaroid 690 --',
        'polaroid_690_cold': 'Polaroid 690 cold',
        'polaroid_690_cold_+': 'Polaroid 690 cold +',
        'polaroid_690_cold_++': 'Polaroid 690 cold ++',
        'polaroid_690_cold_-': 'Polaroid 690 cold -',
        'polaroid_690_cold_--': 'Polaroid 690 cold --',
        'polaroid_690_warm': 'Polaroid 690 warm',
        'polaroid_690_warm_+': 'Polaroid 690 warm +',
        'polaroid_690_warm_++': 'Polaroid 690 warm ++',
        'polaroid_690_warm_-': 'Polaroid 690 warm -',
        'polaroid_690_warm_--': 'Polaroid 690 warm --',
        'polaroid_polachrome': 'Polaroid Polachrome',
        'polaroid_px-100uv+_cold': 'Polaroid PX-100uv+ cold',
        'polaroid_px-100uv+_cold_+': 'Polaroid PX-100uv+ cold +',
        'polaroid_px-100uv+_cold_++': 'Polaroid PX-100uv+ cold ++',
        'polaroid_px-100uv+_cold_+++': 'Polaroid PX-100uv+ cold +++',
        'polaroid_px-100uv+_cold_-': 'Polaroid PX-100uv+ cold -',
        'polaroid_px-100uv+_cold_--': 'Polaroid PX-100uv+ cold --',
        'polaroid_px-100uv+_warm': 'Polaroid PX-100uv+ warm',
        'polaroid_px-100uv+_warm_+': 'Polaroid PX-100uv+ warm +',
        'polaroid_px-100uv+_warm_++': 'Polaroid PX-100uv+ warm ++',
        'polaroid_px-100uv+_warm_+++': 'Polaroid PX-100uv+ warm +++',
        'polaroid_px-100uv+_warm_-': 'Polaroid PX-100uv+ warm -',
        'polaroid_px-100uv+_warm_--': 'Polaroid PX-100uv+ warm --',
        'polaroid_px-680': 'Polaroid PX-680',
        'polaroid_px-680_+': 'Polaroid PX-680 +',
        'polaroid_px-680_++': 'Polaroid PX-680 ++',
        'polaroid_px-680_-': 'Polaroid PX-680 -',
        'polaroid_px-680_--': 'Polaroid PX-680 --',
        'polaroid_px-680_cold': 'Polaroid PX-680 cold',
        'polaroid_px-680_cold_+': 'Polaroid PX-680 cold +',
        'polaroid_px-680_cold_++': 'Polaroid PX-680 cold ++',
        'polaroid_px-680_cold_++_alt': 'Polaroid PX-680 cold ++ alt',
        'polaroid_px-680_cold_-': 'Polaroid PX-680 cold -',
        'polaroid_px-680_cold_--': 'Polaroid PX-680 cold --',
        'polaroid_px-680_warm': 'Polaroid PX-680 warm',
        'polaroid_px-680_warm_+': 'Polaroid PX-680 warm +',
        'polaroid_px-680_warm_++': 'Polaroid PX-680 warm ++',
        'polaroid_px-680_warm_-': 'Polaroid PX-680 warm -',
        'polaroid_px-680_warm_--': 'Polaroid PX-680 warm --',
        'polaroid_px-70': 'Polaroid PX-70',
        'polaroid_px-70_+': 'Polaroid PX-70 +',
        'polaroid_px-70_++': 'Polaroid PX-70 ++',
        'polaroid_px-70_+++': 'Polaroid PX-70 +++',
        'polaroid_px-70_-': 'Polaroid PX-70 -',
        'polaroid_px-70_--': 'Polaroid PX-70 --',
        'polaroid_px-70_cold': 'Polaroid PX-70 cold',
        'polaroid_px-70_cold_+': 'Polaroid PX-70 cold +',
        'polaroid_px-70_cold_++': 'Polaroid PX-70 cold ++',
        'polaroid_px-70_cold_-': 'Polaroid PX-70 cold -',
        'polaroid_px-70_cold_--': 'Polaroid PX-70 cold --',
        'polaroid_px-70_warm': 'Polaroid PX-70 warm',
        'polaroid_px-70_warm_+': 'Polaroid PX-70 warm +',
        'polaroid_px-70_warm_++': 'Polaroid PX-70 warm ++',
        'polaroid_px-70_warm_-': 'Polaroid PX-70 warm -',
        'polaroid_px-70_warm_--': 'Polaroid PX-70 warm --',
        'polaroid_time_zero_(expired)': 'Polaroid time zero (expired)',
        'polaroid_time_zero_(expired)_+': 'Polaroid time zero (expired) +',
        'polaroid_time_zero_(expired)_++': 'Polaroid time zero (expired) ++',
        'polaroid_time_zero_(expired)_-': 'Polaroid time zero (expired) -',
        'polaroid_time_zero_(expired)_--': 'Polaroid time zero (expired) --',
        'polaroid_time_zero_(expired)_---': 'Polaroid time zero (expired) ---',
        'polaroid_time_zero_(expired)_cold': 'Polaroid time zero (expired) cold',
        'polaroid_time_zero_(expired)_cold_-': 'Polaroid time zero (expired) cold -',
        'polaroid_time_zero_(expired)_cold_--': 'Polaroid time zero (expired) cold --',
        'polaroid_time_zero_(expired)_cold_---': 'Polaroid time zero (expired) cold ---',
        'purple': 'purple',
        'retro': 'retro',
        'rollei_ir_400': 'Rollei IR 400',
        'rollei_ortho_25': 'Rollei Ortho 25',
        'rollei_retro_100_tonal': 'Rollei Retro 100 tonal',
        'rollei_retro_80s': 'Rollei Retro 80s',
        'rotate_muted': 'rotate muted',
        'rotate_vibrant': 'rotate vibrant',
        'rotated': 'rotated',
        'rotated_crush': 'rotated crush',
        'smooth_cromeish': 'smooth cromeish',
        'smooth_fade': 'smooth fade',
        'soft_fade': 'soft fade',
        'solarized_color': 'solarized color',
        'solarized_color2': 'solarized color2',
        'summer': 'summer',
        'summer_alt': 'summer alt',
        'sunny': 'sunny',
        'sunny_alt': 'sunny alt',
        'sunny_rich': 'sunny rich',
        'sunny_warm': 'sunny warm',
        'super_warm': 'super warm',
        'super_warm_rich': 'super warm rich',
        'sutro_fx': 'Sutro FX',
        'technicalfx_backlight_filter': 'TechnicalFX backlight filter',
        'vibrant': 'vibrant',
        'vibrant_alien': 'vibrant alien',
        'vibrant_contrast': 'vibrant contrast',
        'vibrant_cromeish': 'vibrant cromeish',
        'vintage': 'vintage',
        'vintage_alt': 'vintage alt',
        'vintage_brighter': 'vintage brighter',
        'warm': 'warm',
        'warm_highlight': 'warm highlight',
        'warm_yellow': 'warm yellow',
        'zilverfx_b_w_solarization': 'ZiverFX bw solarization',
        'zilverfx_infrared': 'ZiverFX infrared',
        'zilverfx_vintage_b_w': 'ZiverFX vintage bw',
}

try:
    os.mkdir('hald_cluts_GMIC')
except FileExistsError:
    pass

try:
    os.mkdir('csv')
except FileExistsError:
    pass

try:
    os.mkdir('dtstyles')
except FileExistsError:
    pass

for style, name in styles.items():
    print('\ngenerating darktable style for film emulation style »{}«'.format(name))
    hald_name_png='hald{}.png'.format(level) 
    hald_name_pfm='hald{}.pfm'.format(level) 
    file_name_png='hald_cluts_GMIC/{}.png'.format(name) 
    file_name_pfm='hald_cluts_GMIC/{}.pfm'.format(name)
    file_name_csv='csv/{}.csv'.format(name)
    file_name_dtstyle='dtstyles/{}.dtstyle'.format(name)
    # apply film emulation style to test image
    subprocess.run([ 'gmic', hald_name_png, '-clut',
                     '{},64'.format(style), '--map_clut[0]', '[1]', '-o[2]',
                      file_name_png])
    # convert result to LAB space
    try:
        os.remove(file_name_pfm)
    except FileNotFoundError:
        pass
    # generate csv file with LAB color values of original test file and image
    subprocess.run([ 'darktable-cli', file_name_png, file_name_pfm ])
    # with film emulation applied
    with open(hald_name_pfm, 'rb') as file:
        l1=file.readline()
        l2=file.readline()
        l3=file.readline()
        A=np.fromfile(file, dtype=np.dtype('f4'))
    A=np.reshape(A, (image_size+2, image_size, 3))
    A=A[::-1, :, :]
    with open(file_name_pfm, 'rb') as file:
        l1=file.readline()
        l2=file.readline()
        l3=file.readline()
        B=np.fromfile(file, dtype=np.dtype('f4'))
    B=np.reshape(B, (image_size+2, image_size, 3))
    B=B[::-1, :, :]
    with open(file_name_csv, 'w', encoding='utf-8') as csv_file:
        csv_file.write('name;film emulation: {}\n'.format(name))
        csv_file.write('description;fitted LUT style from G''MIC film emulation style “{}”\n'.format(name))
        csv_file.write('num_gray;{}\n'.format(2*image_size))
        csv_file.write('patch;L_source;a_source;b_source;L_reference;a_reference;b_reference\n')
        for i in range(0, image_size):
            for j in range(0, image_size):
                csv_file.write('A{:02d}B{:02d};{};{};{};{};{};{}\n'.
                               format(i, j,
                                      A[i, j, 0], A[i, j, 1], A[i, j, 2],
                                      B[i, j, 0], B[i, j, 1], B[i, j, 2]))
        # make in- and out- grays identical
        for i in range(image_size, image_size+2):
            for j in range(0, image_size):
                csv_file.write('G{:02d};{};{};{};{};{};{}\n'.
                               format(j+(i-image_size)*image_size,
                                      A[i, j, 0], A[i, j, 1], A[i, j, 2],
                                      B[i, j, 0], B[i, j, 1], B[i, j, 2]))
    # remove temporary pfm file
    os.remove(file_name_pfm)
    # create darktable style
    subprocess.run([ 'darktable-chart', '--csv', file_name_csv, '49', file_name_dtstyle ])
    # remove unwanted elements from style
    tree=et.parse(file_name_dtstyle)
    for style in tree.findall('style'):
        n=0
        for plugin in style.findall('plugin'):
            if plugin.find('operation').text!='colorchecker' and plugin.find('operation').text!='tonecurve':
                style.remove(plugin)
            else:
                plugin.find('num').text=str(n)
                n=n+1
    tree.write(file_name_dtstyle)
    subprocess.run([ 'convert', file_name_png, '-scale', '1200%', file_name_png ])
