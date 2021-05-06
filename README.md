# Helmholtz-Kohlrausch effect
Here I am implementing "Simple Estimation Methods for the Helmholtz – Kohlrausch Effect" by Nayatani to see what can be done about it. I am almost certain the implementation is not correct.

Running the code generates the following images:

### Helmholtz-Kohlrausch effect in action:
![HKE demo](/images/equal_Y.png)
All the patches in the above image have the same Y luminance value as the background, but clearly look very different in terms of percieved luminance thanks to the Helmholtz-Kohlrausch effect.

### Same image, but HKE compensated for:
![HKE demo](/images/HKE_compensated.png)
Here I have tried to compensate for the HKE effect using the VCC for luminous colours from Nayatani. I would say it has overcompensated, as the red, purple and blue all look too dark to me.

This code is a work in progress.
