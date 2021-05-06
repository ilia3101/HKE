import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
import colour

#Luminance of background
Y_value = 0.14
Y_sRGB = colour.models.eotf_inverse_sRGB(Y_value)

#Inspired by the image on https://en.wikipedia.org/wiki/Helmholtz%E2%80%93Kohlrausch_effect
# ***Patch colours specified in sRGB here
patches = [
    [248, 0, 0],
    [118, 131, 0],
    [0, 142, 92],
    [0, 130, 197],
    [212, 0, 234],
]
#normalise to 0-1 and linearise
for p in patches:
    for i in range (0,3):
        p[i] /= 255.0

#Make patches' luminance equal to Y_value and convert them to XYZ
patches_XYZ = []
for patch in patches:
    in_XYZ = colour.sRGB_to_XYZ(patch, apply_cctf_decoding=True)
    Y_mul = (Y_value/in_XYZ[1])
    for i in range(0,3): in_XYZ[i] *= Y_mul #Normalise Y value
    patches_XYZ.append(in_XYZ)

def plot_patches(FileName, PatchesXYZ, BackgroundColour):
    #dont know what this does
    fig,ax = plt.subplots()
    #background grey
    background_rect = mpathes.Rectangle([0.0,0.0],0.3+len(patches)*0.3,0.32,color=BackgroundColour)
    ax.add_patch(background_rect)
    #Draw all patches
    patch_count = 0
    for patch in PatchesXYZ:
        rgb = colour.XYZ_to_sRGB(patch)
        ax.add_patch(mpathes.Rectangle([0.2+patch_count*0.3, 0.06], 0.2, 0.2, color=colour.notation.RGB_to_HEX(rgb)))
        patch_count += 1
    # Save image
    plt.axis('scaled')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(FileName, dpi=500,bbox_inches='tight',pad_inches=0,transparent=True)


##################################################################################################
# Implementation of "Simple Estimation Methods forthe Helmholtz – Kohlrausch Effect" by Nayatani

# I have implemented both the VCC and VAC method, Specifically, the 'luminous colours' variant,
# although I'm not 100.0% sure about the difference between 'object colours' and 'luminous colours'...

#CIE C white point in u' v' coordinates
# u_c = 

#Theta of hue
def q(theta):
    return (- 0.01585
            - 0.03017*math.cos(theta) - 0.04556*math.cos(2*theta)
            - 0.02667*math.cos(3*theta) - 0.00295*math.cos(4*theta)
            + 0.14592*math.sin(theta) + 0.05084*math.sin(2*theta)
            - 0.01900*math.sin(3*theta) - 0.00764*math.sin(4*theta))

#KBr is normalized to sunity at La 63.66cd/m2
La = 200 #Luminance adapting, set to 200 here to represent a display at medium brightness i guess
K_Br = 0.2717 * (6.469 + 6.362 * pow(La, 0.4495)) / (6.469 + pow(La, 0.4495))

def s(uv, uv_C):
    return 13*pow((uv[0]-uv_C[0])**2 + (uv[1]-uv_C[1])**2,0.5)

def VAC(x, y):
    uv = colour.xy_to_Luv_uv([x,y])
    C = colour.xy_to_Luv_uv([0.31006,0.31616])
    theta = math.atan((uv[0]-C[0]) / (uv[1]-C[1]))
    return 0.4462 * pow(1.0 + (-0.1340*q(theta) + 0.0872*K_Br) * s(uv, C) + 0.3086, 3)

def VCC(x, y):
    uv = colour.xy_to_Luv_uv([x,y])
    C = colour.xy_to_Luv_uv([0.31006,0.31616])
    theta = math.atan2(uv[1]-C[1], uv[0]-C[0])
    return 0.4462 * pow(1.0 + (-0.8660*q(theta) + 0.0872*K_Br)*s(uv, C) + 0.3086, 3)

##################################################################################################

grey_colour = colour.notation.RGB_to_HEX([Y_sRGB,Y_sRGB,Y_sRGB])

plot_patches("equal_Y.png", patches_XYZ, grey_colour)


bg_xy = colour.XYZ_to_xy(colour.sRGB_to_XYZ([Y_sRGB,Y_sRGB,Y_sRGB]))
bg_vcc = VCC(bg_xy[0], bg_xy[1])

#Try to compensate the patches
for i in range (0,len(patches_XYZ)):
    patch = patches_XYZ[i]
    in_xy = colour.XYZ_to_xy(patch)
    Leq_L = VCC(in_xy[0], in_xy[1])
    fac = bg_vcc/Leq_L
    print("Luminance factor for patch " + str(i) + " = " + str(fac))
    patch *= fac

plot_patches("HKE_compensated.png", patches_XYZ, grey_colour)